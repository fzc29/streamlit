import asyncio
import uuid
import os
from datetime import datetime, timezone
from dotenv import load_dotenv
from wayfound import Session

# Import your existing system
from multiagent import build_agent_system


# ============================================================
# Wayfound Session Setup
# ============================================================

load_dotenv()

session = Session()


def log_step(run_id: str, step_name: str, input_payload: dict, output_payload: dict):
    """
    Logs a single step execution to Wayfound.
    """
    now = datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")

    event = {
        "timestamp": now,
        "event_type": "agent_call",
        "attributes": {
            "run_id": run_id,
            "input": input_payload,
            "output": output_payload,
            "model": os.getenv("CLAUDE_MODEL"),
            "embedding_provider": os.getenv("MCP_EMBEDDING_PROVIDER"),
        },
    }

    if session.session_id is None:
        session.create(messages=[event], is_async=False)
    else:
        session.append_to_session(messages=[event], is_async=False)


# ============================================================
# Instrumented Runner
# ============================================================

async def run_with_wayfound(question: str):
    """
    Runs full multi-agent workflow with step-level logging.
    """

    run_id = str(uuid.uuid4())

    orchestrator = build_agent_system()

    # -------------------------
    # Market (sequential)
    # -------------------------

    market_result = await asyncio.to_thread(
        orchestrator.market.analyze,
        question
    )

    log_step(
        run_id,
        "agent_call",
        {"agent": "market_context", "question": question},
        market_result,
    )

    # -------------------------
    # Performance (sequential)
    # -------------------------

    perf_result = await asyncio.to_thread(
        orchestrator.performance.analyze,
        question
    )

    log_step(
        run_id,
        "agent_call",
        {"agent": "portfolio_performance", "question": question},
        perf_result,
    )

    # -------------------------
    # Risk
    # -------------------------

    risk_result = await asyncio.to_thread(
        orchestrator.risk.analyze,
        question,
        market_result["analysis"],
        perf_result["analysis"],
    )

    log_step(
        run_id,
        "agent_call",
        {
            "question": question,
            "market_summary": market_result["analysis"],
            "performance_summary": perf_result["analysis"],
        },
        risk_result,
    )

    # -------------------------
    # Newsletter
    # -------------------------

    writer_result = await asyncio.to_thread(
        orchestrator.writer.write,
        question,
        market_result["analysis"],
        perf_result["analysis"],
        risk_result["analysis"],
    )

    log_step(
        run_id,
        "agent_call",
        {
            "question": question,
            "market_summary": market_result["analysis"],
            "performance_summary": perf_result["analysis"],
            "risk_summary": risk_result["analysis"],
        },
        writer_result,
    )

    return {
        "run_id": run_id,
        "question": question,
        "market": market_result,
        "performance": perf_result,
        "risk": risk_result,
        "newsletter": writer_result,
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }


# ============================================================
# Entry Point
# ============================================================

if __name__ == "__main__":

    question = "Analyze October 2025 portfolio performance and produce a newsletter."

    result = asyncio.run(run_with_wayfound(question))

    print("\n" + "=" * 80)
    print("RUN ID:", result["run_id"])
    print("=" * 80)

    print("\nNEWSLETTER OUTPUT\n")
    print(result["newsletter"]["newsletter"])
