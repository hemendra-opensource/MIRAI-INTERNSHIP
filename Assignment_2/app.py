import streamlit as st

st.title("The Multiverse of chatbots")

personality= st.selectbox("Who do you want to talk to?", ["Friendly", "Professional", "Sarcastic", "Wise", "Funny"])

st.write(f"You selected: {personality}")

from google import genai
from dotenv import load_dotenv
import os

load_dotenv()
client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)

user_message = st.text_input("Enter your message:")
if st.button("Send"):
    if user_message:
        ai_instruction = f"Respond in a {personality} manner."

        with st.spinner("Generating response..."):
            response = client.models.generate_content(
                model="gemini-2.5-flash",
                contents=f"{ai_instruction} User message: {user_message}"
            )
            st.success("Response generated!")
            st.write(f"AI Response: {response.text}")
    else:
        st.warning("Please enter a message before sending.")