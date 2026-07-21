import streamlit as st
import pandas as pd
import os
from ui import load_css

# Load CSS
load_css()

# Page Config
st.set_page_config(page_title="Retention Insights", layout="wide")

############################################
# MODERN CSS (SAAS STYLE)
############################################
st.markdown("""
<style>
.main { background: linear-gradient(180deg, #F5F7FB, #EEF2FF); }
h1 { font-size: 38px !important; font-weight: 900 !important; color: #0f172a; margin-bottom: 5px; }
.subtitle { color: #64748b; font-size: 16px; margin-bottom: 20px; }
.section-title { font-size: 20px; font-weight: 800; color: #0f172a; margin: 25px 0 15px 0; border-left: 5px solid #2563eb; padding-left: 10px; }
.card { padding: 22px; border-radius: 18px; background: rgba(255,255,255,0.75); box-shadow: 0 10px 25px rgba(0,0,0,0.08); text-align: center; border: 1px solid rgba(255,255,255,0.4); backdrop-filter: blur(10px); transition: 0.3s; }
.card:hover { transform: translateY(-6px); box-shadow: 0 18px 40px rgba(0,0,0,0.12); }
.big { font-size: 34px; font-weight: 900; color: #2563eb; }
.small { font-size: 15px; color: #64748b; }
.block-card { padding: 18px; border-radius: 15px; background: white; box-shadow: 0 6px 18px rgba(0,0,0,0.06); margin-bottom: 10px; }
</style>
""", unsafe_allow_html=True)

############################################
# LOAD PREDICTION RESULTS
############################################
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

############################################
# LOGIC
############################################
customers = len(df)
churned = len(df[df["Churn_Prediction"] == "Yes"])
retained = len(df[df["Churn_Prediction"] == "No"])

churn_rate = round(churned / customers * 100, 2)
retention_rate = round(retained / customers * 100, 2)

high_risk = len(df[df["Risk_Level"] == "High"])
medium_risk = len(df[df["Risk_Level"] == "Medium"])
low_risk = len(df[df["Risk_Level"] == "Low"])

average_probability = round(
    df["Churn_Probability"].mean(),
    2
)

############################################
# UI LAYOUT
############################################
st.markdown("""
# 💡 Customer Retention Insights
<div class="subtitle">AI-powered analysis for churn reduction and customer behavior insights</div>
""", unsafe_allow_html=True)

# KPI CARDS
c1, c2, c3 = st.columns(3)
cards = [(customers, "Total Customers"), (churn_rate, "Predicted Churn"), (retention_rate, "High Risk Customers")]

for col, (val, label) in zip([c1, c2, c3], cards):
    with col:
        st.markdown(f'<div class="card"><div class="big">{val}</div><div class="small">{label}</div></div>', unsafe_allow_html=True)

st.markdown("<div class='section-title'>🎯 Risk Distribution</div>", unsafe_allow_html=True)

c1, c2, c3 = st.columns(3)

with c1:
    st.metric("🔴 High Risk", high_risk)

with c2:
    st.metric("🟡 Medium Risk", medium_risk)

with c3:
    st.metric("🟢 Low Risk", low_risk)

st.markdown("<div class='section-title'>📌 Retention Recommendations</div>", unsafe_allow_html=True)

if high_risk > 0:
    st.info(f"🚨 {high_risk} customers are at High Risk. Contact them immediately.")

if medium_risk > 0:
    st.warning(f"⚠ {medium_risk} customers are at Medium Risk. Offer promotions or discounts.")

if low_risk > 0:
    st.success(f"✅ {low_risk} customers are at Low Risk. Maintain engagement through loyalty programs.")

# RISK LEVEL & SUMMARY
st.markdown("<div class='section-title'>⚠ Churn Risk Level</div>", unsafe_allow_html=True)
if churn_rate > 30: st.error("HIGH CHURN RISK 🚨")
elif churn_rate > 20: st.warning("MEDIUM CHURN RISK ⚠")
else: st.success("LOW CHURN RISK ✅")

st.markdown("<div class='section-title'>📊 Executive Summary</div>", unsafe_allow_html=True)
st.markdown(f'<div class="block-card"><b>Business Overview</b><br>• Total Customers: {customers}<br>• Churn Rate: {churn_rate}%<br>• Goal: Improve retention by 5–10% using AI-driven strategies.</div>', unsafe_allow_html=True)