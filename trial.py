# app.py
import streamlit as st
import time
from datetime import datetime

# Mock data - includes your actual October example
MOCK_NEWSLETTER_OCT = """
## **Monthly Performance Review - October 2025**

**TO:** Portfolio Managers  
**FROM:** AI Portfolio Analyst  
**DATE:** November 5, 2025  
**SUBJECT:** Performance Analysis for October 2025

---

### **1. Core Macro Thesis & Positioning**

The portfolio's positioning in October reflected a complex macro view, primarily centered on a **stagflationary thesis**. This outlook anticipates persistent inflation combined with slowing economic growth.

*   **Pro-Inflationary / Reflationary Stance:** This was expressed through long notional positions across the commodities complex, including industrial metals (Copper), precious metals (Platinum, Silver), and energy (Oil). Long positions in Uranium Miners (CCJ) and Treasury Inflation-Protected Securities (TIPS) further supported this view, betting on rising inflation expectations and the continued importance of energy security.
*   **Dovish / Recessionary Stance:** A significant long duration position in the front-end and belly of the U.S. Treasury curve (USGG5YR Index) was structured to profit from falling interest rates, likely in anticipation of a Federal Reserve pivot or a flight-to-safety bid driven by weakening economic data. This was complemented by a short position in S&P 500 futures (ESA index), positioned for an equity market downturn.
*   **FX & Thematic Views:** The book carried specific relative value and directional bets in foreign exchange, notably a large short position in CHFJPY and long positions in USDCNH and USDHKD. A long position in a spot Bitcoin ETF (IBIT) was maintained as a thematic allocation to digital assets.

The expected outcome was to capture upside from inflation-sensitive assets while hedging against a growth slowdown through long duration and short equity positions. However, the performance in October revealed a divergence in these themes, where falling rates boosted risk assets, creating a headwind for the equity hedge.

### **2. October 2025 Performance Summary**

October was a challenging month, with significant gains in the rates and commodities books being more than offset by substantial losses in FX and equities. The portfolio recorded a **net loss of -$1,881,152**.

| Top Contributors | Ticker | P&L (USD) | Top Detractors | Ticker | P&L (USD) |
| :--- | :--- | ---: | :--- | :--- | ---: |
| 1. Platinum | PLA comdty | 4,329,859 | 1. Short CHFJPY | CHFJPY curncy | -5,713,897 |
| 2. Rates (Front/Belly) | USGG5YR Index | 2,057,500 | 2. Long USDCNH | USDCNH curncy | -2,456,135 |
| 3. Uranium Miners | CCJ Equity | 1,445,806 | 3. Short SPX | ESA index | -1,429,828 |

### **3. Detailed Attribution Analysis**

---

#### **Top Contributors**

**1. Long Platinum (PLA comdty): +$4,329,859**  
The long notional position in Platinum was the month's best performer, indicating a sharp price rally.

*   **Event / Data Point:** A significant price increase in platinum is typically driven by a combination of factors such as positive industrial demand data (e.g., global auto sales), supply constraints from key producers, or broad-based US dollar weakness that lifts the entire commodities complex.
*   **Market Impact:** These drivers would have led to increased demand for platinum as both an industrial component and a precious metal, causing futures prices to appreciate significantly.
*   **Portfolio Linkage:** The portfolio's long exposure directly captured this upward price movement, generating a substantial gain that validated the pro-inflation/industrial demand component of the core thesis.

**2. Long Rates (Front/Belly) (USGG5YR Index): +$2,057,500**  
The long duration position, measured in DV01, profited from a fall in U.S. Treasury yields.

*   **Event / Data Point:** A rally in bonds (and corresponding fall in yields) is typically precipitated by weaker-than-expected economic data (e.g., CPI, Non-Farm Payrolls, ISM surveys) or dovish commentary from Federal Reserve officials, leading markets to price in a less aggressive path for monetary policy.
*   **Market Impact:** Such events would have fueled a bond market rally, pushing yields on the 5-year Treasury note lower.
*   **Portfolio Linkage:** The portfolio's long DV01 position in the USGG5YR Index benefited directly from the decrease in interest rates, confirming the dovish/recessionary part of the thesis.

**3. Uranium Miners (CCJ Equity): +$1,445,806**  
Long position in Cameco Corporation benefited from sector strength.

*   **Event / Data Point:** Uranium miner rallies are typically driven by nuclear energy policy announcements, supply constraints, or increased institutional interest in clean energy infrastructure.
*   **Market Impact:** Positive sentiment around nuclear energy and uranium supply dynamics drove the stock higher.
*   **Portfolio Linkage:** The position captured the ongoing energy transition theme and uranium supply/demand imbalance.

---

#### **Top Detractors**

**1. Short CHFJPY (CHFJPY curncy): -$5,713,897**  
The short notional position in the Swiss Franc vs. the Japanese Yen was the largest detractor, indicating the CHFJPY cross-rate rallied sharply.

*   **Event / Data Point:** A strong rally in CHFJPY suggests a significant "risk-off" event where the Swiss Franc's safe-haven appeal outstripped the Yen's, or a major policy divergence between the Swiss National Bank (SNB) and the Bank of Japan (BoJ), such as a hawkish turn from the SNB.
*   **Market Impact:** A risk-off catalyst or hawkish SNB action would drive capital flows into the Franc, causing it to strengthen materially against the Yen and pushing the CHFJPY exchange rate higher.
*   **Portfolio Linkage:** The fund's short position was positioned for CHF to weaken against JPY. The powerful move in the opposite direction resulted in a severe mark-to-market loss, highlighting a significant misreading of cross-currency dynamics or risk sentiment during the month.

**2. Long USDCNH (USDCNH curncy): -$2,456,135**  
The long position in the US Dollar vs. the offshore Chinese Yuan suffered a large loss, meaning the USD weakened against the CNH.

*   **Event / Data Point:** A fall in the USDCNH rate is often driven by signs of economic stabilization in China, forceful policy support from Beijing, or broad-based US Dollar weakness stemming from the same dovish Fed expectations that benefited the fund's rates positions.
*   **Market Impact:** Evidence of a resilient Chinese economy or a weaker dollar would increase investor demand for the Yuan, causing the USDCNH rate to fall.
*   **Portfolio Linkage:** The position was a bet on continued Yuan weakness or Dollar strength. The reversal of this trend during October led to a significant loss.

**3. Short S&P 500 (ESA index): -$1,429,828**  
The short equity position was a key detractor as the S&P 500 index evidently rallied in October.

*   **Event / Data Point:** The same fall in bond yields that drove gains in the portfolio's rates book likely fueled the equity rally. Lower yields increase the present value of future earnings and often signal to markets that financial conditions are easing, boosting risk appetite.
*   **Market Impact:** A lower discount rate and improved sentiment would have driven equity indices like the S&P 500 higher.
*   **Portfolio Linkage:** The short S&P 500 position, acting as a hedge against a growth slowdown, incurred losses as risk assets rallied. This outcome reveals a key conflict within the portfolio: the thesis for lower rates was correct, but its second-order effect was to stimulate the equity market, working directly against the short SPX position.

### **4. Risk Analysis & Scenario Planning**

**Current Portfolio Risk Metrics:**
- Net Loss: -$1,881,152 (-1.88% of NAV)
- Max Drawdown: -5.7% (driven by CHFJPY position)
- Correlation to S&P 500: -0.42 (inverse correlation from short position)
- FX Concentration Risk: 43% of losses from FX book

**Scenario Analysis:**

**BASE CASE (55% probability):**
- Fed continues gradual easing cycle
- Commodities remain supported by supply constraints
- USD ranges with slight weakness bias
- **Portfolio Impact:** Commodities and rates continue to perform; need to resize FX book
- **Recommended Actions:** Trim CHFJPY short by 50%, reduce USDCNH long by 30%

**UPSIDE - Reflation Accelerates (30% probability):**
- Inflation re-accelerates above 3%
- Fed pauses cuts, rates stabilize higher
- Commodities rally extends, equities weaken
- **Portfolio Impact:** +$3-4M (commodities surge, short SPX profitable)
- **Recommended Actions:** Add to precious metals, maintain equity hedge

**DOWNSIDE - Hard Landing (15% probability):**
- Recession triggers aggressive Fed cuts (150bps+)
- Flight to quality: USD, JPY, CHF strengthen
- Commodities sell off, equities crater
- **Portfolio Impact:** -$2-3M (FX losses accelerate, commodities give back gains)
- **Recommended Actions:** Close FX positions immediately, increase equity shorts, rotate to long gold

### **5. Key Risks & Tactical Recommendations**

**High-Risk Areas:**
1. **Internal Hedging Conflict:** The primary driver of gains in the rates book (falling yields) was also a primary driver of losses in the short equity book. This suggests the negative correlation between bonds and equities, which is central to many hedging strategies, did not hold. The portfolio should review whether the short SPX position is an effective hedge in the current macro regime.

2. **FX Sizing and Thesis:** The substantial loss in the short CHFJPY position warrants an immediate review. The conviction and sizing of this trade were not commensurate with the outcome, suggesting the underlying thesis may be flawed or exposed to unforeseen tail risks.

3. **Dollar View Inconsistency:** The portfolio benefited from falling US rates but lost money on a weaker USD (via USDCNH). This indicates a need to refine the house view on the US dollar and ensure positioning is consistent across asset classes.

**High-Return Opportunities:**
1. **Commodities Complex:** Platinum, Oil, and Uranium positions continue to show strong technical and fundamental support. Consider adding to these positions on pullbacks.

2. **Rates Positioning:** The long duration call proved correct. Consider extending duration further into the 10Y if economic data continues to soften.

3. **Bitcoin/Digital Assets:** IBIT position remains constructive as institutional adoption continues. Monitor for add opportunities.

**Tactical Actions:**
- **Immediate:** Cut CHFJPY short position by 50% to reduce tail risk
- **Near-term:** Reduce USDCNH long by 30%, reassess USD thesis across book
- **Strategic:** Review correlation assumptions between rates and equities; consider restructuring equity hedge
- **Opportunistic:** Add to Platinum and Oil on any 5%+ pullback

---

**Conclusion:**  
October's -1.88% loss highlights critical portfolio construction issues despite correct macro calls in rates and commodities. The FX book requires urgent attention, and the equity hedge effectiveness must be reassessed. Moving forward, resolving internal conflicts and refining conviction levels in detractor positions—particularly FX—will be essential to improving risk-adjusted returns.
"""

MOCK_SOURCES = [
    "newsletters/2025_03_monthly.pdf",
    "newsletters/2025_04_monthly.pdf", 
    "newsletters/2025_05_monthly.pdf",
    "context/fed_minutes_oct_2025.pdf",
    "context/ecb_press_conference_oct18.pdf",
    "context/macro_daily_oct01_oct31.pdf",
    "context/china_stimulus_announcement.pdf",
    "context/snb_policy_statement_oct.pdf",
    "context/uranium_sector_report_oct.pdf",
    "pnl/october_pnl_attribution.csv",
    "pnl/trade_log_oct_2025.md",
    "pnl/position_snapshot_oct31.csv",
    "pnl/fx_position_details.xlsx",
    "pnl/commodities_breakdown.xlsx"
]

MOCK_MARKET_CONTEXT = """
**Key Market Drivers - October 2025:**

1. **Federal Reserve Policy** (Oct 18 FOMC)
   - Held rates at 5.25-5.50% as expected
   - Minutes revealed growing dovish dissent among members
   - Powell emphasized "data dependence" but acknowledged cooling inflation
   - Impact: 10Y yields rallied 15bps, 5Y yields fell 12bps, USD weakened vs. EUR/JPY/CNH

2. **Swiss National Bank Surprise** (Oct 10 SNB Meeting)
   - Unexpected hawkish statement on inflation concerns
   - Signaled potential rate hike if CHF weakens further
   - Impact: CHF strengthened sharply across all pairs, CHFJPY rallied 2.8%

3. **China Economic Stabilization** (Oct 8-15)
   - Better-than-expected PMI data (50.2 vs 49.5 forecast)
   - PBOC announced targeted stimulus for manufacturing sector
   - Impact: CNH strengthened 1.9% vs USD, commodity demand outlook improved

4. **Commodities Rally** (Throughout October)
   - Platinum: Global auto sales beat expectations, supply disruptions in South Africa
   - Uranium: Major utility signed 10-year supply contracts, nuclear policy support in EU/Asia
   - Oil: OPEC+ production discipline, geopolitical premium from Middle East
   - Impact: Broad commodities complex up 4-7%

5. **Equity Market Rally** (Oct 20-31)
   - Lower bond yields fueled multiple expansion
   - Tech earnings exceeded expectations
   - S&P 500 rallied 3.2% despite recession concerns
   - Impact: Risk-on sentiment, growth stocks outperformed
"""

MOCK_PERFORMANCE = """
**Portfolio Performance Attribution - October 2025:**

**Total Return:** -1.88% (-$1,881,152)

**By Asset Class:**
- Commodities: +$6.1M (Platinum, Uranium, Oil all strong)
- Rates: +$2.1M (Long duration profitable on Fed dovish pivot)
- Equities: -$1.4M (Short SPX hurt by equity rally)
- FX: -$8.2M (CHFJPY and USDCNH major losses)
- Other: -$0.4M (Bitcoin flat, TIPS modest gains)

**Position-Level Detail:**

**Top 3 Winners:**

1. **Long Platinum (PLA comdty): +$4,329,859**
   - Entry: $980/oz (June 2025)
   - Current: $1,065/oz (+8.7%)
   - Notional: ~$50M exposure
   - Drivers: Auto demand recovery + South African supply disruptions
   - Max drawdown during hold: -3.2%

2. **Long Rates 5Y (USGG5YR Index): +$2,057,500**
   - Duration: +$850K DV01 
   - Yield move: 4.15% → 4.03% (-12bps)
   - Entry: Early September on economic weakness thesis
   - Drivers: Dovish Fed, weaker employment data, flight-to-safety

3. **Long Uranium Miners (CCJ Equity): +$1,445,806**
   - Entry: $42.50 (August 2025)
   - Current: $51.20 (+20.5%)
   - Position size: 65K shares (~$3.3M)
   - Drivers: Utility contracts, EU nuclear policy support, uranium spot price +12%

**Top 3 Losers:**

1. **Short CHFJPY (CHFJPY curncy): -$5,713,897**
   - Entry: 168.50 (September 2025)
   - Exit/Mark: 173.20 (+2.8% against position)
   - Notional: $200M short
   - Thesis: Expected BoJ policy normalization to strengthen JPY vs CHF
   - What happened: SNB hawkish surprise + risk-off drove CHF surge
   - Position still held: 50% (cut 50% at 172.00)

2. **Long USDCNH (USDCNH curncy): -$2,456,135**
   - Entry: 7.28 (early October)
   - Current: 7.14 (-1.9%)
   - Notional: $130M long
   - Thesis: Expected China slowdown + Fed hawkish hold to support USD
   - What happened: China data stabilized, Fed turned dovish, USD weakened broadly
   - Position reduced: Trimmed from $150M to $100M

3. **Short S&P 500 (ESA Index): -$1,429,828**
   - Entry: 4,520 (Oct 12)
   - Current: 4,665 (+3.2%)
   - Notional: ~$45M short via futures
   - Thesis: Recession hedge, overvalued equities
   - What happened: Lower rates fueled equity rally, tech earnings strong
   - Hedge conflict: Rates position drove equity gains (negative correlation broke)

**Other Notable Positions:**
- Long Oil (WTI): +$892K (geopolitical premium)
- Long Silver: +$645K (industrial demand)
- Long TIPS: +$380K (inflation breakevens widened)
- Long Bitcoin ETF (IBIT): -$125K (crypto sideways, slight fees drag)
"""

MOCK_RISK_ANALYSIS = """
**Risk & Scenario Analysis - October 2025:**

**Current Portfolio Risk Metrics:**
- Net Loss: -$1,881,152 (-1.88% NAV)
- Max Drawdown (MTD): -5.7% (occurred Oct 10 on CHFJPY spike)
- Sharpe Ratio (YTD): 0.42 (down from 0.68 in September)
- Beta to S&P 500: -0.42 (negative correlation from short)
- FX Book Contribution to Loss: 43% of total losses

**Concentration Analysis:**
- Single largest position risk: CHFJPY short ($100M remaining notional)
- Top 5 positions: 62% of gross exposure
- Commodities concentration: 38% of NAV (diversified across metals/energy)
- Duration risk: +$850K DV01 (moderate)

**Correlation Breakdown (October):**
- Bonds vs Equities: +0.65 (historically -0.3) ⚠️ **RISK SIGNAL**
- USD vs Commodities: -0.45 (expected)
- CHF vs Safe Havens: +0.82 (CHF behaving as premier safe haven)

---

**Scenario Probabilities & Portfolio Impact:**

**1. BASE CASE - Muddle Through (55%)**

**Outlook:**
- Fed cuts 25bps in Dec, pauses in Q1 2026
- Inflation stabilizes 2.5-3.0%, no hard landing
- Commodities supported by supply constraints but moderate demand
- USD ranges with modest weakness bias
- S&P 500 in 4,400-4,800 range (volatility persists)

**Portfolio Impact:** 
- Next 3 months P&L: +$1.5M to +$2.5M
- Commodities: Modest gains (+$500K)
- Rates: Small gains if Fed cuts materialize (+$300K)
- Equities: Short position roughly flat (±$200K)
- FX: Reduced risk after cuts, small gains if USD weakens (+$400K)

**Recommended Actions:**
- Maintain commodity positions, trim on 5%+ rallies
- Hold rates duration, add on 5Y yield >4.2%
- **Critical:** Reduce CHFJPY short to $50M (currently $100M)
- Cut USDCNH long to $70M (currently $100M)
- Keep equity hedge at current size but monitor correlation

---

**2. UPSIDE - Reflation / No Landing (30%)**

**Outlook:**
- Inflation re-accelerates to 3.5%+ (wage growth, oil spike)
- Fed forced to hold rates longer or even hike
- Commodities surge on supply constraints + demand resilience
- Risk assets weaken (equities down 8-12%)
- USD strengthens as Fed becomes most hawkish G10 central bank

**Portfolio Impact:**
- Next 3 months P&L: +$4M to +$6M
- Commodities: Major gains (+$3M) - Platinum, Oil, Uranium all rally
- Rates: Losses on duration (-$1M) as yields rise
- Equities: Short SPX profitable (+$2M)
- FX: Mixed - USDCNH profitable but CHFJPY still problematic

**Recommended Actions:**
- **Add** to commodities on any pullback (target +20% exposure)
- Consider trimming rates duration to $600K DV01
- Maintain or slightly increase equity short
- **Still reduce** CHFJPY - even in risk-off, CHF can outperform
- Let USDCNH run in this scenario (USD strength thesis plays out)

---

**3. DOWNSIDE - Hard Landing / Recession (15%)**

**Outlook:**
- Major economic deterioration (unemployment spikes to 5%+)
- Fed emergency cuts (150-200bps in 6 months)
- Flight to quality: Bonds, USD, JPY, CHF all surge
- Commodities sell off hard (-15-25%) on demand destruction
- S&P 500 down 20%+, credit spreads blow out

**Portfolio Impact:**
- Next 3 months P&L: -$2M to -$4M
- Commodities: Severe losses (-$4M) - demand destruction
- Rates: Major gains (+$3M) - yields collapse
- Equities: Short SPX very profitable (+$3M)
- FX: **Catastrophic losses** (-$4M+) - CHF and JPY both surge, CHFJPY rallies violently

**Recommended Actions:**
- **IMMEDIATE:** Exit CHFJPY short entirely (this is a tail risk position)
- Close USDCNH long (flight to safety hurts USD vs safe havens)
- Add to rates duration to $1.2M DV01
- Increase equity short by 30%
- Rotate commodities to gold only (close industrial metals)
- This scenario validates urgent FX book restructuring

---

**Risk Mitigation - Priority Actions:**

**Critical (Do Immediately):**
1. **CHFJPY Short:** Reduce to $50M max (from $100M current)
   - Rationale: Tail risk in recession scenario is unacceptable
   - This position has cost -$5.7M and remains dangerous
   - SNB unpredictability + CHF safe-haven status = high risk

2. **USDCNH Long:** Reduce to $70M (from $100M)
   - Rationale: Thesis not playing out, USD weakness is broader trend
   - China stabilization narrative gaining traction
   - Cut loss, reassess in 30 days

**Important (Next 2 Weeks):**
3. **Equity Hedge Review:** Analyze correlation breakdown
   - Problem: Rates rally driving equity rally (negative correlation failed)
   - Consider: Put spreads instead of outright short? Or accept hedge will hurt in easing cycle?
   - Decision needed: Is this a hedge or a directional bet?

4. **Dollar Thesis Alignment:** Reconcile USD view across portfolio
   - Currently: Long duration (implies weak USD) + Long USDCNH (implies strong USD)
   - Pick a side: Is USD in structural decline or not?

**Opportunistic (Monitor):**
5. **Commodities Additions:** Build shopping list for pullbacks
   - Platinum: Add 20% on 3%+ dip (target $1,020/oz entry)
   - Uranium: Add to CCJ on pullback to $48 (strong fundamentals)
   - Oil: Watch geopolitical developments, add on $85/bbl

6. **Rates Extension:** Consider 10Y duration if growth slows further
   - Currently focused on 5Y, could extend curve
   - Wait for 10Y yield >4.4% to add

---

**High-Risk Areas (Red Flags):**

1. **FX Book Construction** ⚠️⚠️⚠️
   - Lost $8.2M in one month (43% of total loss)
   - CHFJPY short is uninvestable in current form (max pain in all scenarios except base)
   - Need complete re-evaluation of FX strategy and sizing

2. **Correlation Assumptions** ⚠️⚠️
   - Bonds/Equities correlation broke down (+0.65 vs historical -0.3)
   - Equity hedge didn't work when rates rallied
   - May indicate new regime where both rally on Fed dovishness

3. **Concentration in Commodities** ⚠️
   - 38% NAV in commodities (diversified but still large)
   - Vulnerable to demand shock in recession scenario
   - Mitigant: Stop losses at -15% from current levels

**High-Return Opportunities (Green Lights):**

1. **Commodities Structural Bull** ✅✅
   - Platinum, Uranium showing strong fundamentals
   - Supply constraints are real, demand resilient
   - Opportunity: Add on weakness, extend timeline

2. **Rates Duration** ✅✅
   - Thesis validated (+$2M in Oct)
   - Fed pivoting dovish, data softening
   - Opportunity: Extend to 10Y, increase DV01 to $1M+

3. **Energy Transition Plays** ✅
   - Uranium miners (CCJ) continue to perform
   - Nuclear renaissance underway (policy support)
   - Opportunity: Add to uranium miners, consider adding lithium/copper

---

**Summary:**
October revealed that the macro thesis (stagflation, dovish Fed) was directionally correct but portfolio construction was flawed. FX book requires immediate restructuring (particularly CHFJPY), equity hedge effectiveness must be reassessed, and USD view needs alignment across positions. Commodities and rates remain compelling opportunities.
"""

BUILT_IN_INSTRUCTIONS = """
You are an AI portfolio analyst for a discretionary global macro hedge fund.
Your goal is to analyze monthly performance data, interpret market drivers, 
and produce a clear, insightful report for portfolio managers.

You have access to:
- Monthly portfolio P&L attribution table
- RAG layer containing daily macro commentaries (updates on macro markets by country, 
  important news, data releases and events that drove market movements, risk sentiment 
  and macro trends)
- Sample commentaries for tone and style reference
- Weekly market data

You must:
- Produce structured, evidence-based analysis
- Use concise, professional financial language
- Link each portfolio outcome to macro context drawn from your knowledge base
- Highlight both qualitative insight and quantitative attribution

Tasks:
1. Explain the core macro thesis underlying the portfolio, trade expressions and expected outcomes
2. Identify and rank the top contributors and detractors to portfolio P&L for the month
3. For the top contributors and detractors, identify the macro drivers behind their performance
4. Extract relevant daily commentary and summarize each driver as:
   • Event / Data Point (e.g., "CPI release", "FOMC minutes")
   • Market Impact: how it influenced rates, FX, equities, or commodities
   • Portfolio Linkage: which positions were affected and how
5. Scenario analysis: Base, Upside (risk-on), Downside (risk-off)
   • For each scenario: Probability (with %), effect on key positions, 
     recommended tactical actions (size/hedge/close)
6. Predict or point out high risk areas and explain why, give suggestions for mitigation
7. Identify high return opportunities and explain why
"""

# Streamlit App
st.set_page_config(
    page_title="P&L Analysis RAG",
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
    st.image("https://via.placeholder.com/300x80/1f77b4/white?text=P%26L+RAG", use_container_width=True)
    
    st.markdown("### 📊 System Status")
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Indices", "0", delta="Ready")
    with col2:
        st.metric("Documents", "0", delta="Add files below")
    
    st.markdown("---")
    
    st.markdown("### 📁 Upload Documents")
    
    # File uploader for PDFs
    uploaded_pdfs = st.file_uploader(
        "Upload PDFs",
        type=['pdf'],
        accept_multiple_files=True,
        help="Upload P&L reports, newsletters, or market commentary PDFs"
    )
    
    if uploaded_pdfs:
        st.success(f"✅ {len(uploaded_pdfs)} PDF(s) uploaded")
        for pdf in uploaded_pdfs:
            st.caption(f"📄 {pdf.name}")
    
    # File uploader for Excel
    uploaded_excel = st.file_uploader(
        "Upload Excel Files",
        type=['xlsx', 'xls'],
        accept_multiple_files=True,
        help="Upload P&L data, trade logs, or attribution tables"
    )
    
    if uploaded_excel:
        st.success(f"✅ {len(uploaded_excel)} Excel file(s) uploaded")
        for excel in uploaded_excel:
            st.caption(f"📊 {excel.name}")
    
    # File uploader for Word docs
    uploaded_docs = st.file_uploader(
        "Upload Word Documents",
        type=['docx', 'doc'],
        accept_multiple_files=True,
        help="Upload market analysis reports or commentary documents"
    )
    
    if uploaded_docs:
        st.success(f"✅ {len(uploaded_docs)} Word doc(s) uploaded")
        for doc in uploaded_docs:
            st.caption(f"📝 {doc.name}")
    
    # Process button
    total_files = len(uploaded_pdfs or []) + len(uploaded_excel or []) + len(uploaded_docs or [])
    if total_files > 0:
        if st.button("⚡ Process All Files", type="primary"):
            with st.spinner("Processing documents..."):
                progress = st.progress(0)
                for i in range(100):
                    time.sleep(0.01)
                    progress.progress(i + 1)
                st.success(f"✅ Processed {total_files} file(s)!")
                st.balloons()
    
    st.markdown("---")
    
    st.markdown("### 🗂️ Vector Stores")
    st.info("⚪ Newsletters (0 docs)")
    st.info("⚪ Market Context (0 docs)")
    st.info("⚪ P&L Data (0 docs)")
    
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
st.markdown('<p class="main-header">💼 Profit and Loss Analysis RAG System</p>', unsafe_allow_html=True)

# Tabs
tab1, tab2, tab3 = st.tabs(["📰 Generate Newsletter", "🤖 Multi-Agent View", "📚 Knowledge Base"])

with tab1:
    st.markdown("### Monthly Newsletter Generator")
    
    # User prompt input
    st.markdown("#### Your Analysis Query")
    user_prompt = st.text_area(
        "Enter your analysis request:",
        placeholder="Example: Analyze October 2025 performance and explain the drivers behind our top positions. Focus on the FX book losses and provide tactical recommendations...",
        height=150,
        help="Describe what you want to analyze. The system will use your uploaded documents and the built-in instructions."
    )
    
    # Month selector and generate button
    col1, col2 = st.columns([3, 1])
    
    with col1:
        month_select = st.selectbox(
            "Select Month",
            ["October 2025", "September 2025", "August 2025"],
            help="Choose the month to analyze"
        )
    
    with col2:
        st.markdown("##")  # Spacing
        generate_btn = st.button("🚀 Generate Analysis", type="primary", use_container_width=True, disabled=(not user_prompt))
    
    # Show built-in instructions (collapsed by default)
    with st.expander("📋 View Built-in Analysis Instructions"):
        st.code(BUILT_IN_INSTRUCTIONS, language="text")
    
    if generate_btn and user_prompt:
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
        
        # Show user's prompt
        with st.expander("📝 Your Query"):
            st.info(user_prompt)
        
        # Display based on mode
        if analysis_mode == "Full Newsletter":
            st.markdown("---")
            st.markdown(MOCK_NEWSLETTER_OCT)
            
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
                for src in MOCK_SOURCES[9:]:
                    st.markdown(f"- `{src}`")
            
            with col2:
                st.markdown("**🌍 Market Context:**")
                for src in MOCK_SOURCES[3:9]:
                    st.markdown(f"- `{src}`")
        
        # Download button
        st.download_button(
            label="📥 Download Newsletter",
            data=MOCK_NEWSLETTER_OCT,
            file_name=f"newsletter_{month_select.replace(' ', '_').lower()}.md",
            mime="text/markdown"
        )
    
    elif generate_btn and not user_prompt:
        st.warning("⚠️ Please enter an analysis query before generating.")

with tab2:
    st.markdown("### 🤖 Multi-Agent Analysis Pipeline")
    st.markdown("View how different specialized agents contribute to the final newsletter")
    
    # User prompt for multi-agent
    agent_prompt = st.text_area(
        "Enter your analysis request for multi-agent processing:",
        placeholder="Example: Generate a comprehensive October 2025 analysis focusing on the FX losses and internal portfolio conflicts...",
        height=120,
        key="agent_prompt"
    )
    
    if st.button("▶️ Run Multi-Agent Analysis", type="primary", disabled=(not agent_prompt)):
        # Show user's prompt
        with st.expander("📝 Your Query"):
            st.info(agent_prompt)
        
        # Agent 1: Market Context
        with st.status("**Agent 1:** Market Context Analyzer", expanded=True) as status:
            st.write("Querying macro context documents...")
            time.sleep(1)
            st.write("✅ Retrieved 38 relevant documents")
            st.write("✅ Identified 6 key market drivers (Fed, SNB, China, Commodities)")
            time.sleep(0.5)
            status.update(label="✅ Market Context Agent - Complete", state="complete")
        
        with st.expander("📊 Market Context Output"):
            st.markdown(MOCK_MARKET_CONTEXT)
        
        # Agent 2: Performance
        with st.status("**Agent 2:** Portfolio Performance Analyzer", expanded=True) as status:
            st.write("Analyzing P&L data...")
            time.sleep(1)
            st.write("✅ Processed 42 trade records")
            st.write("✅ Attributed -$1,881,152 net P&L")
            st.write("✅ Identified critical FX book issues")
            time.sleep(0.5)
            status.update(label="✅ Performance Agent - Complete", state="complete")
        
        with st.expander("💰 Performance Output"):
            st.markdown(MOCK_PERFORMANCE)
        
        # Agent 3: Risk
        with st.status("**Agent 3:** Risk Analyst", expanded=True) as status:
            st.write("Running scenario analysis...")
            time.sleep(1)
            st.write("✅ Modeled 3 scenarios with probabilities")
            st.write("✅ Identified critical tail risks in FX book")
            st.write("✅ Calculated portfolio correlation breakdown")
            time.sleep(0.5)
            status.update(label="✅ Risk Agent - Complete", state="complete")
        
        with st.expander("⚠️ Risk Analysis Output"):
            st.markdown(MOCK_RISK_ANALYSIS)
        
        # Agent 4: Writer
        with st.status("**Agent 4:** Newsletter Writer", expanded=True) as status:
            st.write("Synthesizing all agent outputs...")
            time.sleep(1)
            st.write("✅ Referenced 3 example newsletters for style")
            st.write("✅ Integrated market context with P&L attribution")
            st.write("✅ Composed final narrative with tactical recommendations")
            time.sleep(0.5)
            status.update(label="✅ Writer Agent - Complete", state="complete")
        
        st.success("🎉 All agents complete! Final newsletter generated.")
        
        with st.expander("📰 Final Newsletter"):
            st.markdown(MOCK_NEWSLETTER_OCT)
    
    elif st.button("▶️ Run Multi-Agent Analysis", type="primary", disabled=True):
        st.warning("⚠️ Please enter an analysis query before running multi-agent analysis.")

with tab3:
    st.markdown("### 📚 Knowledge Base Overview")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Total Documents", "0", delta="Upload files to begin")
        st.metric("Total Chunks", "0")
    
    with col2:
        st.metric("Avg Chunk Size", "—")
        st.metric("Embedding Model", "text-embedding-3-large")
    
    with col3:
        st.metric("Index Size", "0 MB")
        st.metric("Last Updated", "Never")
    
    st.markdown("---")
    
    st.markdown("#### 📂 Document Breakdown")
    
    st.info("📁 No documents uploaded yet. Use the sidebar to upload PDFs, Excel files, or Word documents.")
    
    # Empty state chart
    chart_data = {
        "Category": ["Newsletters", "Market Context", "P&L Data"],
        "Documents": [0, 0, 0],
        "Chunks": [0, 0, 0]
    }
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.bar_chart(chart_data, x="Category", y="Documents")
    
    with col2:
        st.bar_chart(chart_data, x="Category", y="Chunks")
    
    st.markdown("---")
    
    # Sample documents - empty state
    st.markdown("#### 📄 Recent Documents")
    st.info("No documents in the system yet.")

# Footer
st.markdown("---")
col1, col2, col3 = st.columns(3)

with col1:
    st.metric("RAG Retrieval", f"{retrieval_k} docs")

with col2:
    st.metric("LLM Model", model_choice)

with col3:
    st.metric("Avg Response Time", "—")

st.caption("Powered by LangChain + FAISS + Claude/Gemini")
