# app.py
import streamlit as st
import io
from Track import count_and_list_contents, stop_flag

st.title("Data")
st.session_state.log_messages = []
log_output = io.StringIO()

# Function to capture log messages
def log_callback(message):
    log_output.write(message + "\n")
    if "log_messages" not in st.session_state:
    st.session_state.log_messages = []
    st.session_state.log_messages.append(message)

# Define a function to start counting and listing contents
def start_count_and_list():
    global stop_flag
    stop_flag = False
    st.write("Calling count_and_list_contents function...")
    result = count_and_list_contents('cctv_footages',log_callback)
    if "error" in result:
        st.error(result["error"])
    else:
        st.write("Roots:")
        st.write(result["roots"])
        st.write("Directories:")
        st.write(result["dirs"])
        st.write("Files:")
        st.write(result["files"])

# Sidebar message
st.sidebar.success("Select a page above.")

# Session state for text input
if "my_input" not in st.session_state:
    st.session_state["my_input"] = ""

# Text input field
my_input = st.text_input("Input a text", st.session_state["my_input"])
submit = st.button("Submit")

# Handle text input submission
if submit:
    st.session_state["my_input"] = my_input
    st.write("You have entered", my_input)

# Button to start the function
if st.button("Start Function"):
    start_count_and_list()

# Button to stop the function
if st.button("Stop Function"):
    stop_flag = True
    st.write("Stop Signal sent.")
