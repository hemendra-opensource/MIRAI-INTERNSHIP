import streamlit as st
from google import genai
from dotenv import load_dotenv
import os

# =========================
# Page Title
# =========================
st.title("The Multiverse of Chatbots")

# =========================
# Sidebar
# =========================
personality = st.sidebar.selectbox(
    "Choose AI Personality",
    [
        "Professional",
        "Technical Expert",
        "Business Consultant",
        "Academic Tutor",
        "Creative Thinker"
    ]
)

intensity = st.sidebar.slider(
    "Select the intensity of the personality:",
    min_value=1,
    max_value=10,
    value=5
)

# =========================
# Gemini Setup
# =========================
load_dotenv()

client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)

# =========================
# Task 1: Initialize Memory Vault
# =========================
if "messages" not in st.session_state:
    st.session_state.messages = []

# =========================
# Task 2: Render Chat History
# =========================
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# =========================
# Task 3: Replace Text Input + Button
# =========================
if user_message := st.chat_input("Say something..."):

    # Display user message
    with st.chat_message("user"):
        st.markdown(user_message)

    # =========================
    # Task 4: Save User Message
    # =========================
    st.session_state.messages.append(
        {
            "role": "user",
            "content": user_message
        }
    )

#     ai_instruction = (
#     f"You are a {personality}. "
#     f"Respond with intensity level {intensity}/10. "
#     f"Provide clear, helpful, and well-structured answers."
# )

    # Intensity Logic
    if intensity <= 3:
        style = "Keep responses short and simple."

    elif intensity <= 7:
        style = "Give detailed and well-structured responses."

    else:
        style = (
        "Give highly detailed, expert-level, professional "
        "responses with examples and explanations."
    )

    ai_instruction = f"""
        You are a {personality} AI assistant.

    {style}"""

    with st.spinner("Generating response..."):
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=f"{ai_instruction}\n\nUser message: {user_message}"
        )

    ai_reply = response.text

    # Display assistant message
    with st.chat_message("assistant"):
        st.markdown(ai_reply)

    # Save assistant message
    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": ai_reply
        }
    )