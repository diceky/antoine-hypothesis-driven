import streamlit as st
import pandas as pd
import time

from datetime import datetime

from utils import (
    page_setup,
    save_widget,
    get_case_index,
    get_case_description,
    get_group,
    get_case_description_with_citations,
    on_hypotheses_change,
    get_hypotheses,
    get_ai_prompt,
    get_run_and_thread_id,
    get_run_status,
    get_latest_message_content,
    parse_citations_from_message)

from config import Group

#######################################
# SETUP
#######################################


page_setup("Case")

if "case_index" not in st.session_state:
    st.session_state["case_index"] = 0

if "citations" not in st.session_state:
    st.session_state["citations"] = None

if f"case_{get_case_index()}_start_time" not in st.session_state["results"]:
    st.session_state["results"][f"case_{get_case_index()}_start_time"] = \
        datetime.now().time()


#######################################
# DISPLAYS
#######################################


def display_case_description():
    if st.session_state['citations'] is not None:
        st.write(get_case_description_with_citations())
    else:
        st.write(get_case_description())


def display_hypothesis_input(group: Group, key: str):
    columns = ["hypothesis"]
    column_config = {
            "hypothesis": st.column_config.TextColumn(
                "Your hypotheses:",
                help="Enter your hypotheses here.",
                required=True,
                validate="^[A-Za-z0-9 -]+$"
            )
        }

    if group is Group.HYPOTHESIS_DRIVEN:
        columns.append("selected")
        column_config["selected"] = st.column_config.CheckboxColumn(
            "Select?",
            help="Select the hypotheses you want to investigate further.",
            default=False,
            required=True,
        )

    df = pd.DataFrame(columns=columns)
    st.data_editor(
        df,
        column_config=column_config,
        use_container_width=True,
        num_rows='dynamic',
        on_change=on_hypotheses_change,
        key=key)


def display_ai_help(
        group: Group,
        case_description: str,
        hypotheses_table: dict):

    if group is Group.CONTROL:
        st.write(
            "You are in the control group. You will not receive any AI help.")
        return

    hypotheses = get_hypotheses(group, hypotheses_table)

    status_container = st.status(
        label="",
        expanded=False,
        state="running")

    if group is Group.HYPOTHESIS_DRIVEN:
        if len(hypotheses) == 0:
            status_container.update(
                label="Please select at least one hypothesis.",
                expanded=False,
                state="error")
            return
    if group is Group.RECOMMENDATIONS_DRIVEN:
        if len(hypotheses) < 2:
            status_container.update(
                label="Please add at least two hypotheses.",
                expanded=False,
                state="error")
            return

    # Add message to a new thread and run it
    # Because function is cached, this will only run once per prompt
    thread_id, run_id = get_run_and_thread_id(
        get_ai_prompt(group, case_description, hypotheses)
    )

    status_container.update(
        label="Generating AI help...",
        expanded=False,
        state="running")
    with status_container:
        while get_run_status(thread_id, run_id) in ["queued", "in_progress"]:
            time.sleep(0.1)

    if get_run_status(thread_id, run_id) == "completed":
        status_container.update(
                label="AI's help is ready:",
                expanded=True,
                state="complete")
        with status_container:
            citations, parsed_message = parse_citations_from_message(
                get_latest_message_content(thread_id))
            st.write(parsed_message)
            display_citations(citations)
            st.session_state['parsed_message'] = parsed_message
            st.session_state['citations'] = citations
    else:
        status_container.update(
                label="Failed to generate AI help. Please try again.",
                expanded=False,
                state="error")


def display_citations(citations: list[str]):
    citations_string = ("**Citations:**\n\n"
                        if len(citations) > 0
                        else "No citations found.")
    for citation in citations:
        citations_string += f"{citations.index(citation) + 1}. {citation}\n\n"
    st.caption(citations_string)


@st.experimental_dialog("Are you done with the case?")  # type: ignore
def dialog_case_done():
    if st.button("Yes", type="primary"):

        st.session_state["results"][f"case_{get_case_index()}_end_time"] = \
            datetime.now().time()
        save_widget(
            "hypotheses_table",
            new_name=f"case_{get_case_index()}_hypotheses")

        st.switch_page("pages/03_case_questionnaire.py")


#######################################
# MAIN
#######################################


st.title(f"Case {get_case_index() + 1}")

case_description_container = st.container(height=300)

col1, col2 = st.columns([0.3, 0.7])

with col1:
    hypotheses_df = display_hypothesis_input(
        get_group(),
        key="hypotheses_table")

with col2:
    display_ai_help(
        get_group(),
        get_case_description(),
        st.session_state["hypotheses_table"])

# Because the case description depends on the AI message (citations) we need
# to compute it after the AI message.
with case_description_container:
    display_case_description()

st.divider()

if st.button("Next"):
    dialog_case_done()

with st.sidebar:
    st.header("Debug")
    st.write(st.session_state)