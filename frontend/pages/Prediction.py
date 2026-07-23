import streamlit as st
import pandas as pd
import sys
import os

# 1. Path setup
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

# 2. Import your pipeline
from ml.predict import run_prediction_pipeline

st.set_page_config(
    page_title="Customer Churn Prediction",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

###############################################
# CSS - Blue Theme (matches platform design)
###############################################

st.markdown("""
<style>

.stApp{
background-color:#F5F7FA;
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
            
/* Hero Section */
.hero{
    padding:60px 50px;
    border-radius:25px;
    background: linear-gradient(135deg,#0F172A,#1E3A8A,#2563EB,#38BDF8);
    color:white;
    text-align:center;
    box-shadow:0 10px 30px rgba(0,0,0,0.2);
    margin-bottom:30px;
}
.hero-title{
    font-size:48px;
    font-weight:900;
    margin:0;
    line-height:1.2;
    background: linear-gradient(90deg,#ffffff,#dbeafe,#93c5fd);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    letter-spacing:1px;
}
.hero p{
    font-size:20px;
    opacity:.95;
    margin-top:10px;
}
.tag{
    display:inline-block;
    padding:12px 25px;
    background:white;
    color:#2563EB;
    border-radius:12px;
    font-weight:bold;
    margin-top:15px;
}

.section{
    font-size:28px;
    font-weight:700;
    margin-top:35px;
    margin-bottom:15px;
    color:#0F172A;
}

/* Card container for uploader / preview / results */
.card{
    background:white;
    padding:30px;
    border-radius:20px;
    box-shadow:0 4px 15px rgba(0,0,0,.08);
    transition:.3s;
    margin-bottom:25px;
}
.card:hover{
    box-shadow:0 10px 25px rgba(0,0,0,.15);
}

/* File uploader box */
section[data-testid="stFileUploaderDropzone"] {
    background-color:#EFF6FF;
    border:2px dashed #2563EB;
    border-radius:14px;
    padding:20px;
}
section[data-testid="stFileUploaderDropzone"]:hover {
    border-color:#38BDF8;
}

/* DataFrames */
.stDataFrame {
    border-radius:14px;
    overflow:hidden;
    box-shadow:0 4px 15px rgba(0,0,0,.08);
}

/* Buttons */
.stButton > button {
    background: linear-gradient(135deg,#1E3A8A,#2563EB,#38BDF8);
    color:white;
    border:none;
    border-radius:12px;
    padding:0.7em 1.6em;
    font-weight:700;
    font-size:16px;
    transition:.3s;
    box-shadow:0 4px 12px rgba(37,99,235,0.4);
}
.stButton > button:hover {
    transform:translateY(-3px);
    box-shadow:0 8px 20px rgba(37,99,235,0.5);
}

/* Download button */
.stDownloadButton > button {
    background: linear-gradient(135deg,#2563EB,#38BDF8);
    color:white;
    border:none;
    border-radius:12px;
    padding:0.7em 1.6em;
    font-weight:700;
    box-shadow:0 4px 12px rgba(56,189,248,0.4);
    transition:.3s;
}
.stDownloadButton > button:hover {
    transform:translateY(-3px);
    box-shadow:0 8px 20px rgba(56,189,248,0.5);
}

/* Alerts */
.stAlert {
    border-radius:14px;
}

/* Nav link buttons (Dashboard / Insights) */
div[data-testid="stPageLink"] a {
    background: white;
    border: 1.5px solid #2563EB;
    color: #2563EB !important;
    border-radius: 12px;
    padding: 0.7em 1.2em;
    font-weight: 700;
    text-align: center;
    transition: .3s;
    display: block;
}
div[data-testid="stPageLink"] a:hover {
    background: #2563EB;
    color: white !important;
    transform: translateY(-3px);
    box-shadow: 0 8px 20px rgba(37,99,235,0.3);
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

#################################################
# HERO
#################################################

st.markdown(
"""
<div class="hero">
<div class="hero-title">💻 Customer Churn Prediction</div>
<p>Upload your customer data and get instant churn risk predictions</p>
</div>
""",
unsafe_allow_html=True
)

# 3. Create the UI inputs
# NOTE: Use the exact column names as your training dataset (e.g., 'tenure', 'Contract', 'InternetService')

st.markdown("<div class='section'>📤 Upload Customer Data</div>", unsafe_allow_html=True)

with st.container(border=True):
    uploaded_file = st.file_uploader(
        "Upload Customer CSV",
        type=["csv"]
    )
    if "uploaded_df" in st.session_state:
        st.caption("✅ A previously uploaded dataset is currently loaded. Upload a new file to replace it.")

#################################################
# RESOLVE DATA SOURCE
# - fresh upload takes priority
# - otherwise fall back to whatever is already in session_state
#   (so data survives navigating to Dashboard/Insights and back)
#################################################
if uploaded_file:
    df = pd.read_csv(
        uploaded_file,
        encoding="utf-8-sig"
    )
    # remove hidden spaces
    df.columns = (
        df.columns
        .str.strip()
        .str.replace("\ufeff", "", regex=False)
    )
    df.columns = df.columns.str.strip()

    # Save uploaded dataset globally for dashboard
    st.session_state["uploaded_df"] = df

    # A brand-new file was uploaded -> clear any old prediction results
    st.session_state.pop("prediction_results", None)

elif "uploaded_df" in st.session_state:
    df = st.session_state["uploaded_df"]
else:
    df = None

if df is not None:

    print(df.columns.tolist())

    required_columns = [
        "customerID",
        "gender",
        "SeniorCitizen",
        "Partner",
        "Dependents",
        "tenure",
        "PhoneService",
        "MultipleLines",
        "InternetService",
        "OnlineSecurity",
        "OnlineBackup",
        "DeviceProtection",
        "TechSupport",
        "StreamingTV",
        "StreamingMovies",
        "Contract",
        "PaperlessBilling",
        "PaymentMethod",
        "MonthlyCharges",
        "TotalCharges"
    ]

    missing_columns = [
        col for col in required_columns
        if col not in df.columns
    ]

    if missing_columns:
        st.error("❌ Uploaded CSV is missing these columns:")
        st.write(missing_columns)
        st.stop()

    st.markdown("<div class='section'>📄 Dataset Preview</div>", unsafe_allow_html=True)
    with st.container(border=True):
        st.dataframe(df.head())

    #############################################
    # NAVIGATE TO DASHBOARD / INSIGHTS
    #############################################
    st.markdown("<div class='section'>🧭 Explore Your Data</div>", unsafe_allow_html=True)

    nav_col1, nav_col2 = st.columns(2)

    with nav_col1:
        st.page_link(
            "pages/Dashboard.py",
            label="📊 Go to Dashboard",
            use_container_width=True
        )

    with nav_col2:
        st.page_link(
            "pages/Insights.py",
            label="💡 Go to Insights",
            use_container_width=True
        )

    if st.button("Predict Churn"):

        try:

        # Save uploaded file temporarily
         temp_path = os.path.join(
            os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")),
            "uploaded_customer.csv"
        )

         df.to_csv(
            temp_path,
            index=False
        )

         results = run_prediction_pipeline(temp_path)

         # Persist results so they survive navigating away and back
         st.session_state["prediction_results"] = results

        except Exception as e:
            st.error(f"❌ Prediction failed: {e}")
            st.stop()

    #############################################
    # SHOW RESULTS (either just predicted, or restored from session_state)
    #############################################
    if "prediction_results" in st.session_state:

        results = st.session_state["prediction_results"]

        st.markdown("<div class='section'>🎯 Prediction Results</div>", unsafe_allow_html=True)
        with st.container(border=True):
            st.dataframe(results)

        csv = results.to_csv(index=False).encode("utf-8")

        REPORT_DIR = os.path.join(
            os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")),
            "reports"
        )

        os.makedirs(REPORT_DIR, exist_ok=True)

        results.to_csv(
            os.path.join(REPORT_DIR, "churn_predictions.csv"),
            index=False
        )

        st.download_button(
            label="📥 Download Prediction Report",
            data=csv,
            file_name="prediction_results.csv",
            mime="text/csv"
        )

