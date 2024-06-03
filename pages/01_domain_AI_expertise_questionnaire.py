import streamlit as st

from utils import page_setup, save_widget

#######################################
# SETUP
#######################################


page_setup("Setup")


#######################################
# MAIN
#######################################

st.title("Domain & AI Expertise Questionnaire")

st.divider()

st.radio(
    "Select your background",
    ["Resident", "Registrar", "Consultant"],
    index=None,
    key="background",
)

st.radio(
    "How many years of experience do you have?",
    [
        "0-1 year",
        "2-4 years",
        "5-9 years",
        "10-14 years",
        "15-19 years",
        "20-24 years",
        "25+ years",
    ],
    index=None,
    key="domain_experience",
)

st.radio(
    (
        "How often do you use Large Language Models (LLMs, e.g., "
        "ChatGPT, Bing Chat, Google Bard / Gemini) "
        "in any context (not just professional)?"
    ),
    [
        "I have never used such tools",
        "I have tried such tools before, but do not use them regularly",
        "I use such tools monthly",
        "I use such tools weekly",
        "I use such tools daily",
    ],
    index=None,
    key="llm_usage",
)

st.radio(
    "Have you ever studied anything related to AI?",
    ["Yes", "No"],
    index=None,
    key="ai_study",
)

st.divider()

st.markdown(
    "**Please mark each statement with the number that best "
    "describes your feelings or your impression of trust with the "
    "AI you will see.**"
)

questions = [
    "I am confident in the AI. I feel that it will work well.",
    "The outputs of the AI will be very predictable.",
    "The AI will be very reliable. I can count on it to be correct all the time.",
    "I feel safe that when I will rely on the AI I will get the right answers.",
    "The AI will be efficient in that it works very quickly.",
    "I am wary of the AI.",
    "The AI will be able to perform the task better than a novice human user.",
    "I will like using the AI for decision making.",
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
        key=f"ai_trust_before_{i}",
    )

st.divider()

results = ["background", "domain_experience", "llm_usage", "ai_study"] + [
    f"ai_trust_before_{i}" for i in range(len(questions))
]

if st.button("Next", disabled=(any([st.session_state[r] is None for r in results]))):

    for r in results:
        save_widget(r)
    st.switch_page("pages/02_case.py")
