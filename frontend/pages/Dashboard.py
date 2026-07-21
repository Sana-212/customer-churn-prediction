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

#######################################
# LOAD PREDICTION REPORT
#######################################
import os

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))

REPORT_PATH = os.path.join(
    BASE_DIR,
    "reports",
    "churn_predictions.csv"
)

if not os.path.exists(REPORT_PATH):
    st.warning("⚠ No prediction report found. Please run predictions first.")
    st.stop()

df = pd.read_csv(REPORT_PATH)

#######################################
# METRICS (UNCHANGED LOGIC)
#######################################
customers = len(df)

churned = len(df[df["Churn_Prediction"] == "Yes"])
retained = len(df[df["Churn_Prediction"] == "No"])

churn_rate = round(churned / customers * 100, 2)
retention = round(retained / customers * 100, 2)

high_risk = len(df[df["Risk_Level"] == "High"])
average_probability = round(df["Churn_Probability"].mean(), 2)

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
# KPI CARDS
#######################################
c1, c2, c3, c4 = st.columns(4)

cards = [
    (customers, "Customers"),
    (churn_rate, "Predicted Churn %"),
    (high_risk, "High Risk"),
    (average_probability, "Avg Probability %")
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
# CHART SECTION
#######################################
st.markdown("<div class='section'>📈 Customer Insights</div>", unsafe_allow_html=True)

col1, col2 = st.columns(2)

with col1:
    fig = px.pie(
        df,
        names="Churn_Prediction",
        hole=0.5,
        title="Predicted Churn Distribution"
    )
    st.plotly_chart(fig, use_container_width=True)

with col2:
    risk = df["Risk_Level"].value_counts()

    fig = px.bar(
        x=risk.index,
        y=risk.values,
        title="Risk Levels"
    )

    st.plotly_chart(fig, use_container_width=True)

col3, col4 = st.columns(2)

with col3:
    fig = px.histogram(
        df,
        x="Churn_Probability",
        nbins=20,
        title="Prediction Probability Distribution"
    )

    st.plotly_chart(fig, use_container_width=True)

with col4:
    fig = px.box(
        df,
        y="Churn_Probability",
        color="Risk_Level",
        title="Probability by Risk Level"
    )

    st.plotly_chart(fig, use_container_width=True)
#######################################
# EXECUTIVE SUMMARY
#######################################
st.markdown("<div class='section'>🧠 Executive Intelligence</div>", unsafe_allow_html=True)

st.info(f"""
### Prediction Summary

- Total Customers: {customers}
- Predicted Churn: {churned}
- Retained Customers: {retained}
- High Risk Customers: {high_risk}
- Average Churn Probability: {average_probability}%

### Business Actions

✔ Contact High Risk Customers Immediately

✔ Prioritize Customers with High Probability Scores

✔ Offer Retention Discounts

✔ Monitor Medium Risk Customers

✔ Continue Monitoring Low Risk Customers
""")