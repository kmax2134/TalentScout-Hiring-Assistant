# app.py (Streamlit)
import sys, os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

import streamlit as st
from utils.openai_utils import call_llm
from utils.conversation import save_candidate
from prompts import GREETING_PROMPT, TECH_QUESTION_PROMPT

# --- Streamlit Page Config ---
st.set_page_config(page_title="TalentScout Hiring Assistant", layout="centered")
st.title("🤖 TalentScout Hiring Assistant")
st.write("Welcome! I’ll help you with the initial screening process for tech roles.")

# --- Session State ---
if "conversation" not in st.session_state:
    st.session_state.conversation = []
if "candidate" not in st.session_state:
    st.session_state.candidate = {}
if "phase" not in st.session_state:
    st.session_state.phase = "greeting"
if "current_question" not in st.session_state:
    st.session_state.current_question = None
if "asked_questions" not in st.session_state:
    st.session_state.asked_questions = []  # track all questions to prevent duplicates


# --- Greeting Phase ---
if st.session_state.phase == "greeting":
    bot_msg = call_llm(GREETING_PROMPT)
    st.chat_message("assistant").write(bot_msg)
    st.session_state.phase = "info"


# --- Info Collection Phase ---
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
        # 🔒 Save with privacy masking
        save_candidate(st.session_state.candidate)

        if tech_stack.strip():
            # 🔥 Reset for new set of questions
            st.session_state.conversation = []
            st.session_state.asked_questions = []

            prompt = TECH_QUESTION_PROMPT.format(tech_stack=tech_stack)
            questions = call_llm(prompt, mode="default", asked_questions=st.session_state.asked_questions)

            # Save asked questions
            for line in questions.split("\n"):
                if "?" in line:
                    st.session_state.asked_questions.append(line.strip())

            st.session_state.current_question = questions
            st.session_state.conversation.append(("bot", questions))

        st.session_state.phase = "questions"
        st.rerun()


# --- Questions Phase ---
if st.session_state.phase == "questions":
    # Display conversation so far
    for role, msg in st.session_state.conversation:
        st.chat_message("assistant" if role == "bot" else "user").write(msg)

    # Candidate reply
    user_input = st.chat_input("Your response:")
    if user_input:
        # 🔹 Exit detection
        exit_keywords = ["exit", "quit", "bye", "thank you"]
        if any(word in user_input.lower() for word in exit_keywords):
            st.session_state.conversation.append(("user", user_input))
            st.session_state.conversation.append(
                ("bot", "🙏 Thank you for your time! Your details have been securely recorded. Our team will contact you soon.")
            )
            st.session_state.phase = "end"
            st.rerun()
        else:
            st.session_state.conversation.append(("user", user_input))
            bot_reply = call_llm(
                user_input,
                context=f"Candidate's Tech Stack: {st.session_state.candidate.get('Tech Stack', '')}",
                mode="default",
                asked_questions=st.session_state.asked_questions
            )
            # Save new asked question(s) if generated
            for line in bot_reply.split("\n"):
                if "?" in line and line.strip() not in st.session_state.asked_questions:
                    st.session_state.asked_questions.append(line.strip())

            st.session_state.conversation.append(("bot", bot_reply))
            st.rerun()

    # 🔥 Add "Ask New Questions" button
    if st.button("Ask New Questions"):
        st.session_state.conversation = []

        tech_stack = st.session_state.candidate.get("Tech Stack", "")
        if tech_stack.strip():
            prompt = TECH_QUESTION_PROMPT.format(tech_stack=tech_stack)
            questions = call_llm(prompt, mode="default", asked_questions=st.session_state.asked_questions)

            for line in questions.split("\n"):
                if "?" in line and line.strip() not in st.session_state.asked_questions:
                    st.session_state.asked_questions.append(line.strip())

            st.session_state.current_question = questions
            st.session_state.conversation.append(("bot", questions))

        st.rerun()


# --- End Phase ---
if st.session_state.phase == "end":
    st.success("✅ Interview ended. Thank you for using TalentScout Hiring Assistant.")
