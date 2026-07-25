import streamlit as st
import pandas as pd
import os
from ui import load_css

load_css()

st.set_page_config(page_title="Export Reports", layout="wide")

##########################################
# MODERN CSS (SAAS STYLE)
##########################################
st.markdown("""
<style>
.card { padding: 22px; border-radius: 18px; background: rgba(255,255,255,0.75); box-shadow: 0 10px 25px rgba(0,0,0,0.08); text-align: center; border: 1px solid rgba(255,255,255,0.4); backdrop-filter: blur(10px); }
.big { font-size: 34px; font-weight: 900; color: #2563eb; }
.small { font-size: 15px; color: #64748b; }
.section-title { font-size: 20px; font-weight: 800; color: #0f172a; margin: 25px 0 15px 0; border-left: 5px solid #2563eb; padding-left: 10px; }
.block-card { padding: 18px; border-radius: 15px; background: white; box-shadow: 0 6px 18px rgba(0,0,0,0.06); }
</style>
""", unsafe_allow_html=True)

st.title("⬇ Export Reports")

##########################################
# LOAD PREDICTION REPORT
##########################################
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

##########################################
# METRICS
##########################################
customers = len(df)

churned = len(df[df["Churn_Prediction"] == "Yes"])

retained = len(df[df["Churn_Prediction"] == "No"])

high_risk = len(df[df["Risk_Level"] == "High"])

# KPI CARDS
# KPI CARDS
c1, c2, c3 = st.columns(3)

for col, val, name in zip(
    [c1, c2, c3],
    [customers, churned, high_risk],
    ["Customers", "Predicted Churn", "High Risk"]
):
    with col:
        st.markdown(
            f'<div class="card"><div class="big">{val}</div><div class="small">{name}</div></div>',
            unsafe_allow_html=True
        )

##########################################
# PREVIEW
##########################################
st.markdown("<div class='section-title'>Dataset Preview</div>", unsafe_allow_html=True)
st.dataframe(df.head(10), use_container_width=True)

##########################################
# DOWNLOADS
##########################################
st.markdown("<div class='section-title'>Download Reports</div>", unsafe_allow_html=True)

def convert_df(data):
    return data.to_csv(index=False).encode('utf-8')

col1, col2, col3 = st.columns(3)
with col1:
    st.download_button(
        "📄 Full Prediction Report",
        convert_df(df),
        "prediction_report.csv",
        "text/csv"
    )

with col2:
    st.download_button(
        "⚠ High Risk Customers",
        convert_df(df[df["Risk_Level"] == "High"]),
        "high_risk_customers.csv",
        "text/csv"
    )

with col3:
    st.download_button(
        "✅ Low Risk Customers",
        convert_df(df[df["Risk_Level"] == "Low"]),
        "low_risk_customers.csv",
        "text/csv"
    )

##########################################
# SUMMARY
##########################################
st.info(f"""
### Available Exports

• Full Prediction Report

• High Risk Customers

• Low Risk Customers

### Statistics

Total Customers: {customers}

Predicted Churn: {churned}

High Risk Customers: {high_risk}

These reports are generated from the machine learning prediction pipeline and can be shared with management for customer retention planning.
""")