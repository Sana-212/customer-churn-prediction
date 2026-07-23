import streamlit as st
import pandas as pd

from ui import load_css
load_css()

st.set_page_config(
    page_title="Retention Insights",
    layout="wide"
)

############################################
# MODERN CSS (SAAS STYLE - MATCH DASHBOARD)
############################################
st.markdown("""
<style>

.main {
    background: linear-gradient(180deg, #F5F7FB 0%, #EEF2FF 100%);
}

[data-testid="stSidebar"]{
    background: linear-gradient(180deg, #0F172A 0%, #172554 100%);
    border-right: 1px solid rgba(255,255,255,0.06);
}

[data-testid="stSidebar"] *{
    color:white;
}

section[data-testid="stSidebar"] {
    width: 300px !important;
}
section[data-testid="stSidebar"] > div {
    width: 300px !important;
    padding: 0 !important;
}

/* Hide default Streamlit page navigation */
[data-testid="stSidebarNav"] {
    display: none;
}

/* Brand / logo header */
.sidebar-brand{
    display:flex;
    align-items:center;
    gap:12px;
    padding:28px 22px 22px 22px;
    border-bottom:1px solid rgba(255,255,255,0.08);
    margin-bottom:18px;
}
.sidebar-brand-icon{
    width:42px;
    height:42px;
    border-radius:12px;
    background:linear-gradient(135deg,#2563EB,#38BDF8);
    display:flex;
    align-items:center;
    justify-content:center;
    font-size:20px;
    box-shadow:0 4px 12px rgba(37,99,235,0.4);
    flex-shrink:0;
}
.sidebar-brand-text{
    line-height:1.25;
}
.sidebar-brand-title{
    font-size:15.5px;
    font-weight:800;
    color:white;
}
.sidebar-brand-sub{
    font-size:12px;
    color:#94A3B8;
    font-weight:500;
}

/* Nav section label */
.sidebar-section-label{
    font-size:11.5px;
    font-weight:700;
    color:#64748B;
    text-transform:uppercase;
    letter-spacing:1px;
    padding:0 22px;
    margin:6px 0 10px 0;
}

/* Nav link container padding */
[data-testid="stSidebar"] .element-container:has(.stPageLink) {
    padding: 0 14px;
}

/* Sidebar page links */
[data-testid="stSidebar"] .stPageLink a {
    display:flex;
    align-items:center;
    gap:10px;
    padding:13px 16px;
    margin:4px 0;
    border-radius:12px;
    font-size:15px;
    font-weight:600;
    color:#CBD5E1 !important;
    background:transparent;
    transition:all 0.25s ease;
    border:1px solid transparent;
}

[data-testid="stSidebar"] .stPageLink a:hover {
    background:rgba(37,99,235,0.18);
    border:1px solid rgba(56,189,248,0.25);
    color:white !important;
    transform:translateX(6px);
}

/* Sidebar footer */
.sidebar-footer{
    position:absolute;
    bottom:0;
    left:0;
    right:0;
    padding:18px 22px;
    border-top:1px solid rgba(255,255,255,0.08);
    font-size:12px;
    color:#64748B;
    text-align:center;
}
.block-container {
    padding-top: 2rem;
    padding-bottom: 3rem;
    max-width: 1200px;
}

/* Title */
h1 {
    font-size: 40px !important;
    font-weight: 900 !important;
    color: #0f172a;
    margin-bottom: 4px;
    letter-spacing: -0.5px;
}

/* Subtitle */
.subtitle {
    color: #64748b;
    font-size: 16px;
    margin-bottom: 24px;
    padding-bottom: 20px;
    border-bottom: 1px solid rgba(15,23,42,0.08);
}

/* Section title */
.section-title {
    font-size: 21px;
    font-weight: 800;
    color: #0f172a;
    margin: 36px 0 16px 0;
    padding-left: 12px;
    border-left: 5px solid #2563eb;
}

.section-sub {
    font-size: 13.5px;
    color: #94a3b8;
    margin: -12px 0 16px 17px;
}

/* KPI CARD */
.card {
    padding: 26px 20px;
    border-radius: 20px;
    background: rgba(255,255,255,0.85);
    box-shadow: 0 8px 24px rgba(37,99,235,0.08);
    text-align: center;
    border: 1px solid rgba(37,99,235,0.08);
    backdrop-filter: blur(12px);
    transition: 0.3s ease;
    position: relative;
    overflow: hidden;
}
.card::before {
    content: "";
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 4px;
    background: linear-gradient(90deg, #1E3A8A, #2563EB, #38BDF8);
}
.card:hover {
    transform: translateY(-8px);
    box-shadow: 0 20px 40px rgba(37,99,235,0.15);
    border-color: rgba(37,99,235,0.2);
}
.big {
    font-size: 36px;
    font-weight: 900;
    background: linear-gradient(135deg, #1E3A8A, #2563eb);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    line-height: 1.2;
}
.small {
    font-size: 14px;
    font-weight: 600;
    color: #64748b;
    margin-top: 6px;
    text-transform: uppercase;
    letter-spacing: 0.4px;
}

/* Real Streamlit bordered containers -> styled as cards */
div[data-testid="stVerticalBlockBorderWrapper"] {
    border-radius: 18px !important;
    background: white;
    box-shadow: 0 6px 18px rgba(15,23,42,0.06);
    border: 1px solid rgba(15,23,42,0.05) !important;
    transition: 0.3s ease;
    padding: 4px;
}
div[data-testid="stVerticalBlockBorderWrapper"]:hover {
    box-shadow: 0 12px 28px rgba(37,99,235,0.12);
    border-color: rgba(37,99,235,0.15) !important;
    transform: translateY(-4px);
}

/* Segmentation label + value */
.seg-label {
    font-size: 13px;
    font-weight: 700;
    color: #94a3b8;
    text-transform: uppercase;
    letter-spacing: 0.5px;
}
.seg-value {
    font-size: 19px;
    font-weight: 800;
    color: #2563eb;
    margin-top: 6px;
}

/* Recommendation card header row */
.rec-title {
    font-size: 16px;
    font-weight: 800;
    color: #0f172a;
    margin-bottom: 10px;
}
.rec-stat {
    display: inline-block;
    background: #EFF6FF;
    color: #2563EB;
    font-weight: 700;
    padding: 3px 10px;
    border-radius: 8px;
    font-size: 13.5px;
    margin-bottom: 12px;
}
.rec-actions {
    color: #475569;
    font-size: 14.5px;
    line-height: 1.9;
}

/* Executive summary grid */
.summary-heading {
    font-size: 14px;
    font-weight: 800;
    color: #94a3b8;
    text-transform: uppercase;
    letter-spacing: 0.5px;
    margin-bottom: 10px;
}
.summary-row {
    display: flex;
    justify-content: space-between;
    padding: 8px 0;
    border-bottom: 1px dashed rgba(15,23,42,0.08);
    font-size: 15px;
}
.summary-row:last-child { border-bottom: none; }
.summary-row span:first-child { color: #64748b; }
.summary-row span:last-child { font-weight: 700; color: #0f172a; }
.goal-box {
    margin-top: 16px;
    background: linear-gradient(135deg, #1E3A8A, #2563EB);
    color: white;
    padding: 16px 18px;
    border-radius: 14px;
    font-size: 14.5px;
    line-height: 1.6;
}

/* Alerts */
.stAlert {
    border-radius: 14px;
    font-weight: 600;
}

/* Column spacing */
div[data-testid="column"] {
    padding: 6px;
}

</style>
""", unsafe_allow_html=True)


with st.sidebar:

    st.markdown("""
    <div class="sidebar-brand">
        <div class="sidebar-brand-icon">🚀</div>
        <div class="sidebar-brand-text">
            <div class="sidebar-brand-title">Churn Platform</div>
            <div class="sidebar-brand-sub">AI Retention Analytics</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<div class='sidebar-section-label'>Navigation</div>", unsafe_allow_html=True)

    st.page_link(
        "Home.py",
        label="  Home"
    )

    st.page_link(
        "pages/Prediction.py",
        label="  Prediction"
    )

############################################
# TITLE
############################################
st.markdown("""
# 💡 Customer Retention Insights
<div class="subtitle">
AI-powered analysis for churn reduction and customer behavior insights
</div>
""", unsafe_allow_html=True)

############################################
# LOAD DATA
############################################

if "uploaded_df" in st.session_state:

    df = st.session_state["uploaded_df"]

else:

    st.warning(
        "⚠️ Please upload a customer CSV file from the Upload page first."
    )

    st.stop()
   # Back button aligned left
col1, col2, col3 = st.columns([1, 4, 1])

with col1:
    st.markdown("<div style='margin-top:30px'></div>", unsafe_allow_html=True)

    st.page_link(
        "pages/Prediction.py",
        label="⬅ Back"
    )



df["TotalCharges"] = pd.to_numeric(
    df["TotalCharges"],
    errors="coerce"
)

df.dropna(inplace=True)

############################################
# KPIS (UNCHANGED LOGIC)
############################################
customers = len(df)

churned = len(df[df["Churn"] == "Yes"])

retained = customers - churned

churn_rate = round(churned / customers * 100, 2)

retention_rate = round(retained / customers * 100, 2)

############################################
# SEGMENTS (UNCHANGED LOGIC)
############################################
high_contract = (
    df[df['Churn'] == 'Yes']['Contract']
    .value_counts()
    .idxmax()
)

high_payment = (
    df[df['Churn'] == 'Yes']['PaymentMethod']
    .value_counts()
    .idxmax()
)

high_internet = (
    df[df['Churn'] == 'Yes']['InternetService']
    .value_counts()
    .idxmax()
)

############################################
# EXTRA METRICS (UNCHANGED LOGIC)
############################################
month_percent = round(
    (df["Contract"].value_counts()["Month-to-month"] / customers) * 100,
    2
)

fiber = len(df[(df["InternetService"] == "Fiber optic") & (df["Churn"] == "Yes")])

fiber_percent = round(fiber / churned * 100, 2)

electronic = len(df[(df["PaymentMethod"] == "Electronic check") & (df["Churn"] == "Yes")])

electronic_percent = round(electronic / churned * 100, 2)

############################################
# KPI CARDS
############################################
c1, c2, c3 = st.columns(3)

cards = [
    (customers, "Total Customers"),
    (churn_rate, "Churn Rate %"),
    (retention_rate, "Retention Rate %")
]

for col, data in zip([c1, c2, c3], cards):
    value, label = data
    with col:
        st.markdown(f"""
        <div class="card">
            <div class="big">{value}</div>
            <div class="small">{label}</div>
        </div>
        """, unsafe_allow_html=True)

############################################
# SEGMENTATION
############################################
st.markdown("<div class='section-title'>🎯 Customer Segmentation</div>", unsafe_allow_html=True)
st.markdown("<div class='section-sub'>Where churn concentrates across contract, payment, and service type</div>", unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)

with col1:
    with st.container(border=True):
        st.markdown(f"""
        <div class="seg-label">🔥 Highest Churn Contract</div>
        <div class="seg-value">{high_contract}</div>
        """, unsafe_allow_html=True)

with col2:
    with st.container(border=True):
        st.markdown(f"""
        <div class="seg-label">💳 Highest Churn Payment</div>
        <div class="seg-value">{high_payment}</div>
        """, unsafe_allow_html=True)

with col3:
    with st.container(border=True):
        st.markdown(f"""
        <div class="seg-label">🌐 Highest Churn Internet</div>
        <div class="seg-value">{high_internet}</div>
        """, unsafe_allow_html=True)

############################################
# RECOMMENDATIONS
############################################
st.markdown("<div class='section-title'>📌 Retention Recommendations</div>", unsafe_allow_html=True)
st.markdown("<div class='section-sub'>Targeted actions based on churn drivers detected in your data</div>", unsafe_allow_html=True)

rec_cols = st.columns(3)
rec_slot = 0

if month_percent > 40:
    with rec_cols[rec_slot % 3]:
        with st.container(border=True):
            st.markdown(f"""
            <div class="rec-title">📄 Contract Insight</div>
            <div class="rec-stat">{month_percent}% Month-to-Month</div>
            <div class="rec-actions">
            • Promote yearly plans<br>
            • Offer discounts<br>
            • Bundle services
            </div>
            """, unsafe_allow_html=True)
    rec_slot += 1

if fiber_percent > 50:
    with rec_cols[rec_slot % 3]:
        with st.container(border=True):
            st.markdown(f"""
            <div class="rec-title">🌐 Fiber Optic Risk</div>
            <div class="rec-stat">{fiber_percent}% of churners</div>
            <div class="rec-actions">
            • Improve service stability<br>
            • Faster complaint resolution<br>
            • Dedicated support
            </div>
            """, unsafe_allow_html=True)
    rec_slot += 1

if electronic_percent > 30:
    with rec_cols[rec_slot % 3]:
        with st.container(border=True):
            st.markdown(f"""
            <div class="rec-title">💳 Payment Insight</div>
            <div class="rec-stat">{electronic_percent}% of churners</div>
            <div class="rec-actions">
            • Auto-pay incentives<br>
            • Cashback offers<br>
            • Billing simplification
            </div>
            """, unsafe_allow_html=True)
    rec_slot += 1

############################################
# RISK LEVEL
############################################
st.markdown("<div class='section-title'>⚠ Churn Risk Level</div>", unsafe_allow_html=True)

if churn_rate > 30:
    st.error("HIGH CHURN RISK 🚨")
elif churn_rate > 20:
    st.warning("MEDIUM CHURN RISK ⚠")
else:
    st.success("LOW CHURN RISK ✅")

############################################
# EXECUTIVE SUMMARY
############################################
st.markdown("<div class='section-title'>📊 Executive Summary</div>", unsafe_allow_html=True)

sum_col1, sum_col2 = st.columns(2)

with sum_col1:
    with st.container(border=True):
        st.markdown("<div class='summary-heading'>Business Overview</div>", unsafe_allow_html=True)
        st.markdown(f"""
        <div class="summary-row"><span>Total Customers</span><span>{customers}</span></div>
        <div class="summary-row"><span>Churn Rate</span><span>{churn_rate}%</span></div>
        <div class="summary-row"><span>Retention Rate</span><span>{retention_rate}%</span></div>
        """, unsafe_allow_html=True)

with sum_col2:
    with st.container(border=True):
        st.markdown("<div class='summary-heading'>High Risk Segments</div>", unsafe_allow_html=True)
        st.markdown(f"""
        <div class="summary-row"><span>Contract</span><span>{high_contract}</span></div>
        <div class="summary-row"><span>Payment</span><span>{high_payment}</span></div>
        <div class="summary-row"><span>Internet</span><span>{high_internet}</span></div>
        """, unsafe_allow_html=True)

st.markdown("""
<div class="goal-box">
🎯 <b>Goal:</b> Improve retention by 5–10% using AI-driven targeting strategies.
</div>
""", unsafe_allow_html=True)