import streamlit as st
from google import genai
from dotenv import load_dotenv
import os
import json
import requests
from gtts import gTTS
from io import BytesIO

# ==================================================
# PAGE CONFIG
# ==================================================
st.set_page_config(
    page_title="AI Visual Novel Engine",
    page_icon="📖",
    layout="wide"
)

st.title("📖 AI Multi-Modal Visual Novel")
st.write("Choose your adventure and watch the story unfold!")

# ==================================================
# GEMINI CLIENT
# ==================================================
load_dotenv()

@st.cache_resource
def get_gemini_client():
    return genai.Client(
        api_key=os.getenv("GEMINI_API_KEY")
    )

client = get_gemini_client()

# ==================================================
# SIDEBAR SETTINGS
# ==================================================
st.sidebar.header("🎭 Story Settings")

user_story_prompt = st.text_input(
    "📝 Describe your story idea",
    placeholder="Example: A poor boy discovers a magical dragon egg..."
)

genre = st.sidebar.selectbox(
    "Story Genre",
    [
        "Fantasy",
        "Sci-Fi",
        "Horror",
        "Mystery",
        "Adventure"
    ]
)

art_style = st.sidebar.selectbox(
    "Art Style",
    [
        "Anime",
        "Realistic",
        "Fantasy Art",
        "Cyberpunk",
        "Comic Book"
    ]
)

width = st.sidebar.slider(
    "Image Width",
    256,
    1024,
    512,
    64
)

height = st.sidebar.slider(
    "Image Height",
    256,
    1024,
    512,
    64
)

# ==================================================
# SESSION STATE
# ==================================================
if "story_history" not in st.session_state:
    st.session_state.story_history = []

if "current_options" not in st.session_state:
    st.session_state.current_options = []

if "story_started" not in st.session_state:
    st.session_state.story_started = False

if "story_prompt" not in st.session_state:
    st.session_state.story_prompt = ""

if "prompt_history" not in st.session_state:
    st.session_state.prompt_history = []


# ==================================
# SIDEBAR HISTORY
# ==================================

st.sidebar.markdown("---")
st.sidebar.subheader("📝 Prompt History")

if st.session_state.prompt_history:

    for i, prompt in enumerate(
        st.session_state.prompt_history
    ):
        st.sidebar.write(
            f"{i+1}. {prompt[:40]}..."
        )

else:
    st.sidebar.info("No prompts yet.")

# ==================================================
# SYSTEM PROMPT
# ==================================================
def build_system_prompt(user_choice):

    return f"""
You are a professional interactive visual novel engine.

Story Genre:
{genre}

Art Style:
{art_style}

Story Theme / User Idea:
{st.session_state.story_prompt}

Continue the story based on this player action:

{user_choice}

IMPORTANT:

Return ONLY valid JSON.

Format:

{{
  "story_text":"A narrative paragraph.",
  "image_prompt":"Detailed image generation prompt.",
  "options":[
      "Choice 1",
      "Choice 2",
      "Choice 3"
  ]
}}

Rules:

1. Use simple and easy English.
2. Keep sentences short and readable.
3. Write at a level that a teenager can easily understand.
4. Avoid overly poetic or complex vocabulary.
5. Keep story_text between 80 and 150 words.
6. Make the story exciting and immersive.
"""

# ==================================================
# POLLINATIONS IMAGE
# ==================================================
def generate_image(prompt):

    try:

        style_prompt = prompt

        if art_style == "Anime":
            style_prompt += (
                ", anime style, manga artwork, studio ghibli, "
                "vibrant colors, detailed anime character, masterpiece"
            )

        elif art_style == "Comic Book":
            style_prompt += (
                ", comic book illustration, marvel comics style, "
                "bold outlines, inked artwork, graphic novel"
            )

        elif art_style == "Cyberpunk":
            style_prompt += (
                ", cyberpunk city, neon lights, futuristic atmosphere"
            )

        url = (
            "https://image.pollinations.ai/prompt/"
            + requests.utils.quote(style_prompt)
            + f"?width={width}&height={height}"
        )

        response = requests.get(url, timeout=60)

        if response.status_code == 200:
            return response.content

        return None

    except Exception:
        st.toast("Image server is busy, skipping visual...")
        return None
# ==================================================
# TTS
# ==================================================
def generate_audio(text):

    try:

        tts = gTTS(
            text=text,
            lang="en"
        )

        audio_buffer = BytesIO()
        tts.write_to_fp(audio_buffer)
        audio_buffer.seek(0)

        return audio_buffer

    except Exception:
        return None

# ==================================================
# GEMINI STORY ENGINE
# ==================================================
def get_story_scene(user_choice):

    try:

        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=build_system_prompt(user_choice)
        )

        raw_text = response.text.strip()

        if raw_text.startswith("```json"):
            raw_text = raw_text.replace(
                "```json",
                ""
            ).replace(
                "```",
                ""
            ).strip()

        data = json.loads(raw_text)

        return data

    except Exception as e:

        st.error(
            f"Story generation failed: {e}"
        )

        return None

# ==================================================
# STORY RENDERER
# ==================================================
def render_scene(scene):

    story_text = scene["story_text"]
    image_prompt = scene["image_prompt"]
    options = scene["options"]

    image_data = generate_image(image_prompt)

    audio_data = generate_audio(story_text)

    st.session_state.story_history.append(
        {
            "story_text": story_text,
            "image": image_data,
            "audio": audio_data
        }
    )

    st.session_state.current_options = options

# ==================================================
# START STORY
# ==================================================
if st.button("🚀 Start Adventure"):

    if not user_story_prompt.strip():
        st.warning("Please enter a story idea first.")
        st.stop()

    st.session_state.story_prompt = user_story_prompt

    # Save prompt BEFORE rerun
    if user_story_prompt not in st.session_state.prompt_history:
        st.session_state.prompt_history.append(
            user_story_prompt
        )

    opening_scene = get_story_scene(
        "Begin the story."
    )

    if opening_scene:
        render_scene(opening_scene)
        st.session_state.story_started = True
        st.rerun()

# ==================================================
# DISPLAY STORY HISTORY
# ==================================================
for scene in st.session_state.story_history:

    st.markdown("---")

    st.subheader("📜 Story")

    st.write(scene["story_text"])

    if scene["image"] is not None:
        st.image(
            scene["image"],
            use_container_width=True
        )

    if scene["audio"] is not None:
        st.audio(
            scene["audio"],
            format="audio/mp3"
        )

# ==================================================
# DYNAMIC CHOICE BUTTONS
# ==================================================
if st.session_state.story_started:

    st.markdown("---")
    st.subheader("⚔ Choose Your Next Action")

    options = st.session_state.current_options

    for option in options:

        if st.button(
            option,
            key=option
        ):

            next_scene = get_story_scene(
                option
            )

            if next_scene:
                render_scene(next_scene)

            st.rerun()

st.sidebar.markdown("---")

if st.sidebar.button("🔄 Restart Story"):
    st.session_state.story_history = []
    st.session_state.current_options = []
    st.session_state.story_started = False
    st.rerun()