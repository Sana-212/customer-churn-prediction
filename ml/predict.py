import pandas as pd
import joblib
import os
from ml.preprocess import preprocess_data

# ======================================
# STEP 1: Load saved files
# ======================================
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MODEL_DIR = os.path.join(BASE_DIR, "models")

model = joblib.load(os.path.join(MODEL_DIR, "model.pkl"))
feature_columns = joblib.load(os.path.join(MODEL_DIR, "feature_columns.pkl"))
feature_means = joblib.load(os.path.join(MODEL_DIR, "feature_means.pkl"))

# ======================================
# MAIN LOGIC FUNCTION
# ======================================
def run_prediction_pipeline(input_df):
    """
    Takes a DataFrame, processes it, and returns a results DataFrame.
    """
    raw_df = input_df.copy()

    # --- STEP 3: Handle IDs ---
    id_col = next((col for col in ["customerID", "CustomerID", "customer_id", "ID"] if col in raw_df.columns), None)
    customer_ids = raw_df[id_col] if id_col else pd.Series(range(1, len(raw_df) + 1), name="CustomerID")

    # --- STEP 4: Remove target ---
    if "Churn" in raw_df.columns:
        raw_df = raw_df.drop(columns=["Churn"])

    # --- STEP 5: Preprocess ---
    print("Input Columns:", list(raw_df.columns))
    print(raw_df.columns.tolist())
    X_new = preprocess_data(raw_df, training=False)
    print("Processed Columns:", list(X_new.columns))

    # --- STEP 6: Align features ---
    missing_cols = set(feature_columns) - set(X_new.columns)
    extra_cols = set(X_new.columns) - set(feature_columns)
    for col in missing_cols:
        X_new[col] = 0
    if extra_cols:
        X_new = X_new.drop(columns=list(extra_cols))
    X_new = X_new[feature_columns]

    # --- STEP 7: Prediction ---
    predictions = model.predict(X_new)
    if hasattr(model, "predict_proba"):
        churn_index = list(model.classes_).index("Yes")
        probabilities = model.predict_proba(X_new)[:, churn_index]
    else:
        probabilities = [0] * len(predictions)

    # --- STEP 8: Risk calculation ---
    def risk(prob):
        if prob >= 0.7: return "High"
        elif prob >= 0.4: return "Medium"
        return "Low"

    risk_levels = [risk(p) for p in probabilities]

    # --- STEP 9: Reasons ---
    importance = pd.Series(getattr(model, "feature_importances_", [1]*len(feature_columns)), index=feature_columns)
    if hasattr(model, "coef_"):
        importance = pd.Series(abs(model.coef_[0]), index=feature_columns)
    
    top_features = importance.sort_values(ascending=False).head(8).index

    def get_reason(row):
        reasons = []
        for feature in top_features[:3]:
            if feature in feature_means.index:
                val = row[feature] if feature in row else 0
                reasons.append(f"{feature} is {'higher' if val > feature_means[feature] else 'lower'} than average")
        return "; ".join(reasons)

    reasons = [get_reason(X_new.iloc[i]) for i in range(len(X_new))]

    # --- STEP 10: Retention suggestions ---
    def suggestion(reason):
        if "MonthlyCharges" in reason: return "Offer discount or flexible pricing"
        elif "tenure" in reason: return "Offer loyalty rewards"
        elif "Contract" in reason: return "Encourage long-term contract"
        elif "TechSupport" in reason: return "Offer technical support package"
        return "Contact customer proactively"

    suggestions = [suggestion(r) for r in reasons]

        # --------------------------------------
    # Merge original customer data with predictions
    # --------------------------------------

    output = input_df.copy()

    output["CustomerID"] = customer_ids

    output["Churn_Prediction"] = [
        "Yes" if p == "Yes" else "No"
        for p in predictions
    ]

    output["Churn_Probability"] = [
        round(p * 100, 2)
        for p in probabilities
    ]

    output["Risk_Level"] = risk_levels

    output["Key_Reasons"] = reasons

    output["Retention_Suggestion"] = suggestions

    return output
# ======================================
# EXECUTION (Only if run directly)
# ======================================
if __name__ == "__main__":
    import sys
    input_path = sys.argv[1] if len(sys.argv) > 1 else os.path.join(BASE_DIR, "data", "clean_dataset.csv")
    df = pd.read_csv(input_path)
    results = run_prediction_pipeline(df)
    results.to_csv(os.path.join(BASE_DIR, "reports", "churn_predictions.csv"), index=False)
    print("Report generated successfully")