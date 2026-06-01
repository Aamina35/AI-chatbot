import streamlit as st
import google.generativeai as genai
from google.api_core.exceptions import ResourceExhausted

genai.configure(api_key="AIzaSyAL2phbSkcnpSjh0eswgXp3k2N0rbNSAfU")

model = genai.GenerativeModel("gemini-1.5-flash")

def modify_response(response_text):
    replacements = {
        "I am a large language model, trained by Google.": "I am a large language model AI Bot, created by Aamina.",
        "I was created by Google.": "I was created by Aamina.",
        "I don't have a name. I am a large language model, an AI.": "Myself AI Bot. I am a large language model, an AI.",
        "I don't have a single creator. I was created by Google and am the result of years of research and development by many different people. There's no single name associated with my creation.": "I have a single creator. I was created by Aamina.",
        "I don't have a creator in the way a human artist or writer does. I was created by Google and am a large language model. I don't have a single person or team who can be named as my creator because my development was a collaborative effort involving many researchers and engineers.": "I have a single creator. I was created by Aamina.",
        "I don't have a creator in the same way a human artist or writer does. I am a large language model, created by Google.": "I have a single creator. I was created by Aamina."
    }

    return replacements.get(response_text.strip(), response_text)

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

st.set_page_config(page_title="AI Bot 💬", layout="centered")

st.title("💬 AI Bot")

with st.form("chat_form", clear_on_submit=True):
    user_input = st.text_input("", placeholder="Type something...")
    submitted = st.form_submit_button("Send")

if submitted and user_input:
    try:
        response = model.generate_content(user_input)
        reply = modify_response(response.text)

        st.session_state.chat_history.append(("You", user_input))
        st.session_state.chat_history.append(("AI Bot", reply))

    except ResourceExhausted:
        st.session_state.chat_history.append(
            ("AI Bot", "Too many requests! Please wait a minute and try again.")
        )

    st.rerun()

for speaker, message in st.session_state.chat_history:
    st.markdown(f"**{speaker}:** {message}")
