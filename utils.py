'''
This file contains utility functions that are used across the app.
'''

import streamlit as st
import re

from config import Group


def page_setup(page_title: str):
    """
    Setup the page with the given title. Optionally, show the debug sidebar.

    :param page_title: The title of the page.
    :param debug: Whether to show the debug sidebar.
    :return: None
    """
    st.set_page_config(
        page_title=page_title,
        page_icon='🔬',
        layout='wide',
        initial_sidebar_state='collapsed'
    )


def save_widget(key: str, new_name: str | None = None):
    """
    Save the data of an entry in the session state to the results dictionnary.

    :param widget_key: The key of the widget.
    :return: None
    """
    assert key in st.session_state, \
        f"{key} cannot be found in session_state"

    if new_name is not None:
        st.session_state['results'][new_name] = st.session_state[key]
    else:
        st.session_state['results'][key] = st.session_state[key]


#######################################
# CASE
#######################################


def get_case_index() -> int:
    return st.session_state["case_index"]


def get_case_description() -> str:
    return open(f"data/case_{get_case_index()}.txt", "r").read()


def get_case_description_with_citations() -> str:
    case_description = get_case_description()
    citations = st.session_state['citations']

    for citation in citations:
        case_description = case_description.replace(
            citation,
            f":red-background[{citation} \
                [{citations.index(citation) + 1}]]")

    return case_description


def get_group() -> Group:
    return st.session_state["results"]["group"]


def get_hypotheses(group: Group, hypotheses_table: dict) -> list[str]:
    if group is Group.HYPOTHESIS_DRIVEN:
        hypotheses = [h['hypothesis'] for h in hypotheses_table['added_rows']
                      if h["selected"] is True]

    if group is Group.RECOMMENDATIONS_DRIVEN:
        hypotheses = [h["hypothesis"] for h in hypotheses_table['added_rows']]

    return hypotheses


def on_hypotheses_change():
    st.toast("Hypotheses updated!")


@st.cache_data
def parse_citations_from_message(message: str) -> tuple[list[str], str]:

    citations = []

    def citation_replacer(match: re.Match[str]):
        # Extract the citation from the match
        citation = (match.group(0)
                    .removeprefix("{citation: ").removesuffix("}"))
        # Add the citation to the list if it's not already there
        if citation not in citations:
            citations.append(citation.removeprefix("{citation: '").removesuffix("'}"))
        # Replace with the citation index
        return f":red-background[[{citations.index(citation) + 1}]]"

    modified_message = re.sub(
        r"\{citation:.*?\}",
        citation_replacer,
        message)

    return citations, modified_message


#######################################
# OPENAI API
#######################################


def get_client():
    return st.session_state['client']


def get_model():
    return st.session_state['results']['model']


def get_assistant_id():
    return st.session_state['assistant'].id


@st.cache_data
def get_run_and_thread_id(prompt: str) -> tuple[str, str]:
    '''
    This function gets or creates a new thread and run in the OpenAI API
    and returns the thread_id and run_id. Because it is cached, it will
    only create a new thread and run once per prompt, otherwise just returning
    the already existing corresponding ids.

    :param prompt: The prompt to send to the AI.
    :return: A tuple containing the thread_id and run_id.
    '''
    run = get_client().beta.threads.create_and_run(
        assistant_id=get_assistant_id(),
        thread={
            "messages": [
                {
                    "role": "user",
                    "content": prompt,
                }
            ]
        },
        model=get_model(),
    )
    return (run.thread_id, run.id)


def get_run_status(thread_id, run_id):
    run = get_client().beta.threads.runs.retrieve(
        thread_id=thread_id,
        run_id=run_id,
    )
    return run.status


def get_latest_message_content(thread_id):
    return get_client().beta.threads.messages.list(
        thread_id,
        limit=1,
        order='desc'
    ).data[0].content[0].text.value


def get_ai_prompt(
        group: Group,
        case_description: str,
        hypotheses: list[str]) -> str:
    if group is Group.HYPOTHESIS_DRIVEN:
        if len(hypotheses) == 1:
            return f"""
            Your task is to please provide both evidence for and against
            the given hypothesis.

            <case_description>{case_description}</case_description>
            <hypotheses>{hypotheses[0]}</hypotheses>"""

        if len(hypotheses) > 1:
            return f"""
            Your task is to compare the given hypotheses, providing evidence
            for and against each of them to help discriminate between them, but
            do not ever - EVER - recommend one hypothesis over the other(s).

            <case_description>{case_description}</case_description>
            <hypotheses>{'\n'.join(hypotheses)}</hypotheses>"""
    if group is Group.RECOMMENDATIONS_DRIVEN:
        return f"""
        <case_description>{case_description}</case_description>
        <hypotheses>{'\n'.join(hypotheses)}</hypotheses>"""

    return "Say \"Sorry, something went wrong!\""
