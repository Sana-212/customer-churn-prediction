# Customer Churn Prediction & Retention Intelligence Platform

## Objective

This project predicts which customers are likely to churn (leave a service) based on their account and usage data. Users can upload a customer dataset, and the platform will:

- Predict churn for each customer
- Classify churn risk as **High**, **Medium**, or **Low**
- Provide simple, data-driven reasons behind each prediction
- Suggest relevant retention strategies for at-risk customers
- Allow the prediction report to be downloaded for further use

The goal is to help identify customers at risk of leaving early enough for a business to take action, rather than just reporting churn after the fact.

## Installation Steps

1. **Clone the repository**
   ```bash
   git clone https://github.com/Sana-212/customer-churn-prediction.git
   cd customer-churn-prediction
   ```

2. **Create and activate a virtual environment**

   Windows (PowerShell):
   ```powershell
   python -m venv venv
   venv\Scripts\activate
   ```

   macOS / Linux:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install the required libraries**
   ```bash
   pip install -r requirements.txt
   ```

## Required Libraries

All dependencies are listed in `requirements.txt`. Key libraries used:

| Library | Purpose |
|---|---|
| `pandas` | Data loading, cleaning, and manipulation |
| `numpy` | Numerical operations |
| `scikit-learn` | Model training (Logistic Regression, Random Forest) and preprocessing |
| `joblib` | Saving/loading trained model and preprocessing artifacts |
| `streamlit` | Web application interface |
| `matplotlib`, `seaborn`, `plotly` | Data visualization for the analytics dashboard |
| `scipy` | Supporting scientific computations |

Full pinned versions are available in `requirements.txt`.

## How to Run the Project

1. **Launch the application**

   The trained model files are already included in the repository (`models/` folder), so you can run the app directly without training anything first.
   ```bash
   streamlit run frontend/Home.py
   ```

2. **Use the app**
   - The app opens automatically in your browser (typically at `http://localhost:8501`)
   - On the Home page, upload a customer CSV file (a sample file is provided at `data/test_customers.csv`)
   - Click **Predict Churn**
   - Explore the Dashboard and Insights pages for charts and reasoning behind predictions
   - Download the generated report from the Prediction Results page

> **Note:** If you ever want to retrain the model — for example, after updating `data/raw_customer_data.csv` — run `python ml/train.py`. This will regenerate the files in `models/`. This step is optional and not required for normal use of the app.

## Expected Output

After uploading a dataset and running a prediction, the app displays a results table that merges the customer's **original uploaded columns** (`gender`, `SeniorCitizen`, `tenure`, `Contract`, `MonthlyCharges`, etc.) with the following **prediction columns** added at the end:

| Column | Description |
|---|---|
| `CustomerID` | Identifies the customer |
| `Churn_Prediction` | `Yes` or `No` |
| `Churn_Probability` | Model's confidence (%) that the customer will churn |
| `Risk_Level` | `High`, `Medium`, or `Low` |
| `Key_Reasons` | Top factors driving that customer's prediction |
| `Retention_Suggestion` | A suggested action to help retain that customer |

**Example row:**

| customerID | gender | tenure | Contract | MonthlyCharges | ... | Churn_Prediction | Churn_Probability | Risk_Level | Key_Reasons | Retention_Suggestion |
|---|---|---|---|---|---|---|---|---|---|---|
| TEST0001 | Male | 21 | Month-to-month | 96.59 | ... | No | 24.07 | Low | Contract_Month-to-month is higher than average; Contract_Two year is lower than average; InternetService_Fiber optic is higher than average | Encourage long-term contract |

The full report can also be downloaded as a CSV file from the app, and a copy is automatically saved to `reports/churn_predictions.csv`.