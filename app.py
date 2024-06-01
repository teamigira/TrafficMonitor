import streamlit as st

st.set_page_config(
    page_title="Traffic Counter",
    page_icon=":traffic_light:",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.title("Main Page")
st.sidebar.success("Select the above")