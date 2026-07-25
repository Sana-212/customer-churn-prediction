import streamlit as st
import pandas as pd
from ui import load_css
load_css()

st.set_page_config(
    page_title="Upload Dataset",
    layout="wide"
)


#################################################
# CSS
#################################################

st.markdown("""

<style>

.card{
padding:20px;
border-radius:15px;
background:white;
box-shadow:0px 2px 10px rgba(0,0,0,.1);
text-align:center;
margin-bottom:20px;
}


.big{
font-size:30px;
font-weight:bold;
color:#1f77b4;
}


.small{
font-size:17px;
color:gray;
}


</style>

""",unsafe_allow_html=True)



#################################################

st.title("📂 Upload Customer Dataset")

st.write(
"Upload a telecom customer CSV file to explore and analyze churn patterns."
)

#################################################

uploaded_file = st.file_uploader(

"Choose CSV File",

type=['csv']

)


#################################################

if uploaded_file:


    df = pd.read_csv(uploaded_file)


    st.success(
        "Dataset Uploaded Successfully"
    )


#################################################
# KPIs
#################################################

    rows=df.shape[0]

    columns=df.shape[1]

    missing=df.isnull().sum().sum()



    c1,c2,c3=st.columns(3)



    cards=[

        (rows,"Rows"),

        (columns,"Columns"),

        (missing,"Missing Values")

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

unsafe_allow_html=True)




#################################################
# Preview
#################################################

    st.subheader("📄 Dataset Preview")


    st.dataframe(

        df.head(10),

        use_container_width=True

    )



#################################################
# Column Information
#################################################

    st.subheader("📝 Column Details")


    info = pd.DataFrame({


        "Column":

            df.columns,


        "Data Type":

            df.dtypes.astype(str),



        "Missing Values":

            df.isnull().sum()


    })




    st.dataframe(

        info,

        use_container_width=True

    )



#################################################
# Statistics
#################################################

    st.subheader("📊 Statistical Summary")


    st.dataframe(

        df.describe(),

        use_container_width=True

    )



#################################################
# Missing Values
#################################################

    st.subheader("⚠ Missing Values")


    miss=df.isnull().sum()



    miss=miss[miss>0]



    if len(miss)>0:



        st.dataframe(

            miss,

            use_container_width=True

        )



    else:



        st.success(

            "No Missing Values Found"

        )



#################################################

else:


    st.info(

        "Please upload a CSV file to begin analysis."

    )