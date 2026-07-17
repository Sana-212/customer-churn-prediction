import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report
import joblib
import os

from preprocess import preprocess_data



# ---------------------------------
# Paths
# ---------------------------------

BASE_DIR = os.path.dirname(
    os.path.dirname(
        os.path.abspath(__file__)
    )
)


DATA_PATH = os.path.join(
    BASE_DIR,
    "data",
    "raw_customer_data.csv"
)


MODEL_DIR = os.path.join(
    BASE_DIR,
    "models"
)


os.makedirs(
    MODEL_DIR,
    exist_ok=True
)



# ---------------------------------
# STEP 1: Load dataset
# ---------------------------------

df = pd.read_csv(
    DATA_PATH
)



print(
    "Original Dataset:",
    df.shape
)



# ---------------------------------
# STEP 2: Preprocess whole dataset
# ---------------------------------
y = df["Churn"]

X = df.drop(
    columns=["Churn"]
)


# preprocess ONLY features

X = preprocess_data(
    X,
    training=True
)
print(X.shape)
print(y.shape)


# ---------------------------------
# STEP 4: Train-test split
# ---------------------------------

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42
)



print(
    "Training rows:",
    len(X_train)
)

print(
    "Testing rows:",
    len(X_test)
)



# ---------------------------------
# STEP 5: Logistic Regression
# ---------------------------------

print(
    "\nTraining Logistic Regression..."
)


lr_model = LogisticRegression(
    max_iter=1000
)


lr_model.fit(
    X_train,
    y_train
)


lr_predictions = lr_model.predict(
    X_test
)


lr_accuracy = accuracy_score(
    y_test,
    lr_predictions
)


print(
    f"Accuracy: {lr_accuracy*100:.2f}%"
)



# ---------------------------------
# STEP 6: Random Forest
# ---------------------------------

print(
    "\nTraining Random Forest..."
)


rf_model = RandomForestClassifier(
    n_estimators=100,
    random_state=42
)


rf_model.fit(
    X_train,
    y_train
)


rf_predictions = rf_model.predict(
    X_test
)


rf_accuracy = accuracy_score(
    y_test,
    rf_predictions
)


print(
    f"Accuracy: {rf_accuracy*100:.2f}%"
)



# ---------------------------------
# STEP 7: Select best model
# ---------------------------------

if rf_accuracy >= lr_accuracy:

    best_model = rf_model
    best_predictions = rf_predictions

    print(
        "Winner: Random Forest"
    )

else:

    best_model = lr_model
    best_predictions = lr_predictions

    print(
        "Winner: Logistic Regression"
    )



print(
    classification_report(
        y_test,
        best_predictions
    )
)



# ---------------------------------
# STEP 8: Save model files
# ---------------------------------


joblib.dump(
    best_model,
    os.path.join(
        MODEL_DIR,
        "model.pkl"
    )
)


joblib.dump(
    X.columns.tolist(),
    os.path.join(
        MODEL_DIR,
        "feature_columns.pkl"
    )
)


joblib.dump(
    X_train.mean(),
    os.path.join(
        MODEL_DIR,
        "feature_means.pkl"
    )
)



print(
    "\nAll model files saved successfully"
)