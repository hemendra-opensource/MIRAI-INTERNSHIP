# The Multiverse of Chatbots

A simple Streamlit application that allows users to interact with an AI chatbot through different personalities. Choose how the chatbot responds—whether friendly, professional, sarcastic, wise, or funny—and experience the same conversation from multiple perspectives.

## Features

* Multiple chatbot personalities:

  - Friendly
  - Professional
  - Sarcastic
  - Wise
  - Funny
* Interactive web interface built with Streamlit
* Powered by Google's Gemini 2.5 Flash model
* Real-time AI-generated responses
* Environment variable support for secure API key management

## Tech Stack

* Python
* Streamlit
* Google Gemini API (`google-genai`)
* Python Dotenv

## Project Structure

```text
project/
│
├── app.py
├── .env
├── .gitignore
└── README.md
```

## Installation

### 1. Clone the Repository

```bash
git clone https://github.com/your-username/multiverse-of-chatbots.git
cd multiverse-of-chatbots
```

### 2. Create a Virtual Environment

```bash
python -m venv venv
```

Activate the environment:

**Windows**

```bash
venv\Scripts\activate
```

**macOS/Linux**

```bash
source venv/bin/activate
```

### 3. Install Dependencies

```bash
python -m streamlit run app.py
```

## Environment Setup

Create a `.env` file in the project root directory:

```env
GEMINI_API_KEY=your_api_key_here
```

Replace `your_api_key_here` with your Google Gemini API key.

## Running the Application

Start the Streamlit application:

```bash
streamlit run app.py
```

The application will open automatically in your browser. If it does not, navigate to:

```text
http://localhost:8501
```

## How It Works

1. Select a chatbot personality from the dropdown menu.
2. Enter a message in the text input field.
3. Click the **Send** button.
4. The application sends your message along with the selected personality instruction to the Gemini model.
5. The AI generates a response that matches the chosen personality.

## Example

**Selected Personality:** Friendly

**User Message:**

```text
How can I improve my productivity?
```

**AI Response:**

```text
That's a great question! One of the best ways to improve productivity is to focus on one task at a time and break larger goals into smaller, manageable steps...
```

## Dependencies

```text
streamlit
google-genai
python-dotenv
```

## Future Enhancements

* Chat history support
* Additional personalities
* Custom personality creation
* Dark mode UI
* Conversation export functionality
* Multi-model support
* Voice input and output

## Security Notes

* Never commit your `.env` file to version control.
* Store API keys securely using environment variables.
* Add `.env` to your `.gitignore` file.

## License

This project is licensed under the MIT License. Feel free to use, modify, and distribute it for personal or commercial purposes.

## Acknowledgments

* Streamlit for the interactive web application framework.
* Google Gemini for the generative AI capabilities.
* Python community for the supporting ecosystem and libraries.
