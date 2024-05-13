import streamlit as st

from utils import page_setup

#######################################
# SETUP
#######################################


page_setup("Interview")


#######################################
# MAIN
#######################################

st.title("Semi-structured interview")

with st.sidebar:
    st.header("Debug")
    st.write(st.session_state)
