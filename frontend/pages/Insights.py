# import streamlit as st
# import pandas as pd
# from ui import load_css
# load_css()

# st.set_page_config(
#     page_title="Retention Insights",
#     layout="wide"
# )

# st.title("💡 Customer Retention Insights")


# ############################################
# # Load Dataset
# ############################################

# df = pd.read_csv(
#     "data/WA_Fn-UseC_-Telco-Customer-Churn.csv"
# )

# df["TotalCharges"] = pd.to_numeric(
#     df["TotalCharges"],
#     errors="coerce"
# )

# df.dropna(inplace=True)


# ############################################
# # KPIs
# ############################################

# customers = len(df)

# churned = len(
#     df[df["Churn"] == "Yes"]
# )

# retained = customers - churned


# churn_rate = round(
#     churned/customers*100,
#     2
# )


# retention_rate = round(
#     retained/customers*100,
#     2
# )



# ############################################
# # High Risk Segments
# ############################################


# high_contract = (

#     df[df['Churn'] == 'Yes']

#     ['Contract']

#     .value_counts()

#     .idxmax()

# )


# high_payment = (

#     df[df['Churn'] == 'Yes']

#     ['PaymentMethod']

#     .value_counts()

#     .idxmax()

# )


# high_internet = (

#     df[df['Churn'] == 'Yes']

#     ['InternetService']

#     .value_counts()

#     .idxmax()

# )



# ############################################
# # Percentages
# ############################################


# month_percent = round(

# (
# df["Contract"]

# .value_counts()

# ["Month-to-month"]

# /

# customers

# )*100,

# 2

# )



# fiber = len(

# df[

# (df["InternetService"]=="Fiber optic")

# &

# (df["Churn"]=="Yes")

# ]

# )

# fiber_percent = round(

# fiber/churned*100,

# 2

# )



# electronic = len(

# df[

# (df["PaymentMethod"]

# =="Electronic check")

# &

# (df["Churn"]

# =="Yes")

# ]

# )


# electronic_percent = round(

# electronic/churned*100,

# 2

# )



# ############################################
# # CSS
# ############################################


# st.markdown("""

# <style>

# .card{

# padding:25px;

# border-radius:15px;

# background:#F7F9FC;

# box-shadow:0px 2px 10px rgba(0,0,0,0.1);

# text-align:center;

# }


# .big{

# font-size:30px;

# font-weight:bold;

# color:#1F77B4;

# }


# .small{

# font-size:17px;

# }


# </style>

# """,unsafe_allow_html=True)



# ############################################
# # KPI CARDS
# ############################################


# c1,c2,c3=st.columns(3)



# with c1:


#     st.markdown(f"""

# <div class='card'>

# <div class='big'>
# {customers}
# </div>

# <div class='small'>
# Total Customers
# </div>

# </div>

# """,unsafe_allow_html=True)




# with c2:



#     st.markdown(f"""

# <div class='card'>


# <div class='big'>

# {churn_rate}%


# </div>


# <div class='small'>

# Churn Rate


# </div>


# </div>

# """,unsafe_allow_html=True)




# with c3:


#     st.markdown(f"""

# <div class='card'>


# <div class='big'>

# {retention_rate}%


# </div>


# <div class='small'>

# Retention Rate


# </div>


# </div>

# """,unsafe_allow_html=True)



# st.divider()



# ############################################
# # SEGMENTATION
# ############################################



# st.subheader("🎯 Customer Segmentation")


# col1,col2,col3=st.columns(3)


# col1.info(

# f"""

# Highest Churn Contract


# **{high_contract}**

# """
# )


# col2.warning(

# f"""

# Highest Churn Payment


# **{high_payment}**

# """
# )


# col3.error(

# f"""

# Highest Churn Internet


# **{high_internet}**

# """
# )



# st.divider()



# ############################################
# # BUSINESS RECOMMENDATIONS
# ############################################


# st.subheader("📌 Retention Recommendations")



# if month_percent>40:


#     st.warning(

# f"""

# 📄 **{month_percent}%** customers use Month-to-Month contracts.



# ### Recommendation


# • Promote yearly plans


# • Offer 10% annual discounts


# • Bundle streaming services


# """
# )




# if fiber_percent>50:


#     st.warning(

# f"""

# 🌐 **{fiber_percent}%** of churned customers use Fiber Optic.



# ### Recommendation


# • Improve service reliability


# • Dedicated support


# • Faster complaint resolution


# """
# )




# if electronic_percent>30:


#     st.info(

# f"""

# 💳 **{electronic_percent}%** churners use Electronic Check.



# ### Recommendation


# • Auto-pay incentives


# • Cashback offers


# • Simplified billing


# """
# )




# st.success(

# """

# 🎁 Loyalty Program Suggestions



# • Reward customers with tenure > 24 months


# • Free upgrades


# • Streaming subscriptions


# • Priority support


# • Anniversary discounts



# """
# )



# st.divider()



# ############################################
# # CHURN RISK SCORE
# ############################################



# st.subheader("⚠ Overall Churn Risk")



# if churn_rate>30:


#     st.error("HIGH CHURN RISK")


# elif churn_rate>20:


#     st.warning("MEDIUM CHURN RISK")


# else:


#     st.success("LOW CHURN RISK")



# st.divider()



# ############################################
# # EXECUTIVE SUMMARY
# ############################################



# st.subheader("📊 Executive Summary")



# st.markdown(f"""

# ### Business Problem

# Telecom companies lose customers every month.


# ### Current Situation


# • Total Customers : **{customers}**

# • Churn Rate : **{churn_rate}%**

# • Retention Rate : **{retention_rate}%**


# ### High-Risk Segment


# • Contract Type : **{high_contract}**

# • Payment Method : **{high_payment}**

# • Internet Service : **{high_internet}**


# ### Suggested Actions


# ✔ Personalized Offers

# ✔ Annual Contract Discounts

# ✔ Loyalty Programs

# ✔ Customer Service Improvements

# ✔ Auto-Pay Incentives


# ### Business Goal


# Increase retention by **5–10%** over the next quarter through targeted retention campaigns.


# """)



import streamlit as st
import pandas as pd

from ui import load_css
load_css()

st.set_page_config(
    page_title="Retention Insights",
    layout="wide"
)

############################################
# MODERN CSS (SAAS STYLE - MATCH DASHBOARD)
############################################
st.markdown("""
<style>

.main {
    background: linear-gradient(180deg, #F5F7FB, #EEF2FF);
}

/* Title */
h1 {
    font-size: 38px !important;
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

/* Section title */
.section-title {
    font-size: 20px;
    font-weight: 800;
    color: #0f172a;
    margin: 25px 0 15px 0;
    border-left: 5px solid #2563eb;
    padding-left: 10px;
}

/* KPI CARD */
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

/* BIG NUMBER */
.big {
    font-size: 34px;
    font-weight: 900;
    color: #2563eb;
}

/* SMALL LABEL */
.small {
    font-size: 15px;
    color: #64748b;
}

/* INFO BOX CARD */
.block-card {
    padding: 18px;
    border-radius: 15px;
    background: white;
    box-shadow: 0 6px 18px rgba(0,0,0,0.06);
}

/* Divider spacing */
hr {
    margin: 30px 0;
}

</style>
""", unsafe_allow_html=True)

############################################
# TITLE
############################################
st.markdown("""
# 💡 Customer Retention Insights
<div class="subtitle">
AI-powered analysis for churn reduction and customer behavior insights
</div>
""", unsafe_allow_html=True)

############################################
# LOAD DATA
############################################
df = pd.read_csv("data/WA_Fn-UseC_-Telco-Customer-Churn.csv")

df["TotalCharges"] = pd.to_numeric(df["TotalCharges"], errors="coerce")
df.dropna(inplace=True)

############################################
# KPIS (UNCHANGED LOGIC)
############################################
customers = len(df)

churned = len(df[df["Churn"] == "Yes"])

retained = customers - churned

churn_rate = round(churned / customers * 100, 2)

retention_rate = round(retained / customers * 100, 2)

############################################
# SEGMENTS (UNCHANGED LOGIC)
############################################
high_contract = (
    df[df['Churn'] == 'Yes']['Contract']
    .value_counts()
    .idxmax()
)

high_payment = (
    df[df['Churn'] == 'Yes']['PaymentMethod']
    .value_counts()
    .idxmax()
)

high_internet = (
    df[df['Churn'] == 'Yes']['InternetService']
    .value_counts()
    .idxmax()
)

############################################
# EXTRA METRICS (UNCHANGED LOGIC)
############################################
month_percent = round(
    (df["Contract"].value_counts()["Month-to-month"] / customers) * 100,
    2
)

fiber = len(df[(df["InternetService"] == "Fiber optic") & (df["Churn"] == "Yes")])

fiber_percent = round(fiber / churned * 100, 2)

electronic = len(df[(df["PaymentMethod"] == "Electronic check") & (df["Churn"] == "Yes")])

electronic_percent = round(electronic / churned * 100, 2)

############################################
# KPI CARDS
############################################
c1, c2, c3 = st.columns(3)

cards = [
    (customers, "Total Customers"),
    (churn_rate, "Churn Rate %"),
    (retention_rate, "Retention Rate %")
]

for col, data in zip([c1, c2, c3], cards):
    value, label = data
    with col:
        st.markdown(f"""
        <div class="card">
            <div class="big">{value}</div>
            <div class="small">{label}</div>
        </div>
        """, unsafe_allow_html=True)

############################################
# SEGMENTATION
############################################
st.markdown("<div class='section-title'>🎯 Customer Segmentation</div>", unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown(f"""
    <div class="block-card">
    <b>🔥 Highest Churn Contract</b><br><br>
    <span style="color:#2563eb;font-weight:700;font-size:18px">{high_contract}</span>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
    <div class="block-card">
    <b>💳 Highest Churn Payment</b><br><br>
    <span style="color:#2563eb;font-weight:700;font-size:18px">{high_payment}</span>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown(f"""
    <div class="block-card">
    <b>🌐 Highest Churn Internet</b><br><br>
    <span style="color:#2563eb;font-weight:700;font-size:18px">{high_internet}</span>
    </div>
    """, unsafe_allow_html=True)

############################################
# RECOMMENDATIONS
############################################
st.markdown("<div class='section-title'>📌 Retention Recommendations</div>", unsafe_allow_html=True)

if month_percent > 40:
    st.markdown(f"""
    <div class="block-card">
    <b>📄 Contract Insight</b><br><br>
    {month_percent}% customers use Month-to-Month contracts.<br><br>
    <b>Actions:</b><br>
    • Promote yearly plans<br>
    • Offer discounts<br>
    • Bundle services
    </div>
    """, unsafe_allow_html=True)

if fiber_percent > 50:
    st.markdown(f"""
    <div class="block-card">
    <b>🌐 Fiber Optic Risk</b><br><br>
    {fiber_percent}% churners use Fiber Optic.<br><br>
    <b>Actions:</b><br>
    • Improve service stability<br>
    • Faster complaint resolution<br>
    • Dedicated support
    </div>
    """, unsafe_allow_html=True)

if electronic_percent > 30:
    st.markdown(f"""
    <div class="block-card">
    <b>💳 Payment Insight</b><br><br>
    {electronic_percent}% churners use Electronic Check.<br><br>
    <b>Actions:</b><br>
    • Auto-pay incentives<br>
    • Cashback offers<br>
    • Billing simplification
    </div>
    """, unsafe_allow_html=True)

############################################
# RISK LEVEL
############################################
st.markdown("<div class='section-title'>⚠ Churn Risk Level</div>", unsafe_allow_html=True)

if churn_rate > 30:
    st.error("HIGH CHURN RISK 🚨")
elif churn_rate > 20:
    st.warning("MEDIUM CHURN RISK ⚠")
else:
    st.success("LOW CHURN RISK ✅")

############################################
# EXECUTIVE SUMMARY
############################################
st.markdown("<div class='section-title'>📊 Executive Summary</div>", unsafe_allow_html=True)

st.markdown(f"""
<div class="block-card">

<b>Business Overview</b><br><br>

• Total Customers: {customers}<br>
• Churn Rate: {churn_rate}%<br>
• Retention Rate: {retention_rate}%<br><br>

<b>High Risk Segments</b><br>
• Contract: {high_contract}<br>
• Payment: {high_payment}<br>
• Internet: {high_internet}<br><br>

<b>Goal</b><br>
Improve retention by 5–10% using AI-driven targeting strategies.

</div>
""", unsafe_allow_html=True)