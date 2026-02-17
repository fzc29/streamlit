"""
Multi-Agent Portfolio Analysis System (LangChain v1 Compatible)
"""

import asyncio
import os
from datetime import datetime, timezone
from typing import Any, Dict, List

from dotenv import load_dotenv
from anthropic import Anthropic

from langchain_core.documents import Document
from langchain_community.vectorstores import FAISS

# Embeddings
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_openai import OpenAIEmbeddings

from embed import hybrid_search #, rerank


# ============================================================
# Base Agent
# ============================================================

class BaseAgent:
    def __init__(self, embedding, anthropic_client: Anthropic, base_dir: str, context_k: int = 30):
        self.embedding = embedding
        self.client = anthropic_client
        self.base_dir = base_dir
        self.context_k = context_k

        self.model = os.getenv("CLAUDE_MODEL", "claude-3-5-sonnet-latest")

        self.max_tokens = int(os.getenv("CLAUDE_MAX_OUTPUT_TOKENS", "2048"))
        self.temperature = float(os.getenv("CLAUDE_TEMPERATURE", "0"))

    def _load_vector_store(self, directory_name: str) -> FAISS:
        index_path = os.path.join(self.base_dir, directory_name)
        if not os.path.isdir(index_path):
            raise FileNotFoundError(f"FAISS index not found at {index_path}")

        return FAISS.load_local(
            index_path,
            embeddings=self.embedding,
            allow_dangerous_deserialization=True,
        )

    def _materialize_docs(self, store: FAISS) -> List[Document]:
        return list(store.docstore._dict.values())

    def _call_claude(self, system_prompt: str, user_prompt: str) -> str:
        response = self.client.messages.create(
            model=self.model,
            max_tokens=self.max_tokens,
            temperature=self.temperature,
            system=system_prompt,
            messages=[{"role": "user", "content": user_prompt}],
        )
        return "".join(
            block.text for block in response.content if hasattr(block, "text")
        ).strip()


# ============================================================
# Market Context Agent
# ============================================================

class MarketContextAgent(BaseAgent):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.context_store = self._load_vector_store("context_faiss_index")
        self.context_docs = self._materialize_docs(self.context_store)

    def analyze(self, question: str) -> Dict[str, Any]:
        context = hybrid_search(
            question,
            self.context_store,
            self.context_docs,
            #self.embedding,
            alpha=0.6,
            k=self.context_k,
        )

        # reranked = rerank(question, context)
        reranked = context

        system_prompt = (
            "You are a macro market analyst. Extract key events and impacts "
            "strictly from provided context."
        )

        user_prompt = f"""
Question: {question}

Context:
{''.join(doc.page_content for doc in reranked[:20])}
"""

        analysis = self._call_claude(system_prompt, user_prompt)

        return {
            "agent": "MarketContextAgent",
            "analysis": analysis,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }


# ============================================================
# Portfolio Performance Agent
# ============================================================

class PortfolioPerformanceAgent(BaseAgent):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.pnl_store = self._load_vector_store("pnl_faiss_index")
        self.pnl_docs = self._materialize_docs(self.pnl_store)

    def analyze(self, question: str) -> Dict[str, Any]:
        pnl = hybrid_search(
            f"{question} PnL attribution portfolio positions",
            self.pnl_store,
            self.pnl_docs,
            #self.embedding,
            alpha=0.6,
            k=self.context_k,
        )

        system_prompt = "You are a portfolio performance analyst."

        user_prompt = f"""
Question: {question}

P&L Data:
{''.join(doc.page_content for doc in pnl[:20])}
"""

        analysis = self._call_claude(system_prompt, user_prompt)

        return {
            "agent": "PortfolioPerformanceAgent",
            "analysis": analysis,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }


# ============================================================
# Risk Agent
# ============================================================

class RiskAnalystAgent(BaseAgent):
    def analyze(self, question: str, market_context: str, portfolio_performance: str):
        system_prompt = "You are a portfolio risk analyst."

        user_prompt = f"""
Question: {question}

Market Context:
{market_context}

Portfolio Performance:
{portfolio_performance}

Provide base, upside, downside scenarios with probabilities.
"""

        analysis = self._call_claude(system_prompt, user_prompt)

        return {
            "agent": "RiskAnalystAgent",
            "analysis": analysis,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }


# ============================================================
# Newsletter Writer
# ============================================================

class NewsletterWriterAgent(BaseAgent):
    def write(self, question, market_context, portfolio_performance, risk_analysis):
        system_prompt = "You are a hedge fund newsletter writer."

        user_prompt = f"""
Question: {question}

Market Context:
{market_context}

Portfolio Performance:
{portfolio_performance}

Risk Analysis:
{risk_analysis}

Write a professional monthly newsletter.
"""

        newsletter = self._call_claude(system_prompt, user_prompt)

        return {
            "agent": "NewsletterWriterAgent",
            "newsletter": newsletter,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }


# ============================================================
# Orchestrator
# ============================================================

class OrchestratorAgent:
    def __init__(self, embedding, anthropic_client, base_dir, context_k=30):
        self.market = MarketContextAgent(embedding, anthropic_client, base_dir, context_k)
        self.performance = PortfolioPerformanceAgent(embedding, anthropic_client, base_dir, context_k)
        self.risk = RiskAnalystAgent(embedding, anthropic_client, base_dir, context_k)
        self.writer = NewsletterWriterAgent(embedding, anthropic_client, base_dir, context_k)

    async def run_parallel(self, question: str):
        market_task = asyncio.to_thread(self.market.analyze, question)
        perf_task = asyncio.to_thread(self.performance.analyze, question)

        market_result, perf_result = await asyncio.gather(
            market_task, perf_task
        )

        risk_result = await asyncio.to_thread(
            self.risk.analyze,
            question,
            market_result["analysis"],
            perf_result["analysis"],
        )

        writer_result = await asyncio.to_thread(
            self.writer.write,
            question,
            market_result["analysis"],
            perf_result["analysis"],
            risk_result["analysis"],
        )

        return {
            "question": question,
            "market": market_result,
            "performance": perf_result,
            "risk": risk_result,
            "newsletter": writer_result,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }


# ============================================================
# Factory
# ============================================================

def build_agent_system():
    load_dotenv()
    base_dir = os.path.dirname(os.path.abspath(__file__))

    provider = os.getenv("MCP_EMBEDDING_PROVIDER", "gemini")

    if provider == "gemini":
        embedding = GoogleGenerativeAIEmbeddings(
            model="models/gemini-embedding-001",
            google_api_key=os.getenv("GEMINI_API_KEY"),
        )
    elif provider == "openai":
        embedding = OpenAIEmbeddings(
            model="text-embedding-3-large",
            api_key=os.getenv("OPENAI_API_KEY"),
        )
    else:
        raise ValueError("Unsupported embedding provider.")

    anthropic_client = Anthropic(api_key=os.getenv("CLAUDE_API_KEY"))

    return OrchestratorAgent(embedding, anthropic_client, base_dir)


# ============================================================
# Start Point
# ============================================================

if __name__ == "__main__":
    orchestrator = build_agent_system()

    question = "Analyze October 2025 portfolio performance and produce a newsletter."

    result = asyncio.run(orchestrator.run_parallel(question))

    print("\nNEWSLETTER\n")
    print(result["newsletter"]["newsletter"])
