import pandas as pd
import joblib
import sys
import os

from preprocess import preprocess_data


# ======================================
# STEP 1: Load saved files
# ======================================

BASE_DIR = os.path.dirname(
    os.path.dirname(
        os.path.abspath(__file__)
    )
)

MODEL_DIR=os.path.join(
    BASE_DIR,
    "models"
)


model = joblib.load(
    os.path.join(MODEL_DIR,"model.pkl")
)

feature_columns = joblib.load(
    os.path.join(MODEL_DIR,"feature_columns.pkl")
)

feature_means = joblib.load(
    os.path.join(MODEL_DIR,"feature_means.pkl")
)

print("Model files loaded")



# ======================================
# STEP 2: Load input CSV
# ======================================


if len(sys.argv)>1:

    input_path=sys.argv[1]

else:

    input_path=os.path.join(
    BASE_DIR,
    "data",
    "clean_dataset.csv"
)



raw_df=pd.read_csv(input_path)



print(
    f"Original input shape: {raw_df.shape}"
)



# ======================================
# STEP 3: Save customer IDs
# ======================================


id_col=None


for col in [
    "customerID",
    "CustomerID",
    "customer_id",
    "ID"
]:

    if col in raw_df.columns:

        id_col=col
        break



if id_col:

    customer_ids=raw_df[id_col]

else:

    customer_ids=pd.Series(
        range(1,len(raw_df)+1),
        name="CustomerID"
    )



# ======================================
# STEP 4: Remove target column
# ======================================


if "Churn" in raw_df.columns:

    raw_df=raw_df.drop(
        columns=["Churn"]
    )



# ======================================
# STEP 5: Preprocess features
# ======================================


X_new=preprocess_data(
    raw_df,
    training=False
)



print(
    f"After preprocessing: {X_new.shape}"
)



# ======================================
# STEP 6: Align features
# ======================================


missing_cols=set(feature_columns)-set(X_new.columns)

extra_cols=set(X_new.columns)-set(feature_columns)



for col in missing_cols:

    X_new[col]=0



if extra_cols:

    X_new=X_new.drop(
        columns=list(extra_cols)
    )



X_new=X_new[feature_columns]



if missing_cols:

    print(
        "Missing columns filled:",
        missing_cols
    )



# ======================================
# STEP 7: Prediction
# ======================================


predictions=model.predict(X_new)



# probability


if hasattr(model,"predict_proba"):

    churn_index = list(model.classes_).index("Yes")

    probabilities = model.predict_proba(X_new)[:, churn_index]

else:

    probabilities=[0]*len(predictions)



print("Prediction completed")



# ======================================
# STEP 8: Risk calculation
# ======================================


def risk(prob):

    if prob>=0.7:

        return "High"

    elif prob>=0.4:

        return "Medium"

    else:

        return "Low"



risk_levels=[
    risk(p)
    for p in probabilities
]



# ======================================
# STEP 9: Reasons
# ======================================


if hasattr(model,"feature_importances_"):


    importance=pd.Series(
        model.feature_importances_,
        index=feature_columns
    )


elif hasattr(model,"coef_"):


    importance=pd.Series(
        abs(model.coef_[0]),
        index=feature_columns
    )


else:


    importance=pd.Series(
        1,
        index=feature_columns
    )



top_features=(
    importance
    .sort_values(
        ascending=False
    )
    .head(8)
    .index
)



def get_reason(row):

    reasons=[]


    for feature in top_features[:3]:


        if feature in feature_means.index:


            if row[feature] > feature_means[feature]:

                reasons.append(
                    f"{feature} is higher than average"
                )

            else:

                reasons.append(
                    f"{feature} is lower than average"
                )


    return "; ".join(reasons)



reasons=[

    get_reason(
        X_new.iloc[i]
    )

    for i in range(len(X_new))

]



# ======================================
# STEP 10: Retention suggestions
# ======================================


def suggestion(reason):

    if "MonthlyCharges" in reason:

        return "Offer discount or flexible pricing"

    elif "tenure" in reason:

        return "Offer loyalty rewards"

    elif "Contract" in reason:

        return "Encourage long-term contract"

    elif "TechSupport" in reason:

        return "Offer technical support package"

    else:

        return "Contact customer proactively"



suggestions=[
    suggestion(r)
    for r in reasons
]



# ======================================
# STEP 11: Save report
# ======================================


results=pd.DataFrame({

    "CustomerID":customer_ids,

    "Churn_Prediction":[
        "Yes" if p=="Yes" else "No"
        for p in predictions
    ],

    "Churn_Probability":[
        round(p*100,2)
        for p in probabilities
    ],

    "Risk_Level":risk_levels,

    "Key_Reasons":reasons,

    "Retention_Suggestion":suggestions

})


REPORT_DIR=os.path.join(
    BASE_DIR,
    "reports"
)

os.makedirs(
    REPORT_DIR,
    exist_ok=True
)


results.to_csv(
    os.path.join(
        REPORT_DIR,
        "churn_predictions.csv"
    ),
    index=False
)

print(
    "Report generated successfully"
)


print(results.head())