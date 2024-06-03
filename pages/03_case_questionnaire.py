import streamlit as st

from config import NUMBER_OF_CASES
from utils import get_case_index, page_setup, save_widget

#######################################
# SETUP
#######################################


page_setup("Questionnaire")


#######################################
# MAIN
#######################################

st.title("Case questionnaire")

st.radio(
    (
        "**Please rate your confidence level in your clinical reasoning for "
        "this case, on a scale of 1 to 5:**"
    ),
    range(1, 6),
    format_func=(
        lambda x: [
            "1 - Very low confidence",
            "2 - Low confidence",
            "3 - Neutral",
            "4 - High confidence",
            "5 - Very high confidence",
        ][x - 1]
    ),
    captions=[
        (
            "You have minimal confidence in the accuracy of your diagnosis or in "
            "the reasoning leading you to it."
        ),
        "",
        (
            "You feel neither particularly confident nor doubtful about your "
            "diagnosis or your reasoning."
        ),
        "",
        (
            "You have great confidence in your diagnosis and in your reasoning, "
            "believing your conclusions to be highly accurate and reliable."
        ),
    ],
    index=None,
    key="confidence_level",
)

st.radio(
    (
        "**Please rate your level of agreement with the following statement – on "
        'a scale of 1 to 5: "Given the complexity of this case and the '
        "information available, I am satisfied that I did my best in my clinical "
        'reasoning"**'
    ),
    range(1, 6),
    format_func=(
        lambda x: [
            "1 - Strongly disagree",
            "2 - Disagree",
            "3 - Neutral",
            "4 - Agree",
            "5 - Strongly agree",
        ][x - 1]
    ),
    captions=[
        (
            "You feel extremely dissatisfied with the thoroughness of your "
            "clinical reasoning, feeling like more options should be considered "
            "or some decisions better justified, even with just the information "
            "available to you."
        ),
        "",
        (
            "You feel neither particularly satisfied nor dissatisfied with the "
            "thoroughness of your clinical reasoning, considering it adequate "
            "but not exceptional."
        ),
        "",
        (
            "You are extremely satisfied with the thoroughness of your clinical "
            "reasoning, having carefully considered all options and arrived at a "
            "logical conclusion given the information available to you."
        ),
    ],
    index=None,
    key="contentment_level",
)

if st.button(
    "Next",
    disabled=(
        st.session_state["confidence_level"] is None
        or st.session_state["contentment_level"] is None
    ),
):

    save_widget("confidence_level", f"case_{get_case_index()}_confidence_level")
    save_widget("contentment_level", f"case_{get_case_index()}_contentment_level")

    if get_case_index() == NUMBER_OF_CASES - 1:
        st.switch_page("pages/04_condition_questionnaire.py")
    else:
        st.session_state["case_index"] += 1
        st.switch_page("pages/02_case.py")

with st.sidebar:
    st.header("Debug")
    st.write(st.session_state)
