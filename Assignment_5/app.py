import os
import re
import json
import uuid
import shutil
import requests
import urllib.parse
from pydantic import BaseModel, Field
import streamlit as st
from dotenv import load_dotenv
from gtts import gTTS

load_dotenv()

st.set_page_config(
    page_title="Multi-Modal Visual Novel Engine",
    page_icon="📖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Constants & Paths
TEMP_AUDIO_DIR = "temp_audio"

# Define the Pydantic schema for structured output from Gemini
class VisualNovelScene(BaseModel):
    story_text: str = Field(description="A descriptive narrative paragraph continuing the story (3-5 sentences).")
    image_prompt: str = Field(description="A detailed, cinematic image prompt for an AI image generator depicting this specific scene. Avoid generic terms.")
    options: list[str] = Field(description="2 to 3 meaningful choices for the reader to continue the story.")

# Ensure the temp audio directory exists
if not os.path.exists(TEMP_AUDIO_DIR):
    os.makedirs(TEMP_AUDIO_DIR)

# -- CSS Styling (Rich aesthetics, dark mode, custom fonts)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600;800&display=swap');

/* Apply modern typography globally */
html, body, [class*="css"] {
    font-family: 'Outfit', sans-serif;
}

/* Custom dark gradient background for premium look */
.stApp {
    background: radial-gradient(circle at top left, #120e2e, #090616);
    color: #e5e1fa;
}

/* Sidebar aesthetics */
[data-testid="stSidebar"] {
    background-color: #0d0a21 !important;
    border-right: 1px solid #231c52;
}

/* Custom styled buttons with gradient and smooth transition */
div.stButton > button {
    background: linear-gradient(135deg, #6c5ce7, #a29bfe);
    color: white !important;
    border: none;
    border-radius: 12px;
    padding: 12px 24px;
    font-size: 1rem;
    font-weight: 600;
    transition: all 0.3s cubic-bezier(0.25, 0.8, 0.25, 1);
    box-shadow: 0 4px 15px rgba(108, 92, 231, 0.4);
    width: 100%;
    margin-bottom: 8px;
}

div.stButton > button:hover {
    transform: translateY(-2px);
    box-shadow: 0 6px 20px rgba(108, 92, 231, 0.6);
    background: linear-gradient(135deg, #a29bfe, #6c5ce7);
    border: none !important;
}

div.stButton > button:active {
    transform: translateY(1px);
}

/* Scene Card Container */
.scene-card {
    background: rgba(25, 20, 55, 0.55);
    border: 1px solid rgba(108, 92, 231, 0.25);
    border-radius: 18px;
    padding: 28px;
    margin-bottom: 28px;
    backdrop-filter: blur(12px);
    box-shadow: 0 10px 30px rgba(0, 0, 0, 0.4);
    transition: all 0.3s ease;
}

.scene-card:hover {
    border-color: rgba(108, 92, 231, 0.45);
    box-shadow: 0 12px 35px rgba(108, 92, 231, 0.15);
}

.scene-text {
    font-size: 1.15rem;
    line-height: 1.7;
    color: #e2dffa;
}

/* Selected option pill */
.choice-badge {
    background-color: rgba(108, 92, 231, 0.2);
    border: 1px solid rgba(108, 92, 231, 0.4);
    color: #a29bfe;
    border-radius: 20px;
    padding: 6px 16px;
    font-size: 0.9rem;
    font-weight: 600;
    display: inline-block;
    margin-bottom: 16px;
}

/* Header style styling with linear gradient text */
.gradient-title {
    font-weight: 800 !important;
    background: linear-gradient(to right, #a29bfe, #6c5ce7, #fd79a8);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    font-size: 3rem;
    margin-bottom: 0px;
}

.gradient-subtitle {
    color: #a29bfe;
    font-size: 1.2rem;
    margin-bottom: 30px;
    font-weight: 300;
}
</style>
""", unsafe_allow_html=True)

# Helper Functions

@st.cache_resource
def get_gemini_client(api_key: str):
    """
    Cache the Google GenAI client based on the provided API key.
    """
    from google import genai
    return genai.Client(api_key=api_key)

def cleanup_temp_files():
    """
    Clean up all generated temporary narration audio files.
    """
    if os.path.exists(TEMP_AUDIO_DIR):
        try:
            shutil.rmtree(TEMP_AUDIO_DIR)
        except Exception:
            pass
    os.makedirs(TEMP_AUDIO_DIR, exist_ok=True)

def clean_and_parse_json(text: str) -> dict:
    """
    Cleans raw response from Gemini in case it accidentally wraps it in markdown code fences,
    then parses and validates it using Python's json module.
    """
    cleaned = text.strip()
    
    # Strip markdown code fences if present (e.g. ```json ... ``` or ``` ... ```)
    cleaned = re.sub(r"^```(?:json)?\s*", "", cleaned, flags=re.MULTILINE | re.IGNORECASE)
    cleaned = re.sub(r"\s*```$", "", cleaned, flags=re.MULTILINE | re.IGNORECASE)
    cleaned = cleaned.strip()
    
    # Attempt to parse directly
    try:
        data = json.loads(cleaned)
    except json.JSONDecodeError:
        # Fallback: find the first '{' and last '}' to extract raw JSON
        match = re.search(r"(\{.*\})", cleaned, re.DOTALL)
        if match:
            try:
                data = json.loads(match.group(1))
            except json.JSONDecodeError as e:
                raise ValueError("Could not parse extracted JSON block.") from e
        else:
            raise ValueError("No JSON object structure found in response.")

    # Validate schema fields
    required_fields = ["story_text", "image_prompt", "options"]
    for field in required_fields:
        if field not in data:
            raise KeyError(f"Missing required JSON key: {field}")
            
    if not isinstance(data["options"], list):
        raise TypeError("The 'options' key must be a list.")
        
    return data

def generate_pollinations_image(prompt: str) -> bytes:
    """
    Fetches generated image bytes from the Pollinations Image API based on the prompt.
    Fails gracefully returning None if server is down or times out.
    """
    encoded_prompt = urllib.parse.quote(prompt)
    url = f"https://image.pollinations.ai/prompt/{encoded_prompt}?width=1024&height=768&nologo=true&private=true"
    try:
        response = requests.get(url, timeout=25)
        if response.status_code == 200:
            return response.content
        else:
            raise Exception(f"HTTP Error {response.status_code}")
    except Exception:
        # Graceful failure as requested in Phase 5
        return None

def generate_gtts_audio(text: str) -> str:
    """
    Generates narration audio from text using gTTS and saves it temporarily to disk.
    Fails gracefully returning None if gTTS fails.
    """
    try:
        # Create a unique file name to avoid browser caching issues or collisons
        filename = os.path.join(TEMP_AUDIO_DIR, f"scene_{uuid.uuid4().hex}.mp3")
        tts = gTTS(text=text, lang="en", tld="com")
        tts.save(filename)
        return filename
    except Exception:
        # Graceful failure as requested in Phase 5
        return None

def handle_choice(option_text: str):
    """
    Triggered when a story option button is clicked. Sets state to process choice on rerun.
    """
    st.session_state.next_choice = option_text

# -- Main Application Flow

# Load API Key
api_key = os.getenv("GEMINI_API_KEY")

if not api_key or api_key == "your_api_key_here":
    st.markdown('<h1 class="gradient-title">Multi-Modal Visual Novel Engine</h1>', unsafe_allow_html=True)
    st.markdown('<p class="gradient-subtitle">Capstone Project — MirAI School of Technology</p>', unsafe_allow_html=True)
    st.error("🔑 **Gemini API Key missing or not configured!**")
    st.info("Please create a `.env` file in the project root directory and add your key:\n`GEMINI_API_KEY=your_actual_api_key`\n\nEnsure that you restart your Streamlit server after adding the file.")
    st.stop()

# Initialize Cached Gemini Client
try:
    client = get_gemini_client(api_key)
except Exception as e:
    st.error(f"Failed to initialize Gemini Client: {e}")
    st.stop()

# Sidebar: Story Settings
st.sidebar.markdown("## ⚙️ Story Settings")
st.sidebar.write("Configure your visual novel engine parameters below.")

genre = st.sidebar.selectbox(
    "Story Genre",
    ["Fantasy", "Sci-Fi", "Mystery", "Horror", "Adventure", "Cyberpunk"]
)

art_style = st.sidebar.selectbox(
    "Art Style",
    ["Anime", "Realistic", "Cinematic", "Digital Art", "Watercolor", "Pixel Art"]
)

model_name = st.sidebar.selectbox(
    "Gemini Model",
    ["gemini-2.5-flash", "gemini-2.5-pro", "gemini-2.0-flash"]
)

st.sidebar.markdown("---")

# Session State Initialization
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []  # Raw messages log if needed
if "gemini_chat" not in st.session_state:
    st.session_state.gemini_chat = None
if "generated_scenes" not in st.session_state:
    st.session_state.generated_scenes = []
if "story_started" not in st.session_state:
    st.session_state.story_started = False
if "next_choice" not in st.session_state:
    st.session_state.next_choice = None
if "current_genre" not in st.session_state:
    st.session_state.current_genre = genre
if "current_art_style" not in st.session_state:
    st.session_state.current_art_style = art_style

# Detect setting changes and prompt for restart if settings don't match active story
settings_changed = (genre != st.session_state.current_genre) or (art_style != st.session_state.current_art_style)

# Sidebar Action Controls
if st.session_state.story_started:
    if st.sidebar.button("🔄 Restart Story", use_container_width=True):
        cleanup_temp_files()
        st.session_state.generated_scenes = []
        st.session_state.gemini_chat = None
        st.session_state.story_started = False
        st.session_state.next_choice = None
        st.session_state.current_genre = genre
        st.session_state.current_art_style = art_style
        st.rerun()

if settings_changed and st.session_state.story_started:
    st.sidebar.warning("⚠️ Settings changed! Restart the story to apply the new genre/style.")

# Story Generation Engine

def start_story():
    """
    Initializes the Gemini Chat Session and generates the opening scene.
    """
    cleanup_temp_files()
    st.session_state.generated_scenes = []
    st.session_state.current_genre = genre
    st.session_state.current_art_style = art_style
    
    # Construct System prompt to enforce structured output matching our Pydantic schema
    system_prompt = f"""
    You are the interactive director of a premium Multi-Modal Visual Novel.
    You will generate scenes based on the genre: "{genre}" and the art style: "{art_style}".
    
    You MUST respond in STRICT JSON format matching the schema details:
    - story_text: descriptive paragraph of 3-5 sentences continuing the narrative.
    - image_prompt: a rich, detailed, cinematic image generation prompt for an AI describing the scene, lighting, mood, camera angle, and including the art style: "{art_style}". Do NOT use abstract terms.
    - options: a list of 2 to 3 meaningful choices for the user to make next to progress the story.

    Constraints:
    - Never include markdown wrappers like ```json ... ``` in your output.
    - Never return code fences.
    - Keep the text immersive and write in the second person ("You...").
    """ 
    try:
        # Create chat session with configuration
        from google.genai import types
        chat = client.chats.create(
            model=model_name,
            config=types.GenerateContentConfig(
                system_instruction=system_prompt,
                response_mime_type="application/json",
                response_schema=VisualNovelScene,
                temperature=0.7,
            )
        )
        st.session_state.gemini_chat = chat
        
        # Request opening scene
        opening_prompt = f"Start the visual novel opening scene. The genre is {genre} and the art style is {art_style}."
        response = chat.send_message(opening_prompt)
        
        # Clean and parse JSON response
        scene_data = clean_and_parse_json(response.text)
        
        # Generate Visual and Audio
        with st.spinner("Creating opening visual..."):
            img_prompt = f"{scene_data['image_prompt']}, {art_style} style"
            image_bytes = generate_pollinations_image(img_prompt)
            if image_bytes is None:
                st.toast("Image server is busy, skipping visual...")
        
        with st.spinner("Synthesizing opening audio..."):
            audio_path = generate_gtts_audio(scene_data["story_text"])
            
        first_scene = {
            "choice_made": None,
            "story_text": scene_data["story_text"],
            "image_prompt": scene_data["image_prompt"],
            "image_bytes": image_bytes,
            "audio_path": audio_path,
            "options": scene_data["options"]
        }
        
        st.session_state.generated_scenes.append(first_scene)
        st.session_state.story_started = True
        
    except Exception as e:
        st.error(f"Error starting story: {e}")

def process_next_scene(choice_text: str):
    """
    Processes the chosen path, queries Gemini for the next scene,
    generates visuals & audio, and appends it to the story history.
    """
    chat = st.session_state.gemini_chat
    if not chat:
        st.error("Error: Active chat session lost. Please restart.")
        return
        
    try:
        # Send choice to Gemini chat
        response = chat.send_message(choice_text)
        
        # Clean and parse
        scene_data = clean_and_parse_json(response.text)
        
        # Generate visual (Pollinations)
        img_prompt = f"{scene_data['image_prompt']}, {st.session_state.current_art_style} style"
        image_bytes = generate_pollinations_image(img_prompt)
        if image_bytes is None:
            st.toast("Image server is busy, skipping visual...")
            
        # Generate audio (gTTS)
        audio_path = generate_gtts_audio(scene_data["story_text"])
        
        new_scene = {
            "choice_made": choice_text,
            "story_text": scene_data["story_text"],
            "image_prompt": scene_data["image_prompt"],
            "image_bytes": image_bytes,
            "audio_path": audio_path,
            "options": scene_data["options"]
        }
        
        st.session_state.generated_scenes.append(new_scene)
        
    except Exception as e:
        st.error(f"Error generating next scene: {e}")

# -- Main UI Presentation

# Application Header
st.markdown('<h1 class="gradient-title">Multi-Modal Visual Novel Engine</h1>', unsafe_allow_html=True)
st.markdown('<p class="gradient-subtitle">Capstone Project — MirAI School of Technology AI Builder Internship</p>', unsafe_allow_html=True)

# Process any pending choice first
if st.session_state.next_choice is not None:
    choice = st.session_state.next_choice
    st.session_state.next_choice = None  # Clear flag immediately to prevent double submission
    with st.spinner(f"Navigating: '{choice}'..."):
        process_next_scene(choice)
    st.rerun()

# Layout rendering
if not st.session_state.story_started:
    # Game Launcher Welcome Screen
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown(f"""
        ### Welcome to the AI Visual Novel Generator!
        
        This advanced engine uses **Google Gemini** to orchestrate real-time, branching narratives. For every action you take:
        1. **Generative Text** crafts the story.
        2. **Pollinations AI** designs descriptive visual backgrounds.
        3. **Google TTS** synthesizes voice narration.
        
        **Active Configuration:**
        * 🎭 **Genre:** `{genre}`
        * 🎨 **Art Style:** `{art_style}`
        * 🤖 **Model:** `{model_name}`
        
        Use the sidebar to change settings or click the button below to start your journey.
        """)  
        if st.button("🚀 Begin Adventure", use_container_width=True):
            with st.spinner("Initializing story state..."):
                start_story()
            st.rerun()
            
    with col2:
        # Visual presentation of launcher card
        st.markdown("""
        <div class="scene-card" style="text-align: center;">
            <h3 style="margin-top: 0px;">Project Capstone</h3>
            <p>MirAI School of Technology<br>AI Builder Internship 2026</p>
            <p style="font-size: 3rem; margin: 0px;">🧬</p>
        </div>
        """, unsafe_allow_html=True)

else:
    # Render all generated scenes in the story history sequentially
    for idx, scene in enumerate(st.session_state.generated_scenes):
        st.write("---")
        
        # Display the choice badge if this is a follow-up scene
        if scene["choice_made"]:
            st.markdown(f'<div class="choice-badge">✦ You chose: "{scene["choice_made"]}"</div>', unsafe_allow_html=True)
        else:
            st.markdown('<div class="choice-badge">✦ Story Beginning</div>', unsafe_allow_html=True)
            
        # Left-Right Column Layout for Story and Image
        col_story, col_img = st.columns([1, 1])
        
        with col_story:
            # Narrative text card
            st.markdown(f"""
            <div class="scene-card">
                <div class="scene-text">{scene["story_text"]}</div>
            </div>
            """, unsafe_allow_html=True)
            
            # Narration player if audio exists
            if scene["audio_path"] and os.path.exists(scene["audio_path"]):
                st.audio(scene["audio_path"], format="audio/mp3")
                
        with col_img:
            # Visual scene presentation
            if scene["image_bytes"]:
                st.image(scene["image_bytes"], use_container_width=True)
            else:
                # Fallback style block if image generation was skipped
                st.markdown(f"""
                <div style="background-color: rgba(255, 255, 255, 0.05); border: 2px dashed rgba(108, 92, 231, 0.3); border-radius: 18px; padding: 50px; text-align: center; height: 100%; display: flex; flex-direction: column; justify-content: center;">
                    <p style="font-size: 2.5rem; margin: 0px;">🖼️</p>
                    <p style="color: #a29bfe; font-size: 0.95rem; margin-top: 10px;">Visual skipped (Image server busy)<br><i>Prompt: {scene['image_prompt']}</i></p>
                </div>
                """, unsafe_allow_html=True)

    # Render options for the *last* scene
    current_scene = st.session_state.generated_scenes[-1]
    
    st.write("---")
    st.markdown("### 🧭 Make Your Choice:")
    
    # Render choice buttons side-by-side or stacked nicely
    options = current_scene["options"]
    cols = st.columns(len(options))
    
    for option_idx, option in enumerate(options):
        with cols[option_idx]:
            # Generate a unique key based on scene index and option index to prevent conflicts
            st.button(
                option,
                key=f"option_btn_{len(st.session_state.generated_scenes)-1}_{option_idx}",
                on_click=handle_choice,
                args=(option,)
            )
