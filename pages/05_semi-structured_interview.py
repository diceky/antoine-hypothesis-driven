import json
from datetime import datetime

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

open(f"results/{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.json", "x").write(
    json.dumps(st.session_state["results"], default=str)
)

with st.sidebar:
    st.header("Debug")
    st.write(st.session_state)
