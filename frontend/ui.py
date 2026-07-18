import streamlit as st

def load_css():
    st.markdown("""
    <style>
    [data-testid="stSidebar"]{
    background:#172554;
}
    [data-testid="stSidebar"] *{
    color:white;
}
    </style>
    """, unsafe_allow_html=True)