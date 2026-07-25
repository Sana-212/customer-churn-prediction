import streamlit as st
import pandas as pd
import plotly.express as px
from ui import load_css
load_css()

st.set_page_config(
    page_title="Customer Churn Dashboard",
    layout="wide",
    initial_sidebar_state="expanded"
)

#######################################
# MODERN UI CSS
#######################################
st.markdown("""
<style>

/* Background */
.main {
    background: linear-gradient(180deg, #F5F7FB, #EEF2FF);
}
            /* ============ SIDEBAR REDESIGN ============ */

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

/* Title */
h1 {
    font-size: 40px !important;
    font-weight: 900 !important;
    color: #0f172a;
    margin-bottom: 5px;
}

/* Subtitle */
.subtitle {
    color: #64748b;
    font-size: 16px;
    margin-bottom: 20px;
}

/* KPI Card */
.card {
    padding: 22px;
    border-radius: 18px;
    background: rgba(255,255,255,0.75);
    box-shadow: 0 10px 25px rgba(0,0,0,0.08);
    text-align: center;
    border: 1px solid rgba(255,255,255,0.4);
    backdrop-filter: blur(10px);
    transition: 0.3s;
}

.card:hover {
    transform: translateY(-6px);
    box-shadow: 0 18px 40px rgba(0,0,0,0.12);
}

/* KPI numbers */
.big {
    font-size: 34px;
    font-weight: 900;
    color: #2563eb;
}

/* KPI labels */
.small {
    font-size: 15px;
    color: #64748b;
    margin-top: 5px;
}

/* Section heading */
.section {
    font-size: 22px;
    font-weight: 800;
    margin: 30px 0 15px 0;
    color: #0f172a;
    border-left: 5px solid #2563eb;
    padding-left: 10px;
}

/* Chart containers */
div.stPlotlyChart {
    background: white;
    padding: 12px;
    border-radius: 15px;
    box-shadow: 0 6px 20px rgba(0,0,0,0.06);
}

/* Info box */
.stAlert {
    border-radius: 14px;
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

#######################################
# TITLE
#######################################
st.markdown("""
# 📊 Customer Churn Analytics Dashboard
<div class="subtitle">
AI-powered insights for customer retention and churn prediction
</div>
""", unsafe_allow_html=True)

#######################################
# LOAD DATA
#######################################


if "prediction_results" in st.session_state:

    df = st.session_state["prediction_results"]

else:

    st.warning(
        "⚠️ Please run a prediction from the Prediction page first."
    )

    st.stop()
col1, col2, col3 = st.columns([1, 4, 1])

with col1:
    st.markdown("<div style='margin-top:30px'></div>", unsafe_allow_html=True)

    st.page_link(
        "pages/Prediction.py",
        label="⬅ Back"
    )  

df['TotalCharges'] = pd.to_numeric(df['TotalCharges'], errors='coerce')
df.dropna(inplace=True)

#######################################
# METRICS (UNCHANGED LOGIC)
#######################################
customers = len(df)
churned = len(df[df['Churn_Prediction'] == 'Yes'])
retained = customers - churned

churn_rate = round(churned / customers * 100, 2)
retention = round(retained / customers * 100, 2)

avg_bill = round(df['MonthlyCharges'].mean(), 2)
avg_tenure = round(df['tenure'].mean(), 1)



#######################################
# KPI CARDS
#######################################
c1, c2, c3, c4 = st.columns(4)

cards = [
    (customers, "Customers"),
    (churn_rate, "Churn %"),
    (retention, "Retention %"),
    (avg_bill, "Avg Bill")
]

for col, data in zip([c1, c2, c3, c4], cards):
    value, name = data
    with col:
        st.markdown(f"""
        <div class='card'>
            <div class='big'>{value}</div>
            <div class='small'>{name}</div>
        </div>
        """, unsafe_allow_html=True)

#######################################
# CHART COLOR PALETTE
# Tableau10 classic categorical palette —
# industry-standard, distinct, professional,
# not neon, not all one hue.
#######################################
TABLEAU10 = [
    "#4E79A7",  # blue
    "#F28E2B",  # orange
    "#CE8283",  # green
    "#CE8283",  # red
    "#DA86C2",  # purple
    "#9C755F",  # brown
    "#EDC948",  # gold
    "#76B7B2",  # teal
    "#FF9DA7",  # pink
    "#BAB0AC",  # gray
]

CHURN_COLOR_MAP = {"No": "#EB8284", "Yes": "#4E79A7"}

CHART_LAYOUT = dict(
    plot_bgcolor="white",
    paper_bgcolor="white",
    font_color="#334155",
    title_font_size=15,
    title_font_color="#0f172a",
)

#######################################
# CHART SECTION
#######################################
st.markdown("<div class='section'>📈 Analytics</div>", unsafe_allow_html=True)

col1, col2 = st.columns(2)

with col1:
    fig = px.pie(df, names='Churn_Prediction', hole=0.5,
                 title='Churn Distribution',
                 color='Churn_Prediction',
                 color_discrete_map=CHURN_COLOR_MAP)
    fig.update_layout(**CHART_LAYOUT)
    st.plotly_chart(fig, use_container_width=True)

with col2:
    contract = df['Contract'].value_counts()
    fig = px.bar(x=contract.index, y=contract.values,
                 title='Contract Types',
                 color=contract.index,
                 color_discrete_sequence=TABLEAU10)
    fig.update_layout(**CHART_LAYOUT, showlegend=False)
    st.plotly_chart(fig, use_container_width=True)

col3, col4 = st.columns(2)

with col3:
    fig = px.histogram(df, x='MonthlyCharges', nbins=30,
                       title='Monthly Charges Distribution',
                       color_discrete_sequence=["#ACC2C9"])
    fig.update_layout(**CHART_LAYOUT)
    st.plotly_chart(fig, use_container_width=True)

with col4:
    payment = df['PaymentMethod'].value_counts()
    fig = px.bar(x=payment.index, y=payment.values,
                 title='Payment Methods',
                 color=payment.index,
                 color_discrete_sequence=TABLEAU10)
    fig.update_layout(**CHART_LAYOUT, showlegend=False)
    st.plotly_chart(fig, use_container_width=True)

col5, col6 = st.columns(2)

with col5:
    internet = df['InternetService'].value_counts()
    fig = px.bar(x=internet.index, y=internet.values,
                 title='Internet Services',
                 color=internet.index,
                 color_discrete_sequence=TABLEAU10)
    fig.update_layout(**CHART_LAYOUT, showlegend=False)
    st.plotly_chart(fig, use_container_width=True)

with col6:
    fig = px.box(df, x='Churn_Prediction', y='tenure', color='Churn_Prediction',
                 title='Tenure vs Churn',
                 color_discrete_map=CHURN_COLOR_MAP)
    fig.update_layout(**CHART_LAYOUT)
    st.plotly_chart(fig, use_container_width=True)