"""
Multi-Agent Portfolio Analysis System

This system breaks down the portfolio analysis workflow into specialized agents:
1. MarketContextAgent - Analyzes macro market drivers from context documents
2. PortfolioPerformanceAgent - Analyzes P&L data and identifies top contributors/detractors
3. RiskAnalystAgent - Performs scenario analysis and risk assessment
4. NewsletterWriterAgent - Synthesizes analysis into newsletter format
5. OrchestratorAgent - Coordinates all agents and combines their outputs

Each agent can be exposed as an MCP tool, allowing for:
- Parallel execution of independent agents
- Better separation of concerns
- Wayfound tracking of all agent interactions
- Modular, testable components
"""

import asyncio
import os
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional

from anthropic import Anthropic
from dotenv import load_dotenv
from langchain_core.documents import Document
from langchain_community.vectorstores import FAISS

from embed import hybrid_search, rerank


class BaseAgent:
    """Base class for all specialized agents."""

    def __init__(self, embedding, anthropic_client: Anthropic, base_dir: str, context_k: int = 30):
        self.embedding = embedding
        self.anthropic_client = anthropic_client
        self.base_dir = base_dir
        self.context_k = context_k
        self.model = os.getenv("CLAUDE_MODEL", "claude-3-5-sonnet-20241022")
        self.max_tokens = int(os.getenv("CLAUDE_MAX_OUTPUT_TOKENS", "2048"))
        self.temperature = float(os.getenv("CLAUDE_TEMPERATURE", "0.0"))

    def _load_vector_store(self, directory_name: str):
        index_path = os.path.join(self.base_dir, directory_name)
        if not os.path.isdir(index_path):
            # Try alternative: use october_faiss_index as fallback
            fallback_path = os.path.join(self.base_dir, "october_faiss_index")
            if os.path.isdir(fallback_path):
                print(f"⚠️  {directory_name} not found, using october_faiss_index as fallback")
                index_path = fallback_path
            else:
                raise FileNotFoundError(
                    f"FAISS index not found at {index_path}\n"
                    f"Please create the index or ensure october_faiss_index exists."
                )

        vector_store = FAISS.load_local(
            index_path,
            embeddings=self.embedding,
            allow_dangerous_deserialization=True,
        )
        return vector_store.as_retriever(search_kwargs={"k": self.context_k})

    def _materialize_docs(self, retriever) -> List[Document]:
        return list(retriever.vectorstore.docstore._dict.values())

    def _call_claude(self, system_prompt: str, user_prompt: str) -> str:
        response = self.anthropic_client.messages.create(
            model=self.model,
            max_tokens=self.max_tokens,
            temperature=self.temperature,
            system=system_prompt,
            messages=[{"role": "user", "content": user_prompt}],
        )
        chunks = []
        for block in response.content:
            if hasattr(block, "text"):
                chunks.append(block.text)
        return "".join(chunks).strip()


class MarketContextAgent(BaseAgent):
    """
    Analyzes macro market drivers from context documents.
    Extracts events, data points, and their market impacts.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.context_store = self._load_vector_store("context_faiss_index")
        self.context_docs = self._materialize_docs(self.context_store)

    def analyze(self, question: str) -> Dict[str, Any]:
        """Analyze macro market context and drivers."""
        context = hybrid_search(
            question,
            self.context_store,
            self.context_docs,
            self.embedding,
            alpha=0.6,
            k=self.context_k,
        )
        reranked_context = rerank(question, context)

        system_prompt = (
            "You are a macro market analyst specializing in identifying key market drivers, "
            "economic events, and their impacts on financial markets. Extract and summarize "
            "only from the provided context."
        )

        user_prompt = f"""
Analyze the macro market context for: {question}

From the following context documents, identify:
1. Key economic events and data releases (CPI, FOMC, employment data, etc.)
2. Market impact of each event (how it affected rates, FX, equities, commodities)
3. Risk sentiment and macro trends
4. Country/region-specific developments

Context Documents:
{''.join(doc.page_content for doc in reranked_context[:20])}

Provide a structured analysis with:
- Event/Data Point
- Market Impact
- Relevance to the portfolio question
"""

        analysis = self._call_claude(system_prompt, user_prompt)

        return {
            "agent": "MarketContextAgent",
            "analysis": analysis,
            "sources": [doc.metadata.get("source", "unknown") for doc in reranked_context[:20]],
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }


class PortfolioPerformanceAgent(BaseAgent):
    """
    Analyzes P&L data to identify top contributors and detractors.
    Links performance to specific positions and trades.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.pnl_store = self._load_vector_store("pnl_faiss_index")
        self.pnl_docs = self._materialize_docs(self.pnl_store)

    def analyze(self, question: str) -> Dict[str, Any]:
        """Analyze portfolio performance and P&L attribution."""
        pnl = hybrid_search(
            f"{question} company trade data portfolio positions P&L",
            self.pnl_store,
            self.pnl_docs,
            self.embedding,
            alpha=0.6,
            k=self.context_k,
        )

        system_prompt = (
            "You are a portfolio performance analyst specializing in P&L attribution. "
            "Identify top contributors and detractors, quantify their impact, and explain "
            "the drivers behind each position's performance."
        )

        user_prompt = f"""
Analyze portfolio performance for: {question}

From the following P&L and trade data, identify:
1. Top contributors to portfolio P&L (ranked by impact)
2. Top detractors from portfolio P&L (ranked by impact)
3. For each position: entry/exit levels, position size, P&L attribution
4. Core macro thesis underlying the portfolio

P&L and Trade Data:
{''.join(doc.page_content for doc in pnl[:20])}

Provide a structured analysis with:
- Position name/instrument
- P&L contribution (positive or negative)
- Key drivers behind the performance
- Position details (size, levels, etc.)
"""

        analysis = self._call_claude(system_prompt, user_prompt)

        return {
            "agent": "PortfolioPerformanceAgent",
            "analysis": analysis,
            "sources": [doc.metadata.get("source", "unknown") for doc in pnl[:20]],
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }


class RiskAnalystAgent(BaseAgent):
    """
    Performs scenario analysis and risk assessment.
    Evaluates base/upside/downside scenarios with probabilities and recommendations.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.context_store = self._load_vector_store("context_faiss_index")
        self.pnl_store = self._load_vector_store("pnl_faiss_index")
        self.context_docs = self._materialize_docs(self.context_store)
        self.pnl_docs = self._materialize_docs(self.pnl_store)

    def analyze(self, question: str, market_context: str, portfolio_performance: str) -> Dict[str, Any]:
        """Perform scenario analysis and risk assessment."""
        context = hybrid_search(
            question,
            self.context_store,
            self.context_docs,
            self.embedding,
            alpha=0.6,
            k=self.context_k,
        )
        pnl = hybrid_search(
            f"{question} portfolio positions",
            self.pnl_store,
            self.pnl_docs,
            self.embedding,
            alpha=0.6,
            k=self.context_k,
        )

        system_prompt = (
            "You are a risk analyst specializing in scenario planning and portfolio risk assessment. "
            "Evaluate multiple scenarios, assign probabilities, and provide tactical recommendations."
        )

        user_prompt = f"""
Perform scenario analysis for: {question}

Market Context Summary:
{market_context}

Portfolio Performance Summary:
{portfolio_performance}

Additional Context:
{''.join(doc.page_content for doc in context[:10])}

Additional P&L Data:
{''.join(doc.page_content for doc in pnl[:10])}

Provide scenario analysis with:

1. BASE SCENARIO:
   - Probability (with %)
   - Expected market conditions
   - Impact on key positions
   - Recommended tactical actions (size/hedge/close)

2. UPSIDE SCENARIO (risk-on):
   - Probability (with %)
   - Expected market conditions
   - Impact on key positions
   - Recommended tactical actions

3. DOWNSIDE SCENARIO (risk-off):
   - Probability (with %)
   - Expected market conditions
   - Impact on key positions
   - Recommended tactical actions

4. RISK ASSESSMENT:
   - High-risk areas and why
   - Suggestions for risk mitigation
   - High-return opportunities and why
   - Suggestions for capitalizing on opportunities
"""

        analysis = self._call_claude(system_prompt, user_prompt)

        return {
            "agent": "RiskAnalystAgent",
            "analysis": analysis,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }


class NewsletterWriterAgent(BaseAgent):
    """
    Synthesizes all analysis into a newsletter format.
    Matches the tone and style of example newsletters.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.newsletter_store = self._load_vector_store("newsletters_faiss_index")
        self.newsletter_docs = self._materialize_docs(self.newsletter_store)

    def write(
        self,
        question: str,
        market_context: str,
        portfolio_performance: str,
        risk_analysis: str,
    ) -> Dict[str, Any]:
        """Write newsletter synthesizing all agent analyses."""
        examples = hybrid_search(
            "Newsletter examples format style tone",
            self.newsletter_store,
            self.newsletter_docs,
            self.embedding,
            alpha=0.6,
            k=self.context_k,
        )

        system_prompt = (
            "You are a professional newsletter writer for a global macro hedge fund. "
            "Your writing should be clear, insightful, and match the tone and style of "
            "the example newsletters provided. Use professional financial language."
        )

        user_prompt = f"""
Write a monthly trading newsletter for: {question}

Example Newsletters (for style and format reference):
{''.join(doc.page_content for doc in examples[:3])}

Market Context Analysis:
{market_context}

Portfolio Performance Analysis:
{portfolio_performance}

Risk and Scenario Analysis:
{risk_analysis}

Compose a finished newsletter that:
1. References the example newsletters for tone, structure, and stylistic choices
2. Incorporates the market context analysis
3. Incorporates the portfolio performance analysis
4. Incorporates the risk and scenario analysis
5. Is structured, evidence-based, and uses concise professional financial language
6. Links portfolio outcomes to macro context
7. Highlights both qualitative insights and quantitative attribution

The newsletter should be ready for distribution to portfolio managers.
"""

        newsletter = self._call_claude(system_prompt, user_prompt)

        return {
            "agent": "NewsletterWriterAgent",
            "newsletter": newsletter,
            "sources": [doc.metadata.get("source", "unknown") for doc in examples[:3]],
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }


class OrchestratorAgent:
    """
    Coordinates all specialized agents and combines their outputs.
    Can execute agents in parallel for efficiency.
    """

    def __init__(self, embedding, anthropic_client: Anthropic, base_dir: str, context_k: int = 30):
        self.market_agent = MarketContextAgent(embedding, anthropic_client, base_dir, context_k)
        self.performance_agent = PortfolioPerformanceAgent(embedding, anthropic_client, base_dir, context_k)
        self.risk_agent = RiskAnalystAgent(embedding, anthropic_client, base_dir, context_k)
        self.writer_agent = NewsletterWriterAgent(embedding, anthropic_client, base_dir, context_k)

    async def run_parallel(self, question: str) -> Dict[str, Any]:
        """Execute independent agents in parallel for efficiency."""
        # Market and Performance agents can run in parallel
        market_task = asyncio.create_task(
            asyncio.to_thread(self.market_agent.analyze, question)
        )
        performance_task = asyncio.create_task(
            asyncio.to_thread(self.performance_agent.analyze, question)
        )

        market_result = await market_task
        performance_result = await performance_task

        # Risk agent needs outputs from market and performance
        risk_task = asyncio.create_task(
            asyncio.to_thread(
                self.risk_agent.analyze,
                question,
                market_result["analysis"],
                performance_result["analysis"],
            )
        )
        risk_result = await risk_task

        # Writer agent needs all previous outputs
        writer_result = await asyncio.to_thread(
            self.writer_agent.write,
            question,
            market_result["analysis"],
            performance_result["analysis"],
            risk_result["analysis"],
        )

        return {
            "question": question,
            "market_context": market_result,
            "portfolio_performance": performance_result,
            "risk_analysis": risk_result,
            "newsletter": writer_result,
            "orchestrated_at": datetime.now(timezone.utc).isoformat(),
        }

    def run_sequential(self, question: str) -> Dict[str, Any]:
        """Execute agents sequentially (for debugging or when parallel isn't needed)."""
        market_result = self.market_agent.analyze(question)
        performance_result = self.performance_agent.analyze(question)
        risk_result = self.risk_agent.analyze(
            question, market_result["analysis"], performance_result["analysis"]
        )
        writer_result = self.writer_agent.write(
            question,
            market_result["analysis"],
            performance_result["analysis"],
            risk_result["analysis"],
        )

        return {
            "question": question,
            "market_context": market_result,
            "portfolio_performance": performance_result,
            "risk_analysis": risk_result,
            "newsletter": writer_result,
            "orchestrated_at": datetime.now(timezone.utc).isoformat(),
        }


def build_agent_system() -> OrchestratorAgent:
    """Factory function to build the complete agent system."""
    load_dotenv()

    base_dir = os.path.dirname(os.path.abspath(__file__))
    context_k = int(os.getenv("AGENT_CONTEXT_K", "30"))

    # Build embedding stack
    provider = os.getenv("MCP_EMBEDDING_PROVIDER", "claude").lower()
    if provider in ("claude", "gemini"):
        from langchain_google_genai import GoogleGenerativeAIEmbeddings
        import google.generativeai as genai

        gemini_api_key = os.getenv("GEMINI_API_KEY")
        if not gemini_api_key:
            raise ValueError("GEMINI_API_KEY must be configured for Claude/Gemini embeddings.")
        genai.configure(api_key=gemini_api_key)
        embedding = GoogleGenerativeAIEmbeddings(
            model="models/embedding-001",
            google_api_key=gemini_api_key,
        )
    elif provider == "openai":
        from langchain_openai import OpenAIEmbeddings

        openai_api_key = os.getenv("OPENAI_API_KEY")
        if not openai_api_key:
            raise ValueError("OPENAI_API_KEY must be configured when MCP_EMBEDDING_PROVIDER=openai.")
        embedding = OpenAIEmbeddings(
            model="text-embedding-3-large",
            api_key=openai_api_key,
        )
    else:
        raise ValueError(f"Unsupported MCP_EMBEDDING_PROVIDER: {provider}")

    # Build Claude client
    claude_api_key = os.getenv("CLAUDE_API_KEY")
    if not claude_api_key:
        raise ValueError("CLAUDE_API_KEY must be set to use the Claude SDK.")
    anthropic_client = Anthropic(api_key=claude_api_key)

    return OrchestratorAgent(embedding, anthropic_client, base_dir, context_k)


if __name__ == "__main__":
    # Example usage
    orchestrator = build_agent_system()

    question = """
    You are an AI portfolio analyst for a discretionary global macro hedge fund.
    Your goal is to analyze October 2025 monthly performance data, interpret market drivers, 
    and produce a clear, insightful report for portfolio managers.
    """

    # Run sequentially (easier to debug)
    result = orchestrator.run_sequential(question)

    print("\n" + "=" * 80)
    print("NEWSLETTER OUTPUT")
    print("=" * 80)
    print(result["newsletter"]["newsletter"])

    print("\n" + "=" * 80)
    print("MARKET CONTEXT")
    print("=" * 80)
    print(result["market_context"]["analysis"])

    print("\n" + "=" * 80)
    print("PORTFOLIO PERFORMANCE")
    print("=" * 80)
    print(result["portfolio_performance"]["analysis"])

    print("\n" + "=" * 80)
    print("RISK ANALYSIS")
    print("=" * 80)
    print(result["risk_analysis"]["analysis"])

