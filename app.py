import sys, os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

import streamlit as st
from utils.openai_utils import call_llm
from utils.conversation import save_candidate
from prompts import GREETING_PROMPT, TECH_QUESTION_PROMPT, TECH_ANSWER_PROMPT

# --- Streamlit Page Config ---
st.set_page_config(page_title="TalentScout Hiring Assistant", layout="centered")

st.title("TalentScout Hiring Assistant")
st.write("Welcome! I’ll help you with the initial screening process for tech roles.")

# Initialize Session State 
if "conversation" not in st.session_state:
    st.session_state.conversation = []
if "candidate" not in st.session_state:
    st.session_state.candidate = {}
if "phase" not in st.session_state:
    st.session_state.phase = "greeting"
if "questions" not in st.session_state:
    st.session_state.questions = ""  # store generated questions

# Greeting Phase 
if st.session_state.phase == "greeting":
    bot_msg = call_llm(GREETING_PROMPT)
    st.chat_message("assistant").write(bot_msg)
    st.session_state.phase = "info"

# Info Collection Phase 
if st.session_state.phase == "info":
    with st.form("candidate_form"):
        col1, col2 = st.columns(2)

        with col1:
            full_name = st.text_input("Full Name")
            email = st.text_input("Email Address")
            phone = st.text_input("Phone Number")

        with col2:
            experience = st.text_input("Years of Experience")
            position = st.text_input("Desired Position(s)")
            location = st.text_input("Current Location")

        tech_stack = st.text_area("Tech Stack (languages, frameworks, databases, tools)")

        submitted = st.form_submit_button("Submit")

    if submitted:
        st.session_state.candidate = {
            "Full Name": full_name,
            "Email Address": email,
            "Phone Number": phone,
            "Years of Experience": experience,
            "Desired Position(s)": position,
            "Current Location": location,
            "Tech Stack": tech_stack,
        }
        save_candidate(st.session_state.candidate)

        if tech_stack.strip():
            prompt = TECH_QUESTION_PROMPT.format(tech_stack=tech_stack)
            questions = call_llm(prompt)
            st.session_state.questions = questions
            st.session_state.conversation.append(("bot", questions))

        st.session_state.phase = "questions"

#  Questions Phase 
if st.session_state.phase == "questions":
    for role, msg in st.session_state.conversation:
        if role == "bot":
            st.chat_message("assistant").write(msg)
        else:
            st.chat_message("user").write(msg)

    # Candidate reply
    user_input = st.chat_input("Your response:")
    if user_input:
        st.session_state.conversation.append(("user", user_input))
        bot_reply = call_llm(user_input)   # Treat as candidate’s own reply
        st.session_state.conversation.append(("bot", bot_reply))

    #New Button to get correct answers
    if st.button("Show Answers"):
        prompt = TECH_ANSWER_PROMPT.format(question=st.session_state.questions)
        answers = call_llm(prompt)
        st.session_state.conversation.append(("bot", answers))


