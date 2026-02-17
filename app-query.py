import streamlit as st
import asyncio

from multiagent import build_agent_system

st.set_page_config(
    page_title="Portfolio AI",
    page_icon="📊",
    layout="wide"
)

st.title("📊 Portfolio Newsletter Generator")

st.markdown(
    "Generate portfolio commentary using internal research databases."
)

# -------------------------
# Lazy initialize orchestrator
# -------------------------

@st.cache_resource
def get_orchestrator():
    return build_agent_system()

orchestrator = get_orchestrator()

# -------------------------
# Input
# -------------------------

query = st.text_area(
    "Enter Request",
    height=160,
    placeholder="Example: Draft a weekly performance summary..."
)

generate = st.button("Generate")

# -------------------------
# Execution
# -------------------------

if generate and query.strip():

    with st.spinner("Running multi-agent analysis..."):

        result = asyncio.run(
            orchestrator.run_parallel(query)
        )

    st.divider()

    st.subheader("Generated Newsletter")
    st.markdown(result["newsletter"]["newsletter"])

    # Optional: show intermediate agent outputs
    with st.expander("View Market Context Analysis"):
        st.markdown(result["market"]["analysis"])

    with st.expander("View Portfolio Performance Analysis"):
        st.markdown(result["performance"]["analysis"])

    with st.expander("View Risk Analysis"):
        st.markdown(result["risk"]["analysis"])

elif generate:
    st.warning("Please enter a request.")
