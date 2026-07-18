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
# LOAD DATA
#######################################
df = pd.read_csv('data/WA_Fn-UseC_-Telco-Customer-Churn.csv')

df['TotalCharges'] = pd.to_numeric(df['TotalCharges'], errors='coerce')
df.dropna(inplace=True)

#######################################
# METRICS (UNCHANGED LOGIC)
#######################################
customers = len(df)
churned = len(df[df['Churn'] == 'Yes'])
retained = customers - churned

churn_rate = round(churned / customers * 100, 2)
retention = round(retained / customers * 100, 2)

avg_bill = round(df['MonthlyCharges'].mean(), 2)
avg_tenure = round(df['tenure'].mean(), 1)

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
    (churn_rate, "Churn %"),
    (retention, "Retention %"),
    (avg_bill, "Avg Bill")
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
    fig = px.pie(df, names='Churn', hole=0.5,
                 title='Churn Distribution')
    st.plotly_chart(fig, use_container_width=True)

with col2:
    contract = df['Contract'].value_counts()
    fig = px.bar(x=contract.index, y=contract.values,
                 title='Contract Types')
    st.plotly_chart(fig, use_container_width=True)

col3, col4 = st.columns(2)

with col3:
    fig = px.histogram(df, x='MonthlyCharges', nbins=30,
                       title='Monthly Charges Distribution')
    st.plotly_chart(fig, use_container_width=True)

with col4:
    payment = df['PaymentMethod'].value_counts()
    fig = px.bar(x=payment.index, y=payment.values,
                 title='Payment Methods')
    st.plotly_chart(fig, use_container_width=True)

col5, col6 = st.columns(2)

with col5:
    internet = df['InternetService'].value_counts()
    fig = px.bar(x=internet.index, y=internet.values,
                 title='Internet Services')
    st.plotly_chart(fig, use_container_width=True)

with col6:
    fig = px.box(df, x='Churn', y='tenure', color='Churn',
                 title='Tenure vs Churn')
    st.plotly_chart(fig, use_container_width=True)

#######################################
# EXECUTIVE SUMMARY
#######################################
st.markdown("<div class='section'>🧠 Executive Intelligence</div>", unsafe_allow_html=True)

high_contract = df[df['Churn'] == 'Yes']['Contract'].value_counts().idxmax()
high_payment = df[df['Churn'] == 'Yes']['PaymentMethod'].value_counts().idxmax()
high_internet = df[df['Churn'] == 'Yes']['InternetService'].value_counts().idxmax()

st.info(f"""
### Key Findings
- Total Customers: {customers}
- Churn Rate: {churn_rate}%
- Avg Monthly Bill: ${avg_bill}
- Avg Tenure: {avg_tenure} months

### High Risk Segment
- Contract: {high_contract}
- Payment: {high_payment}
- Internet: {high_internet}

### Business Actions
✔ Promote Annual Contracts  
✔ Improve Fiber Services  
✔ Auto-pay Incentives  
✔ Loyalty Programs  
""")