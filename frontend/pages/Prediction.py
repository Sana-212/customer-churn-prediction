import streamlit as st
import pandas as pd
from ui import load_css
load_css()

st.title("🤖 Predictions")

predictions = pd.DataFrame({

    "CustomerID":[1,2,3],

    "Probability":[0.92,0.65,0.12],

    "Risk":[
        "High",
        "Medium",
        "Low"
    ]
})

st.dataframe(predictions)