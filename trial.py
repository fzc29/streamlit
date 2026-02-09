# app.py
import streamlit as st
import time
from datetime import datetime

# Mock data - no real RAG needed
MOCK_NEWSLETTER = """
# October 2025 Portfolio Commentary

## Executive Summary
The portfolio generated a **+3.2% return** in October, outperforming our benchmark by 180bps. Performance was driven primarily by our long USD positions and tactical equity hedges as risk sentiment deteriorated mid-month.

## Market Context
October saw heightened volatility across asset classes, driven by:
- **Fed Policy Shift**: FOMC minutes revealed growing dovish dissent, leading to a 15bp rally in 10Y yields
- **China Stimulus**: PBOC announced ¥2T infrastructure package, temporarily boosting EM FX
- **Geopolitical Risk**: Middle East tensions drove safe-haven flows into USD and gold

## Top Contributors (+$4.2M)

### 1. Long USD/JPY (+$1.8M) 
- **Entry**: 148.50 on Oct 3
- **Current**: 151.20 
- **Driver**: BoJ maintained ultra-loose policy despite rising inflation, widening rate differential with USD
- **Macro Link**: Fed's higher-for-longer stance vs. Japan's yield curve control created persistent carry opportunity

### 2. Short S&P 500 Futures (+$1.5M)
- **Entry**: 4,520 on Oct 12
- **Exit**: 4,380 on Oct 25
- **Driver**: Earnings recession fears + rising real yields compressed equity multiples
- **Macro Link**: ISM manufacturing fell to 46.2, confirming slowdown narrative

### 3. Long Gold (+$0.9M)
- **Entry**: $1,920/oz on Oct 1
- **Current**: $1,985/oz
- **Driver**: Geopolitical risk premium + real rate decline
- **Macro Link**: Middle East escalation + Fed pivot expectations

## Top Detractors (-$1.0M)

### 1. Long EUR/USD (-$0.6M)
- **Entry**: 1.0650 on Oct 5
- **Current**: 1.0520
- **Driver**: ECB cut rates 25bps unexpectedly, while Fed held steady
- **Macro Link**: Eurozone PMIs missed, forcing ECB into preemptive easing

### 2. Short UST 2Y (-$0.4M)
- **Entry**: Yield 4.95% on Oct 8
- **Exit**: Yield 4.75% on Oct 20
- **Driver**: Flight to quality bid overwhelmed our tactical short
- **Macro Link**: Banking sector stress in regional banks drove safe-haven demand

## Risk Analysis & Scenarios

### Base Case (60% probability)
- **Outlook**: Fed holds rates through Q1 2026, gradual slowdown continues
- **Portfolio Impact**: USD strength persists, equity volatility elevated
- **Action**: Maintain current positioning, add selectively to commodity longs

### Upside Scenario (25% probability) 
- **Outlook**: Soft landing achieved, earnings rebound in Q4
- **Portfolio Impact**: Equity hedges underperform, USD weakens vs. cyclical currencies
- **Action**: Reduce equity shorts by 30%, rotate into AUD/CAD longs

### Downside Scenario (15% probability)
- **Outlook**: Hard landing, Fed forced to cut 100bps in H1 2026
- **Portfolio Impact**: All risk assets sell off, USD whipsaws
- **Action**: Increase equity hedges, close carry trades, buy long-dated bonds

## Key Risks to Monitor
- **Fed Policy Error**: Markets pricing 75bps of cuts by mid-2026, but inflation may re-accelerate
- **China Slowdown**: Property sector showing renewed stress despite stimulus
- **Positioning Crowding**: USD longs becoming consensus, risk of violent unwind

## Tactical Recommendations
1. **Trim** USD/JPY longs by 20% after 150bp move - take profits
2. **Add** selective emerging market exposure (MXN, BRL) on weakness
3. **Hedge** tail risk via OTM SPX puts (3M expiry, 10% OTM)
4. **Monitor** ECB/BoJ policy meetings in November for potential repricing

---
*Portfolio as of October 31, 2025 | Generated on November 1, 2025*
"""

MOCK_SOURCES = [
    "newsletters/2025_03_monthly.pdf",
    "newsletters/2025_04_monthly.pdf", 
    "newsletters/2025_05_monthly.pdf",
    "context/fed_minutes_oct_2025.pdf",
    "context/ecb_press_conference_oct18.pdf",
    "context/macro_daily_oct01_oct31.pdf",
    "context/china_stimulus_announcement.pdf",
    "pnl/october_pnl_attribution.csv",
    "pnl/trade_log_oct_2025.md",
    "pnl/position_snapshot_oct31.csv"
]

MOCK_MARKET_CONTEXT = """
**Key Market Drivers - October 2025:**

1. **Federal Reserve Policy** (Oct 18 FOMC)
   - Held rates at 5.25-5.50% as expected
   - Minutes revealed growing dovish dissent among members
   - Powell emphasized "data dependence" but acknowledged cooling inflation
   - Impact: 10Y yields rallied 15bps, USD strengthened vs. EUR/JPY

2. **China Stimulus** (Oct 8 PBOC Announcement)
   - ¥2T infrastructure package targeting property sector
   - Regional bank liquidity support expanded
   - Impact: Temporary CNY strength (+1.2%), EM FX rally faded after 5 days

3. **Eurozone Weakness** (Oct 15 ECB Meeting)
   - Surprise 25bp rate cut to 3.50%
   - PMI manufacturing at 45.8 (lowest since 2020)
   - Germany in technical recession (Q2/Q3 GDP negative)
   - Impact: EUR/USD fell 130bps in 48 hours

4. **Geopolitical Tensions** (Oct 20-25)
   - Middle East escalation drove oil spike to $92/bbl
   - Safe-haven flows: Gold +$40/oz, USD/CHF +85bps
   - VIX spiked to 22 (from 15 at month start)
"""

MOCK_PERFORMANCE = """
**Portfolio Performance Attribution - October 2025:**

**Total Return:** +3.2% (+$4.2M net)

**By Asset Class:**
- FX: +$2.1M (USD longs drove performance)
- Equities: +$1.5M (tactical shorts profitable)  
- Commodities: +$0.9M (gold position)
- Fixed Income: -$0.3M (rates volatility)

**Position-Level Detail:**

Top 3 Winners:
1. Long USD/JPY (148.50 → 151.20): +$1.8M
   - 3x levered, 20% of NAV exposure
   - Held for 28 days, max drawdown -0.8%
   
2. Short ES Futures (4520 → 4380): +$1.5M
   - Entered on earnings weakness signals
   - Closed 60% on Oct 25, held 40% into Nov
   
3. Long Gold (1920 → 1985): +$0.9M
   - Physical + futures combo
   - Geopolitical hedge thesis played out

Top 2 Losers:
1. Long EUR/USD (1.0650 → 1.0520): -$0.6M
   - ECB surprise cut invalidated thesis
   - Cut position 50% after -80bp move
   
2. Short 2Y UST (4.95% → 4.75% yield): -$0.4M
   - Flight to quality overwhelmed rate view
   - Exited on Oct 20 after regional bank stress
"""

MOCK_RISK_ANALYSIS = """
**Risk & Scenario Analysis - October 2025:**

**Current Portfolio Risk Metrics:**
- VaR (95%, 1-day): $850K
- Expected Shortfall: $1.2M
- Beta to S&P 500: -0.35 (hedged)
- USD exposure: +45% of NAV (concentrated)

**Scenario Probabilities:**

1. BASE CASE (60%)
   - Fed holds through Q1 2026
   - Gradual slowdown, no recession
   - USD strength continues (+2-3% over 3M)
   - Portfolio Impact: +$2-3M over next quarter
   - Action: Hold current book

2. UPSIDE - Soft Landing (25%)
   - Inflation falls to 2.5%, no hard landing
   - Equities rally +8%, USD weakens -3%
   - Portfolio Impact: -$1.5M (equity shorts hurt)
   - Action: Cut equity hedges 30%, rotate to cyclical FX

3. DOWNSIDE - Recession (15%)  
   - Fed cuts 100bps by June 2026
   - S&P falls -15%, credit spreads blow out
   - Portfolio Impact: +$5M (hedges pay off massively)
   - Action: Add equity shorts, close carry trades

**Risk Mitigation Recommendations:**
- Reduce USD concentration (trim JPY longs by 20%)
- Add tail hedges (OTM puts, 3M expiry)
- Diversify into EM FX (MXN, BRL) on pullbacks
- Monitor Fed speakers for pivot signals
"""

# Streamlit App
st.set_page_config(
    page_title="Portfolio Analysis RAG",
    page_icon="💼",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: 700;
        color: #1f77b4;
        margin-bottom: 0.5rem;
    }
    .sub-header {
        font-size: 1.2rem;
        color: #666;
        margin-bottom: 2rem;
    }
    .metric-container {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1rem;
        border-radius: 10px;
        color: white;
    }
    .stButton>button {
        width: 100%;
        background-color: #1f77b4;
        color: white;
        font-weight: 600;
        padding: 0.75rem;
        border-radius: 8px;
        border: none;
        font-size: 1.1rem;
    }
    .stButton>button:hover {
        background-color: #1557b0;
    }
</style>
""", unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.image("https://via.placeholder.com/300x80/1f77b4/white?text=Portfolio+RAG", use_container_width=True)
    
    st.markdown("### 📊 System Status")
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Indices", "3", delta="Active")
    with col2:
        st.metric("Documents", "247", delta="+12 this week")
    
    st.markdown("---")
    
    st.markdown("### 🗂️ Vector Stores")
    st.success("✅ Newsletters (86 docs)")
    st.success("✅ Market Context (124 docs)")
    st.success("✅ P&L Data (37 docs)")
    
    st.markdown("---")
    
    st.markdown("### ⚙️ Settings")
    retrieval_k = st.slider("Documents to retrieve", 5, 50, 30)
    
    model_choice = st.selectbox(
        "LLM Model",
        ["Claude Sonnet 4.5", "Gemini 2.5 Pro", "GPT-5"]
    )
    
    st.markdown("---")
    
    st.markdown("### 🔍 Analysis Type")
    analysis_mode = st.radio(
        "Select mode:",
        ["Full Newsletter", "Market Context Only", "Performance Only", "Risk Only"],
        help="Choose what type of analysis to generate"
    )

# Main content
st.markdown('<p class="main-header">💼 Portfolio Analysis RAG System</p>', unsafe_allow_html=True)
st.markdown('<p class="sub-header">AI-powered monthly newsletter generation for global macro hedge funds</p>', unsafe_allow_html=True)

# Tabs
tab1, tab2, tab3 = st.tabs(["📰 Generate Newsletter", "🤖 Multi-Agent View", "📚 Knowledge Base"])

with tab1:
    st.markdown("### Monthly Newsletter Generator")
    st.markdown("Generate comprehensive portfolio analysis by querying across newsletters, market context, and P&L data.")
    
    # Input section
    col1, col2 = st.columns([3, 1])
    
    with col1:
        month_select = st.selectbox(
            "Select Month",
            ["October 2025", "September 2025", "August 2025"],
            help="Choose the month to analyze"
        )
    
    with col2:
        st.markdown("##")  # Spacing
        generate_btn = st.button("🚀 Generate Analysis", type="primary", use_container_width=True)
    
    # Optional: Show/hide prompt
    with st.expander("📝 View Analysis Prompt"):
        st.code("""
You are an AI portfolio analyst for a discretionary global macro hedge fund.
Analyze October 2025 monthly performance data and produce a monthly newsletter.

Tasks:
1. Explain the core macro thesis underlying the portfolio
2. Identify top contributors and detractors to P&L
3. Link portfolio outcomes to macro drivers from the RAG context
4. Provide scenario analysis (base/upside/downside scenarios)
5. Highlight risks and opportunities
        """, language="text")
    
    if generate_btn:
        # Simulate processing
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        status_text.text("🔍 Retrieving documents from vector stores...")
        progress_bar.progress(20)
        time.sleep(0.8)
        
        status_text.text("📊 Analyzing market context...")
        progress_bar.progress(40)
        time.sleep(0.8)
        
        status_text.text("💰 Processing P&L attribution...")
        progress_bar.progress(60)
        time.sleep(0.8)
        
        status_text.text("⚠️ Running risk scenarios...")
        progress_bar.progress(80)
        time.sleep(0.8)
        
        status_text.text("✍️ Generating newsletter...")
        progress_bar.progress(100)
        time.sleep(0.5)
        
        status_text.empty()
        progress_bar.empty()
        
        # Success message
        st.success(f"✅ Newsletter generated successfully! Retrieved {retrieval_k} documents, analyzed with {model_choice}")
        
        # Display based on mode
        if analysis_mode == "Full Newsletter":
            st.markdown("---")
            st.markdown(MOCK_NEWSLETTER)
            
        elif analysis_mode == "Market Context Only":
            st.markdown("---")
            st.markdown("### 🌍 Market Context Analysis")
            st.markdown(MOCK_MARKET_CONTEXT)
            
        elif analysis_mode == "Performance Only":
            st.markdown("---")
            st.markdown("### 📊 Portfolio Performance Analysis")
            st.markdown(MOCK_PERFORMANCE)
            
        elif analysis_mode == "Risk Only":
            st.markdown("---")
            st.markdown("### ⚠️ Risk & Scenario Analysis")
            st.markdown(MOCK_RISK_ANALYSIS)
        
        # Sources section (collapsible)
        with st.expander("🔍 View Retrieved Sources"):
            st.markdown(f"**{len(MOCK_SOURCES)} documents used for this analysis:**")
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("**📰 Newsletters:**")
                for src in MOCK_SOURCES[:3]:
                    st.markdown(f"- `{src}`")
                
                st.markdown("**📊 P&L Data:**")
                for src in MOCK_SOURCES[7:]:
                    st.markdown(f"- `{src}`")
            
            with col2:
                st.markdown("**🌍 Market Context:**")
                for src in MOCK_SOURCES[3:7]:
                    st.markdown(f"- `{src}`")
        
        # Download button
        st.download_button(
            label="📥 Download Newsletter",
            data=MOCK_NEWSLETTER,
            file_name=f"newsletter_{month_select.replace(' ', '_').lower()}.md",
            mime="text/markdown"
        )

with tab2:
    st.markdown("### 🤖 Multi-Agent Analysis Pipeline")
    st.markdown("View how different specialized agents contribute to the final newsletter")
    
    if st.button("▶️ Run Multi-Agent Analysis", type="primary"):
        # Agent 1: Market Context
        with st.status("**Agent 1:** Market Context Analyzer", expanded=True) as status:
            st.write("Querying macro context documents...")
            time.sleep(1)
            st.write("✅ Retrieved 45 relevant documents")
            st.write("✅ Identified 8 key market drivers")
            time.sleep(0.5)
            status.update(label="✅ Market Context Agent - Complete", state="complete")
        
        with st.expander("📊 Market Context Output"):
            st.markdown(MOCK_MARKET_CONTEXT)
        
        # Agent 2: Performance
        with st.status("**Agent 2:** Portfolio Performance Analyzer", expanded=True) as status:
            st.write("Analyzing P&L data...")
            time.sleep(1)
            st.write("✅ Processed 37 trade records")
            st.write("✅ Attributed +$4.2M net P&L")
            time.sleep(0.5)
            status.update(label="✅ Performance Agent - Complete", state="complete")
        
        with st.expander("💰 Performance Output"):
            st.markdown(MOCK_PERFORMANCE)
        
        # Agent 3: Risk
        with st.status("**Agent 3:** Risk Analyst", expanded=True) as status:
            st.write("Running scenario analysis...")
            time.sleep(1)
            st.write("✅ Modeled 3 scenarios")
            st.write("✅ Calculated risk metrics")
            time.sleep(0.5)
            status.update(label="✅ Risk Agent - Complete", state="complete")
        
        with st.expander("⚠️ Risk Analysis Output"):
            st.markdown(MOCK_RISK_ANALYSIS)
        
        # Agent 4: Writer
        with st.status("**Agent 4:** Newsletter Writer", expanded=True) as status:
            st.write("Synthesizing all agent outputs...")
            time.sleep(1)
            st.write("✅ Referenced 3 example newsletters")
            st.write("✅ Composed final narrative")
            time.sleep(0.5)
            status.update(label="✅ Writer Agent - Complete", state="complete")
        
        st.success("🎉 All agents complete! Final newsletter generated.")
        
        with st.expander("📰 Final Newsletter"):
            st.markdown(MOCK_NEWSLETTER)

with tab3:
    st.markdown("### 📚 Knowledge Base Overview")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Total Documents", "247", delta="+12 this week")
        st.metric("Total Chunks", "3,421", delta="+156")
    
    with col2:
        st.metric("Avg Chunk Size", "842 chars")
        st.metric("Embedding Model", "text-embedding-3-large")
    
    with col3:
        st.metric("Index Size", "124 MB")
        st.metric("Last Updated", "2 hours ago")
    
    st.markdown("---")
    
    st.markdown("#### 📂 Document Breakdown")
    
    chart_data = {
        "Category": ["Newsletters", "Market Context", "P&L Data"],
        "Documents": [86, 124, 37],
        "Chunks": [1205, 1847, 369]
    }
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.bar_chart(chart_data, x="Category", y="Documents")
    
    with col2:
        st.bar_chart(chart_data, x="Category", y="Chunks")
    
    st.markdown("---")
    
    # Sample documents
    st.markdown("#### 📄 Recent Documents")
    
    recent_docs = [
        {"Name": "october_pnl_attribution.csv", "Type": "P&L", "Date": "2025-11-01", "Size": "24 KB"},
        {"Name": "fed_minutes_oct_2025.pdf", "Type": "Context", "Date": "2025-10-30", "Size": "156 KB"},
        {"Name": "macro_daily_oct31.pdf", "Type": "Context", "Date": "2025-10-31", "Size": "89 KB"},
        {"Name": "2025_09_monthly.pdf", "Type": "Newsletter", "Date": "2025-10-01", "Size": "234 KB"},
    ]
    
    st.dataframe(recent_docs, use_container_width=True, hide_index=True)

# Footer
st.markdown("---")
col1, col2, col3 = st.columns(3)

with col1:
    st.metric("RAG Retrieval", f"{retrieval_k} docs")

with col2:
    st.metric("LLM Model", model_choice)

with col3:
    st.metric("Avg Response Time", "4.2s")

st.caption("Powered by LangChain + FAISS + Claude/Gemini • Last updated: November 1, 2025")