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


/* ============ SIDEBAR REDESIGN ============ */

[data-testid="stSidebar"]{
    background: linear-gradient(180deg, #0F172A 0%, #172554 100%);
    border-right: 1px solid rgba(255,255,255,0.06);
}

[data-testid="stSidebar"] *{
    color:white;
}

section[data-testid="stSidebar"] {
    width: 300px !important;
}
section[data-testid="stSidebar"] > div {
    width: 300px !important;
    padding: 0 !important;
}

/* Hide default Streamlit page navigation */
[data-testid="stSidebarNav"] {
    display: none;
}

/* Brand / logo header */
.sidebar-brand{
    display:flex;
    align-items:center;
    gap:12px;
    padding:28px 22px 22px 22px;
    border-bottom:1px solid rgba(255,255,255,0.08);
    margin-bottom:18px;
}
.sidebar-brand-icon{
    width:42px;
    height:42px;
    border-radius:12px;
    background:linear-gradient(135deg,#2563EB,#38BDF8);
    display:flex;
    align-items:center;
    justify-content:center;
    font-size:20px;
    box-shadow:0 4px 12px rgba(37,99,235,0.4);
    flex-shrink:0;
}
.sidebar-brand-text{
    line-height:1.25;
}
.sidebar-brand-title{
    font-size:15.5px;
    font-weight:800;
    color:white;
}
.sidebar-brand-sub{
    font-size:12px;
    color:#94A3B8;
    font-weight:500;
}

/* Nav section label */
.sidebar-section-label{
    font-size:11.5px;
    font-weight:700;
    color:#64748B;
    text-transform:uppercase;
    letter-spacing:1px;
    padding:0 22px;
    margin:6px 0 10px 0;
}

/* Nav link container padding */
[data-testid="stSidebar"] .element-container:has(.stPageLink) {
    padding: 0 14px;
}

/* Sidebar page links */
[data-testid="stSidebar"] .stPageLink a {
    display:flex;
    align-items:center;
    gap:10px;
    padding:13px 16px;
    margin:4px 0;
    border-radius:12px;
    font-size:15px;
    font-weight:600;
    color:#CBD5E1 !important;
    background:transparent;
    transition:all 0.25s ease;
    border:1px solid transparent;
}

[data-testid="stSidebar"] .stPageLink a:hover {
    background:rgba(37,99,235,0.18);
    border:1px solid rgba(56,189,248,0.25);
    color:white !important;
    transform:translateX(6px);
}

/* Sidebar footer */
.sidebar-footer{
    position:absolute;
    bottom:0;
    left:0;
    right:0;
    padding:18px 22px;
    border-top:1px solid rgba(255,255,255,0.08);
    font-size:12px;
    color:#64748B;
    text-align:center;
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



/* How It Works */

.step-card{
    background:white;
    padding:28px 24px;
    border-radius:20px;
    box-shadow:0 4px 15px rgba(0,0,0,.08);
    min-height:230px;
    position:relative;
    transition:.3s;
}

.step-card:hover{
    transform:translateY(-6px);
    box-shadow:0 10px 25px rgba(0,0,0,.15);
}

.step-num{
    width:46px;
    height:46px;
    border-radius:50%;
    background:linear-gradient(135deg,#1E3A8A,#38BDF8);
    color:white;
    display:flex;
    align-items:center;
    justify-content:center;
    font-weight:800;
    font-size:18px;
    margin-bottom:18px;
}

.step-card h4{
    font-size:19px;
    margin-bottom:10px;
    color:#0F172A;
}

.step-card p{
    font-size:15.5px;
    line-height:1.6;
    color:#475569;
}

.step-connector{
    text-align:center;
    color:#93C5FD;
    font-size:26px;
    padding-top:70px;
}



/* Risk Overview */

.risk-card{
    padding:28px;
    border-radius:20px;
    text-align:center;
    box-shadow:0 4px 15px rgba(0,0,0,.08);
    transition:.3s;
    border-left:6px solid;
}

.risk-card:hover{
    transform:translateY(-6px);
    box-shadow:0 10px 25px rgba(0,0,0,.15);
}

.risk-high{ background:#FEF2F2; border-color:#EF4444; }
.risk-medium{ background:#FFFBEB; border-color:#F59E0B; }
.risk-low{ background:#F0FDF4; border-color:#22C55E; }

.risk-count{
    font-size:40px;
    font-weight:800;
}

.risk-high .risk-count{ color:#DC2626; }
.risk-medium .risk-count{ color:#D97706; }
.risk-low .risk-count{ color:#16A34A; }

.risk-label{
    font-size:16px;
    font-weight:600;
    color:#334155;
    margin-top:6px;
}

.risk-sub{
    font-size:13.5px;
    color:#64748B;
    margin-top:4px;
}


/* Feature Grid */

.feature-card{
    background:white;
    padding:26px;
    border-radius:20px;
    box-shadow:0 4px 15px rgba(0,0,0,.08);
    height:170px;
    display:flex;
    flex-direction:column;
    justify-content:center;
    transition:.3s;
}

.feature-card:hover{
    transform:translateY(-6px);
    box-shadow:0 10px 25px rgba(0,0,0,.15);
}

.feature-icon{
    font-size:28px;
    margin-bottom:10px;
}

.feature-card h4{
    font-size:17px;
    color:#0F172A;
    margin-bottom:6px;
}

.feature-card p{
    font-size:14px;
    color:#64748B;
    line-height:1.5;
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






</style>

""",unsafe_allow_html=True)


with st.sidebar:

    st.markdown("""
    <div class="sidebar-brand">
        <div class="sidebar-brand-icon">🚀</div>
        <div class="sidebar-brand-text">
            <div class="sidebar-brand-title">Churn Platform</div>
            <div class="sidebar-brand-sub">AI Retention Analytics</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<div class='sidebar-section-label'>Navigation</div>", unsafe_allow_html=True)

    st.page_link(
        "Home.py",
        label="  Home"
    )

    st.page_link(
        "pages/Prediction.py",
        label="  Prediction"
    )

    
#################################################
# HERO
#################################################

st.markdown(
"""
<div class="hero">
<div class="hero-title">🚀 Customer Churn Prediction Platform</div>

<div class="tag">AI Powered Retention Analytics</div>


</div>
""",
unsafe_allow_html=True
)


#################################################
# HOW IT WORKS
#################################################

st.markdown(
"<div class='section'>⚙️ How It Works</div>",
unsafe_allow_html=True
)

steps = [
    ("1", "Upload Your Data", "Bring in your customer dataset — contracts, billing history, usage, and service details — with a simple CSV upload."),
    ("2", "AI Analyzes Patterns", "The model scans payment behavior, tenure, and service usage to spot the signals that precede churn."),
    ("3", "Get Risk Scores", "Every customer is scored by churn probability, so you instantly see who's most likely to leave."),
    ("4", "Act on Insights", "Segment at-risk customers and export retention reports your team can act on right away."),
]

cols = st.columns(len(steps))

for col, (num, title, desc) in zip(cols, steps):
    with col:
        st.markdown(f"""
        <div class='step-card'>
            <div class='step-num'>{num}</div>
            <h4>{title}</h4>
            <p>{desc}</p>
        </div>
        """, unsafe_allow_html=True)




#################################################
# Live Churn Risk Overview
#################################################

st.markdown(
"<div class='section'>🚦 Live Churn Risk Overview</div>",
unsafe_allow_html=True
)

r1, r2, r3 = st.columns(3)

risk_data = [
    ("risk-high", "1,142", "High Risk", "Likely to churn within 30 days"),
    ("risk-medium", "2,015", "Medium Risk", "Showing early warning signals"),
    ("risk-low", "3,886", "Low Risk", "Stable, engaged customers"),
]

for col, (css_class, count, label, sub) in zip([r1, r2, r3], risk_data):
    with col:
        st.markdown(f"""
        <div class='risk-card {css_class}'>
            <div class='risk-count'>{count}</div>
            <div class='risk-label'>{label}</div>
            <div class='risk-sub'>{sub}</div>
        </div>
        """, unsafe_allow_html=True)




st.markdown("<div class='section'>🎯 Key Platform Features</div>", unsafe_allow_html=True)

features = [
    ("🧩", "Customer Segmentation", "Group customers by risk level, tenure, and value to target retention efforts."),
    ("📈", "Interactive Dashboard", "Explore churn trends and customer patterns in real time."),
    ("🔮", "Predictions", "Get churn probability scores for every customer in your dataset."),
    ("💡", "Retention Insights", "Surface the drivers behind churn so teams know what to fix."),
    ("📤", "Export Reports", "Download clean, shareable reports for stakeholders and campaigns."),
]

cols = st.columns(len(features))

for col, (icon, title, desc) in zip(cols, features):
    with col:
        st.markdown(f"""
        <div class='feature-card'>
            <div class='feature-icon'>{icon}</div>
            <h4>{title}</h4>
            <p>{desc}</p>
        </div>
        """, unsafe_allow_html=True)



