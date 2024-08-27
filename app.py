import streamlit as st
from openai import OpenAI

from config import OPENAI_MODELS, Group
from utils import get_group, page_setup, save_widget

#######################################
# SETUP
#######################################


page_setup("Setup")

if "results" not in st.session_state:
    st.session_state["results"] = {}

if "group" not in st.session_state["results"]:
    st.session_state["results"]["group"] = None

if "client" not in st.session_state:
    st.session_state["client"] = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])


#######################################
# MAIN
#######################################


st.title("Setup")

st.divider()

st.selectbox(
    "Which group is the participant in?",
    Group,
    format_func=(
        lambda x: {
            Group.CONTROL: "Control",
            Group.HYPOTHESIS_DRIVEN: "Hypothesis-driven AI",
            Group.RECOMMENDATIONS_DRIVEN: "Recommendations-driven AI",
        }[x]
    ),
    index=None,
    key="group",
)

model = st.radio(
    label="Which model should be used?",
    options=OPENAI_MODELS,
    index=2,
    format_func=lambda s: f"`{s}`",
    key="model",
)

if st.button(
    "Start Experiment",
    disabled=(st.session_state["group"] is None or st.session_state["model"] is None),
):

    # Save the results
    save_widget("group")
    save_widget("model")

    # Switch to the next page
    st.switch_page("pages/01_domain_AI_expertise_questionnaire.py")

with st.sidebar:
    st.header("Debug")
    st.write(st.session_state)
