import streamlit as st
import pandas as pd
from ui import load_css
load_css()

st.set_page_config(
    page_title="Export Reports",
    layout="wide"
)


##########################################
# CSS
##########################################

st.markdown("""

<style>

.card{

padding:20px;

border-radius:15px;

background:white;

box-shadow:0px 2px 10px rgba(0,0,0,0.1);

text-align:center;

margin-bottom:20px;

}


.big{

font-size:28px;

font-weight:bold;

color:#1f77b4;

}


.small{

font-size:16px;

color:gray;

}

</style>

""",unsafe_allow_html=True)



##########################################
# Title
##########################################

st.title("⬇ Export Reports")


##########################################
# Load Dataset
##########################################

df = pd.read_csv(

'data/WA_Fn-UseC_-Telco-Customer-Churn.csv'

)


df['TotalCharges']=pd.to_numeric(

df['TotalCharges'],

errors='coerce'

)

df.dropna(inplace=True)



##########################################
# Metrics
##########################################

customers=len(df)

churned=len(

df[df['Churn']=='Yes']

)

retained=len(

df[df['Churn']=='No']

)



##########################################
# KPI Cards
##########################################


c1,c2,c3=st.columns(3)


cards=[

(customers,"Customers"),

(churned,"Churned"),

(retained,"Retained")

]


for col,data in zip(

[c1,c2,c3],

cards

):


    value,name=data


    with col:


        st.markdown(f"""

<div class='card'>


<div class='big'>

{value}

</div>


<div class='small'>

{name}

</div>


</div>


""",

unsafe_allow_html=True

)



##########################################
# Preview
##########################################


st.subheader("Dataset Preview")


st.dataframe(

df.head(10),

use_container_width=True

)



##########################################
# Downloads
##########################################


st.subheader("Download Reports")



full_csv=df.to_csv(

index=False

)



churned_csv=(

df[df['Churn']=='Yes']

.to_csv(index=False)

)



retained_csv=(

df[df['Churn']=='No']

.to_csv(index=False)

)



col1,col2,col3=st.columns(3)



with col1:


    st.download_button(

        label="📄 Full Dataset",

        data=full_csv,

        file_name="customers.csv",

        mime="text/csv"

    )




with col2:


    st.download_button(

        label="⚠ Churned Customers",

        data=churned_csv,

        file_name="churned_customers.csv",

        mime="text/csv"

    )




with col3:


    st.download_button(

        label="✅ Retained Customers",

        data=retained_csv,

        file_name="retained_customers.csv",

        mime="text/csv"

    )



##########################################
# Report Summary
##########################################


st.divider()


st.subheader("Report Summary")


st.info(f"""

### Available Exports


• Full Customer Dataset

• Churned Customers List

• Retained Customers List



### Statistics


Total Customers : **{customers}**

Churned : **{churned}**

Retained : **{retained}**



These reports can be shared with the ML team,
business analysts, or management for further
customer retention planning.


""")