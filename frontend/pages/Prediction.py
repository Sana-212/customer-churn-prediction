import streamlit as st
import pandas as pd
import sys
import os

# 1. Path setup
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

# 2. Import your pipeline
from ml.predict import run_prediction_pipeline

st.title("📊 Customer Churn Prediction")

# 3. Create the UI inputs
# NOTE: Use the exact column names as your training dataset (e.g., 'tenure', 'Contract', 'InternetService')
uploaded_file = st.file_uploader(
    "Upload Customer CSV",
    type=["csv"]
)

if uploaded_file:
    df = pd.read_csv(uploaded_file)

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

    st.subheader("📄 Dataset Preview")
    st.dataframe(df.head())

    if st.button("Predict Churn"):

        try:
            results = run_prediction_pipeline(df)

            st.subheader("Prediction Results")
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

        except Exception as e:
            st.error(f"❌ Prediction failed: {e}")
            st.stop()