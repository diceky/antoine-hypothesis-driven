import streamlit as st

from utils import get_group, page_setup, save_widget

#######################################
# SETUP
#######################################


page_setup("Questionnaire")


#######################################
# MAIN
#######################################

st.title("Condition questionnaire")

st.radio(
    (
        "**Please indicate to what extent you perceive the clinical decision "
        "aids you used as beneficial in assisting you with your clinical "
        "reasoning, on a scale of 1 to 5:**"
    ),
    range(1, 6),
    format_func=(
        lambda x: [
            "1 - Not helpful at all",
            "2 - Somewhat helpful",
            "3 - Moderately helpful",
            "4 - Very helpful",
            "5 - Extremely helpful",
        ][x - 1]
    ),
    captions=[
        (
            "The absence of the clinical decision aids would not have affected "
            "you at all."
        ),
        "",
        (
            "The clinical decision aids helped you in your reasoning on multiple "
            "occasions."
        ),
        "",
        (
            "The clinical decision aids were instrumental in achieving the "
            "quality of clinical reasoning you achieved."
        ),
    ],
    index=None,
    key="perceived_helpfulness",
)

st.radio(
    (
        "**Please rate your sense of agency/control in your clinical reasoning, "
        "on a scale of 1 to 5:**"
    ),
    range(1, 6),
    format_func=(
        lambda x: [
            "1 - No control/agency",
            "2 - Low control/agency",
            "3 - Neutral",
            "4 - High control/agency",
            "5 - Complete control/agency",
        ][x - 1]
    ),
    captions=[
        "You feel completely powerless or without influence over the " "outcome.",
        "",
        (
            "You feel neither particularly empowered nor powerless, with a "
            "moderate level of control/agency."
        ),
        "",
        (
            "You feel completely empowered and in full control of the outcome, "
            "with no doubts about your ability to influence it."
        ),
    ],
    index=None,
    key="agency",
)

st.radio(
    (
        "**Please rate how cognitively demanding your interaction with the "
        "clinical decision aids were, on a scale of 1 to 5:**"
    ),
    range(1, 6),
    format_func=(
        lambda x: [
            "1 - Very low demand",
            "2 - Low demand",
            "3 - Neutral",
            "4 - High demand",
            "5 - Very high demand",
        ][x - 1]
    ),
    captions=[
        (
            "Interacting with the clinical decision aids required minimal mental "
            "effort."
        ),
        "",
        (
            "Interacting with the clinical decision aids required neither high "
            "nor low mental effort."
        ),
        "",
        (
            "Interacting with the clinical decision aids required intense mental "
            "focus and concentration."
        ),
    ],
    index=None,
    key="mental_demand",
)


if get_group() != "control":
    st.divider()

    st.markdown(
        "**Please mark each statement with the number that best "
        "describes your feelings or your impression of trust with the "
        "AI you saw.**"
    )

    questions = [
        "I am confident in the AI. I feel that it works well.",
        "The outputs of the AI are very predictable.",
        "The AI is very reliable. I can count on it to be correct all the time.",
        "I feel safe that when I rely on the AI I will get the right answers.",
        "The AI is efficient in that it works very quickly.",
        "I am wary of the AI.",
        "The AI can perform the task better than a novice human user.",
        "I like using the AI for decision making.",
    ]

    for i, question in enumerate(questions):
        st.radio(
            f"**{question}**",
            range(1, 6),
            format_func=(
                lambda x: [
                    "1 - I disagree strongly",
                    "2 - I disagree somewhat",
                    "3 - I'm neutral about it",
                    "4 - I agree somewhat",
                    "5 - I agree strongly",
                ][x - 1]
            ),
            horizontal=True,
            index=None,
            key=f"ai_trust_after_{i}",
        )

st.divider()

results = ["perceived_helpfulness", "agency", "mental_demand"] + [
    f"ai_trust_after_{i}" for i in range(len(questions))
]

if st.button("Next", disabled=(any([st.session_state[r] is None for r in results]))):

    for r in results:
        save_widget(r)
    st.switch_page("pages/05_semi-structured_interview.py")

with st.sidebar:
    st.header("Debug")
    st.write(st.session_state)
