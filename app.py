import streamlit as st

from openai import OpenAI

from config import OPENAI_MODELS, Group
from utils import page_setup, save_widget, get_client, get_group


#######################################
# SETUP
#######################################


page_setup("Setup")

if "results" not in st.session_state:
    st.session_state["results"] = {}

if "group" not in st.session_state["results"]:
    st.session_state["results"]["group"] = None

if 'client' not in st.session_state:
    st.session_state['client'] = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])


#######################################
# MAIN
#######################################


st.title("Setup")

st.divider()

st.checkbox("PICF is signed")
st.checkbox("Laptop is charged")
st.checkbox("Screen-recording is setup on Zoom")
st.checkbox("Audio-recording is setup on Zoom and on phone")

st.divider()

st.selectbox(
    "Which group is the participant in?",
    Group,
    format_func=(lambda x:
                 {Group.CONTROL: "Control",
                  Group.HYPOTHESIS_DRIVEN: "Hypothesis-driven AI",
                  Group.RECOMMENDATIONS_DRIVEN: "Recommendations-driven AI"}
                 [x]),
    index=None,
    key="group")

model = st.radio(
    label="Which model should be used?",
    options=OPENAI_MODELS,
    index=None,
    format_func=lambda s: f"`{s}`",
    key="model")

st.divider()

if st.button(
    "Start Experiment",
    disabled=(
        st.session_state['group'] is None
        or st.session_state['model'] is None)):

    # Save the results
    save_widget("group")
    save_widget("model")

    # Setup AI assistant
    if get_group() is Group.CONTROL:
        st.session_state['assistant'] = None
    else:
        assistant_id = st.secrets[
            f"OPENAI_{get_group().name}_ASSISTANT_ID"]
        st.session_state['assistant'] = (
            get_client().beta.assistants.retrieve(assistant_id)
        )

    # Switch to the next page
    st.switch_page("pages/01_domain_AI_expertise_questionnaire.py")

with st.sidebar:
    st.header("Debug")
    st.write(st.session_state)
