# Memory Vault – Stateful Multiverse Chatbot

## Overview

Memory Vault is an upgraded version of the Multiverse Chatbot developed as part of the **MirAI School of Technology – Virtual Summer Internship 2026 (AI Builder Track)**.

The objective of this project was to transform a **stateless chatbot** into a **stateful chatbot** using **Streamlit Session State**. Unlike a traditional chatbot that forgets previous interactions after every rerun, this application maintains conversation history throughout the user session.

The chatbot is powered by **Google Gemini 2.5 Flash** and provides dynamic responses based on selected AI personalities.

---

## Assignment Objective

Streamlit reruns the entire script whenever a user interacts with the application. This behavior causes chat history to disappear unless a persistent state management mechanism is implemented.

This project solves that problem using:

* `st.session_state`
* `st.chat_input()`
* `st.chat_message()`

The result is a chatbot that remembers previous conversations and delivers a modern chat experience.

---

## Features

### Persistent Chat Memory

Stores user and assistant messages using Streamlit Session State, ensuring conversations remain visible across reruns.

### Modern Chat Interface

Uses Streamlit's native chat components:

* `st.chat_input()`
* `st.chat_message()`

for a clean and intuitive messaging experience.

### AI Personality Selection

Users can choose different chatbot personalities from the sidebar:

* Professional
* Technical Expert
* Business Consultant
* Academic Tutor
* Creative Thinker

### 🎚 Personality Strength Control

A slider allows users to adjust the intensity of the selected personality, resulting in varying response styles and levels of detail.

### Gemini AI Integration

Responses are generated using Google's Gemini 2.5 Flash model through the Gemini API.

---

## Project Architecture

```text
User Message
      │
      ▼
st.chat_input()
      │
      ▼
Save Message in Session State
      │
      ▼
Gemini API Request
      │
      ▼
AI Response Generated
      │
      ▼
Save AI Response in Session State
      │
      ▼
Render Entire Chat History
```

---

## How Session State Works

When Streamlit reruns a script, all normal variables are recreated.

To prevent chat history from being lost, the application initializes a memory vault:

```python
if "messages" not in st.session_state:
    st.session_state.messages = []
```

Every user message and AI response is stored in:

```python
st.session_state.messages
```

This allows the chatbot to reconstruct the full conversation whenever the page reruns.

---

## Assignment Requirements Implemented

### Task 1 – Initialize Memory Vault

Created a persistent message store using:

```python
st.session_state.messages
```

### Task 2 – Render Chat History

Displays all previous messages during every rerun using:

```python
for message in st.session_state.messages:
```

### Task 3 – Upgrade Input UI

Replaced:

```python
st.text_input()
st.button()
```

with:

```python
st.chat_input()
```

### Task 4 – Save Messages

Both user messages and AI responses are stored in Session State.

---

## Tech Stack

* Python
* Streamlit
* Google Gemini API
* python-dotenv

---

## Project Structure

```text
Memory-Vault-Stateful-Chatbot/
│
├── app.py
├── requirements.txt
├── .env
├── demo.mp4
└── README.md
```

---

## Installation

### 1. Clone Repository

```bash
git clone <repository-url>
cd Memory-Vault-Stateful-Chatbot
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure Environment Variables

Create a `.env` file:

```env
GEMINI_API_KEY=YOUR_API_KEY
```

### 4. Run Application

```bash
streamlit run app.py
```

---

## Demonstration

The submitted demo video demonstrates:

* A continuous 3-message conversation
* Persistent chat history
* Sidebar personality changes
* Session State memory retention
* Gemini-powered responses

---

## Key Concepts Learned

* Stateful vs Stateless Applications
* Streamlit Session State
* Chat UI Development
* Gemini API Integration
* Prompt Engineering
* User Experience Design
* Conversation Persistence

---

## Author

**Hemendra Sharma**
Github-link : https://github.com/hemendra-opensource/MIRAI-INTERNSHIP/tree/main/Assignment_3

B.Tech Computer Science & Engineering
Aspiring Full Stack Developer | AI Enthusiast | DSA Learner

---

## Internship

**MirAI School of Technology**
**Virtual Summer Internship 2026 – AI Builder Track**

Assignment: **The Memory Vault (Stateful Chatbot)**
