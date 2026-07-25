import pandas as pd
import joblib
import os

from ml.preprocess import preprocess_data


# ======================================
# STEP 1: Paths and load saved files
# ======================================
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MODEL_DIR = os.path.join(BASE_DIR, "models")

print("Loading model...")
model = joblib.load(os.path.join(MODEL_DIR, "model.pkl"))
print("✅ model loaded")


print("Loading feature_columns...")
feature_columns = joblib.load(os.path.join(MODEL_DIR, "feature_columns.pkl"))
print("✅ feature_columns loaded")

print("Loading feature_means...")
feature_means = joblib.load(os.path.join(MODEL_DIR, "feature_means.pkl"))
print("✅ feature_means loaded")

print("Loading feature_stds...")
feature_stds = joblib.load(os.path.join(MODEL_DIR, "feature_stds.pkl"))
print("✅ feature_stds loaded")


def run_prediction_pipeline(df):

    # ======================================
    # STEP 2: Use the provided DataFrame
    # ======================================
    raw_df = df.copy()
    print(f"Original input shape: {raw_df.shape}")

    # ======================================
    # STEP 3: Save customer IDs
    # ======================================
    id_col = None
    for col in ["customerID", "CustomerID", "customer_id", "ID"]:
        if col in raw_df.columns:
            id_col = col
            break

    if id_col:
        customer_ids = raw_df[id_col]
    else:
        customer_ids = pd.Series(range(1, len(raw_df) + 1), name="CustomerID")

    # ======================================
    # STEP 4: Remove target column (if present)
    # ======================================
    if "Churn" in raw_df.columns:
        raw_df = raw_df.drop(columns=["Churn"])

    # ======================================
    # STEP 5: Preprocess features
    # ======================================
    X_new = preprocess_data(raw_df, training=False)
    print(f"After preprocessing: {X_new.shape}")

    # ======================================
    # STEP 6: Align features
    # ======================================
    missing_cols = set(feature_columns) - set(X_new.columns)
    extra_cols = set(X_new.columns) - set(feature_columns)

    for col in missing_cols:
        X_new[col] = 0

    if extra_cols:
        X_new = X_new.drop(columns=list(extra_cols))

    X_new = X_new[feature_columns]

    if missing_cols:
        print("Missing columns filled:", missing_cols)

    # ======================================
    # STEP 7: Prediction
    # ======================================
    predictions = model.predict(X_new)

    if hasattr(model, "predict_proba"):
        churn_index = list(model.classes_).index("Yes")
        probabilities = model.predict_proba(X_new)[:, churn_index]
    else:
        probabilities = [0] * len(predictions)

    print("Prediction completed")

    # ======================================
    # STEP 8: Risk calculation
    # ======================================
    def risk(prob):
        if prob >= 0.7:
            return "High"
        elif prob >= 0.4:
            return "Medium"
        else:
            return "Low"

    risk_levels = [risk(p) for p in probabilities]

    # ======================================
    # STEP 9: Reasons
    # personalized per customer: rank features by how much
    # THIS customer deviates from average, weighted by how
    # important that feature is to the model overall
    # ======================================
    if hasattr(model, "feature_importances_"):
        importance = pd.Series(model.feature_importances_, index=feature_columns)
    elif hasattr(model, "coef_"):
        importance = pd.Series(abs(model.coef_[0]), index=feature_columns)
    else:
        importance = pd.Series(1, index=feature_columns)

    # widen the candidate pool so there's enough variety to draw from per customer
    candidate_features = importance.sort_values(ascending=False).head(15).index

    def get_reason(row):
        scored = []
        for feature in candidate_features:
            if feature in feature_means.index and feature in feature_stds.index:
                std = feature_stds[feature]
                if std == 0 or pd.isna(std):
                    continue  # feature never varies in training data, skip it

                # z-score: how many standard deviations this customer is from
                # the TRAINING average (not the small uploaded batch), so
                # every feature is compared on the same fair scale
                z_score = (row[feature] - feature_means[feature]) / std
                scored.append((feature, abs(z_score) * importance[feature], z_score))

        # keep only this customer's top 3 standout features
        top_for_this_customer = sorted(scored, key=lambda x: x[1], reverse=True)[:3]

        reasons = []
        for feature, _, z_score in top_for_this_customer:
            direction = "higher" if z_score > 0 else "lower"
            reasons.append(f"{feature} is {direction} than average")
        return "; ".join(reasons)

    reasons = [get_reason(X_new.iloc[i]) for i in range(len(X_new))]

    # ======================================
    # STEP 10: Retention suggestions
    # based on this customer's single strongest reason
    # ======================================
    def suggestion(reason):
        top_reason = reason.split(";")[0]

        if "MonthlyCharges" in top_reason:
            return "Offer discount or flexible pricing"
        elif "tenure" in top_reason:
            return "Offer loyalty rewards"
        elif "Contract" in top_reason:
            return "Encourage long-term contract"
        elif "TechSupport" in top_reason:
            return "Offer technical support package"
        elif "InternetService" in top_reason:
            return "Offer a service upgrade or bundle deal"
        elif "OnlineSecurity" in top_reason:
            return "Bundle in a free online security add-on"
        elif "PaymentMethod" in top_reason:
            return "Suggest switching to autopay for convenience"
        else:
            return "Contact customer proactively"

    suggestions = [suggestion(r) for r in reasons]

    # ======================================
    # STEP 11: Build results
    # merge original columns back in so Dashboard/Insights
    # have access to Contract, MonthlyCharges, PaymentMethod, etc.
    # ======================================
    predictions_df = pd.DataFrame({
        "CustomerID": customer_ids,
        "Churn_Prediction": ["Yes" if p == "Yes" else "No" for p in predictions],
        "Churn_Probability": [round(p * 100, 2) for p in probabilities],
        "Risk_Level": risk_levels,
        "Key_Reasons": reasons,
        "Retention_Suggestion": suggestions,
    })

    original_features = raw_df.reset_index(drop=True)
    results = pd.concat(
        [original_features, predictions_df.reset_index(drop=True)],
        axis=1
    )

    # ======================================
    # STEP 12: Save report
    # ======================================
    REPORT_DIR = os.path.join(BASE_DIR, "reports")
    os.makedirs(REPORT_DIR, exist_ok=True)
    results.to_csv(os.path.join(REPORT_DIR, "churn_predictions.csv"), index=False)

    print("Report generated successfully")
    print(results.head())

    return results