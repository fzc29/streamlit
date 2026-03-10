import streamlit as st
from alex_agent import build_agent

st.set_page_config(
    page_title="HonTe",
    page_icon="",
    layout="centered"
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
        <a href="https://honte-pnl-query.streamlit.app/" target="_blank">PnL Query</a>
    </div>
""", unsafe_allow_html=True)

# ============================================================
# Custom Styling
# ============================================================

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@400;600&family=Source+Sans+3:wght@300;400;500&display=swap');

    html, body, [class*="css"] {
        font-family: 'Source Sans 3', sans-serif;
    }

    .main {
        background-color: #0f0f0f;
        color: #e8e2d9;
    }

    h1, h2, h3 {
        font-family: 'Playfair Display', serif !important;
        color: #e8e2d9 !important;
    }

    .stTextArea textarea {
        background-color: #1a1a1a !important;
        color: #e8e2d9 !important;
        border: 1px solid #333 !important;
        font-family: 'Source Sans 3', sans-serif !important;
        font-size: 15px !important;
    }

    .stButton > button {
        background-color: #c9a84c !important;
        color: #0f0f0f !important;
        font-family: 'Source Sans 3', sans-serif !important;
        font-weight: 500 !important;
        border: none !important;
        padding: 0.5rem 2rem !important;
        letter-spacing: 0.05em !important;
    }

    .stButton > button:hover {
        background-color: #e0bc6a !important;
    }

    .answer-block {
        background-color: #1a1a1a;
        border-left: 3px solid #c9a84c;
        padding: 1.5rem 2rem;
        margin-top: 1.5rem;
        border-radius: 2px;
        font-size: 16px;
        line-height: 1.8;
        color: #e8e2d9;
    }

    .source-tag {
        display: inline-block;
        background-color: #222;
        color: #888;
        font-size: 11px;
        padding: 2px 8px;
        border-radius: 2px;
        margin: 2px;
        font-family: monospace;
    }

    .divider {
        border: none;
        border-top: 1px solid #2a2a2a;
        margin: 2rem 0;
    }
</style>
""", unsafe_allow_html=True)

# ============================================================
# Load Agent
# ============================================================

@st.cache_resource
def get_agent():
    return build_agent()

try:
    agent = get_agent()
except FileNotFoundError as e:
    st.error(str(e))
    st.stop()

# ============================================================
# UI
# ============================================================

st.title("HonTe")
st.caption("Ask anything. Answers drawn from the CEO's books, transcripts, and interviews.")

st.markdown('<hr class="divider">', unsafe_allow_html=True)

query = st.text_area(
    "Your Question",
    height=120,
    placeholder="What is the CEO's view on long-term thinking vs short-term performance?",
    label_visibility="collapsed"
)

col1, col2 = st.columns([1, 5])
with col1:
    ask = st.button("Ask")

# ============================================================
# Response
# ============================================================

if ask and query.strip():
    with st.spinner("Thinking..."):
        result = agent.query(query)

    st.markdown(
        f'<div class="answer-block">{result["answer"]}</div>',
        unsafe_allow_html=True
    )

    # Show unique sources
    unique_sources = list(set(result["sources"]))
    if unique_sources:
        st.markdown('<hr class="divider">', unsafe_allow_html=True)
        st.markdown("**Sources referenced:**")
        source_html = " ".join(f'<span class="source-tag">{s}</span>' for s in unique_sources)
        st.markdown(source_html, unsafe_allow_html=True)

elif ask:
    st.warning("Please enter a question.")