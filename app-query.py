import streamlit as st
import asyncio

from multiagent import build_agent_system

st.set_page_config(
    page_title="Portfolio AI",
    page_icon="📊",
    layout="wide"
)

# -------------------------
# Top Navigation Bar
# -------------------------

st.markdown("""
    <style>
        .navbar {
            display: flex;
            align-items: center;
            background-color: #0f1117;
            padding: 10px 24px;
            margin: -60px -60px 20px -60px;
            border-bottom: 1px solid #2e2e2e;
            gap: 32px;
        }
        .navbar-brand {
            font-weight: 700;
            font-size: 16px;
            color: white;
            text-decoration: none;
            margin-right: auto;
        }
        .navbar a {
            color: #a0a0a0;
            text-decoration: none;
            font-size: 14px;
            font-weight: 500;
            transition: color 0.2s;
        }
        .navbar a:hover {
            color: white;
        }
    </style>

    <div class="navbar">
        <span class="navbar-brand">Navigation</span>
        <a href="https://honte-search-app.streamlit.app/" target="_blank">Search</a>
    </div>
""", unsafe_allow_html=True)


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

    with st.expander("View Weekly Market Data Analysis"):
        st.markdown(result["weekly"]["analysis"])

elif generate:
    st.warning("Please enter a request.")
