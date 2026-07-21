import streamlit as st

st.set_page_config(
    page_title="Customer Churn Platform",
    layout="wide",
    initial_sidebar_state="expanded"
)

###############################################
# CSS
###############################################

st.markdown("""
<style>

.stApp{
background-color:#F5F7FA;
}


/* Sidebar */

[data-testid="stSidebar"]{
background:#172554;
}


[data-testid="stSidebar"] *{
color:white;
}



/* Hero Section */
.hero{
    padding:70px 50px;
    border-radius:25px;
    background: linear-gradient(135deg,#0F172A,#1E3A8A,#2563EB,#38BDF8);
    color:white;
    text-align:center;
    box-shadow:0 10px 30px rgba(0,0,0,0.2);
    margin-bottom:30px;
}
.hero-title{
    font-size:58px;
    font-weight:900;
    margin:0;
    line-height:1.2;

    background: linear-gradient(90deg,#ffffff,#dbeafe,#93c5fd);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;

    letter-spacing:1px;
}

.hero h1{

font-size:52px;

font-weight:800;

margin-bottom:10px;
font-weight:bold;


}


.hero p{

font-size:22px;

opacity:.95;

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

font-size:30px;

font-weight:700;

margin-top:40px;

margin-bottom:20px;

}




/* Feature Cards */

.card{


background:white;


padding:30px;


border-radius:20px;


box-shadow:0 4px 15px rgba(0,0,0,.08);


min-height:260px;


transition:.3s;


}


.card:hover{


transform:translateY(-8px);


box-shadow:0 10px 25px rgba(0,0,0,.15);


}



.card h3{


margin-bottom:20px;


}


.card p{


line-height:1.8;


font-size:17px;


}



/* Stats */


.stat{


background:white;


padding:25px;


border-radius:18px;


text-align:center;


box-shadow:0px 3px 15px rgba(0,0,0,.08);


}



.number{


font-size:38px;


font-weight:bold;


color:#2563EB;


}



.label{


font-size:17px;


color:gray;


}




/* Workflow */


.workflow{


padding:30px;


border-radius:20px;


background:white;


box-shadow:0px 4px 15px rgba(0,0,0,.08);


text-align:center;


font-size:24px;


line-height:2.3;


}



/* Footer */


.footer{


padding:25px;


border-radius:20px;


background:#DBEAFE;


font-size:18px;


margin-top:30px;


}


</style>

""",unsafe_allow_html=True)



#################################################
# HERO
#################################################

st.markdown(
"""
<div class="hero">
<div class="hero-title">🚀 Customer Churn Prediction Platform</div>

<div class="tag">AI Powered Retention Analytics</div>

<div class="hero-text">
Helping telecom companies understand customer behavior,
predict churn, and create smarter retention strategies.
</div>
</div>
""",
unsafe_allow_html=True
)


#################################################
# CARDS
#################################################

st.markdown(
"<div class='section'>✨ Why This Platform?</div>",
unsafe_allow_html=True
)


c1,c2,c3 = st.columns(3)



with c1:

    st.markdown("""

<div class='card'>


<h3>😔 Business Problem</h3>



<p>


Telecom companies lose customers every month.



Customer attrition impacts revenue and increases customer acquisition costs.



Businesses struggle to identify customers likely to leave.


</p>


</div>

""",unsafe_allow_html=True)




with c2:


    st.markdown("""

<div class='card'>


<h3>🧠 AI Solution</h3>



<p>

✔ Contract Analysis


✔ Payment History


✔ Monthly Usage Patterns


✔ Internet Service Analysis


✔ Churn Risk Detection


</p>



</div>

""",unsafe_allow_html=True)




with c3:


    st.markdown("""

<div class='card'>


<h3>🎯 Platform Features</h3>



<p>


✔ Customer Segmentation


✔ Interactive Dashboard


✔ Predictions


✔ Retention Insights


✔ Export Reports


</p>



</div>

""",unsafe_allow_html=True)




#################################################
# Statistics
#################################################

st.markdown(
"<div class='section'>📊 Platform Statistics</div>",
unsafe_allow_html=True
)


s1,s2,s3,s4 = st.columns(4)



stats=[

("7043","Customers"),

("21","Features"),

("AI","Prediction Ready"),

("CSV","Export Reports")

]


for col,data in zip([s1,s2,s3,s4],stats):

    num,label=data

    with col:


        st.markdown(f"""

<div class='stat'>


<div class='number'>

{num}

</div>



<div class='label'>

{label}

</div>



</div>


""",unsafe_allow_html=True)




st.markdown("<div class='section'>🔄 Customer Retention Workflow</div>", unsafe_allow_html=True)

workflow_steps = [
    ("📂", "Upload Dataset"),
    ("🧹", "Clean & Preprocess Data"),
    ("📊", "Exploratory Analysis"),
    ("🤖", "Train Churn Model"),
    ("⚡", "Predict Churn Risk"),
    ("💡", "Generate Insights"),
    ("📄", "Export Report")
]

cols = st.columns(len(workflow_steps))

for i, col in enumerate(cols):
    icon, label = workflow_steps[i]

    with col:
        st.markdown(f"""
        <div style="
            background:white;
            padding:20px;
            border-radius:18px;
            text-align:center;
            box-shadow:0 4px 15px rgba(0,0,0,0.08);
            height:140px;
            display:flex;
            flex-direction:column;
            justify-content:center;
            transition:0.3s;
        ">
            <div style="font-size:30px;">{icon}</div>
            <div style="margin-top:10px; font-weight:600; font-size:15px;">
                {label}
            </div>
        </div>
        """, unsafe_allow_html=True)



#################################################
# Footer
#################################################

st.markdown("""

<div class='footer'>


<h3>💙 Our Mission</h3>



Help telecom providers move from reacting to customer churn
to proactively preventing it through AI-driven analytics,
customer segmentation, and personalized retention strategies.



</div>

""",unsafe_allow_html=True)