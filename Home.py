import streamlit as st

st.set_page_config(
    page_title="Tom.Camp Data",
    page_icon=":house:",
    layout="wide",
    initial_sidebar_state="expanded",
)

with open("README.md", "r") as fp:
    page_body = fp.read()

st.markdown(page_body, unsafe_allow_html=True)
