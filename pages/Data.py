import streamlit as st
from Track import count_and_list_contents 

st.title("Data")

st.sidebar.success("Select a page above.")


if "my_input" not in st.session_state:
    st.session_state["my_input"] = ""
    
my_input =  st.text_input("Input a a text", st.session_state["my_input"])
submit = st.button("Submit")

if submit:
    st.session_state["my_input"] = my_input
    st.write("You have entered" ,my_input)
    count_and_list_contents('cctv_footages')
