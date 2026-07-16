import streamlit as st
import requests
import random

# Sidebar
st.sidebar.header("Image Generation Settings")

art_style = st.sidebar.selectbox(
    "Choose an art style for the image:",
    ["Realistic", "Cartoon", "Abstract", "Fantasy", "Sci-Fi", "Vintage", "Anime"]
)

width = st.sidebar.slider(
    "Select the width of the image:",
    min_value=256,
    max_value=1024,
    value=512,
    step=64
)

height = st.sidebar.slider(
    "Select the height of the image:",
    min_value=256,
    max_value=1024,
    value=512,
    step=64
)

# Image Enhancement 
magic_enhance = st.sidebar.checkbox(" Enable Magic Enhance")
st.title(" AI Image Studio")
st.write(
    "Generate AI-powered images with customizable styles, sizes, "
    "Magic Enhance, and Surprise Me prompts!"
)

user_prompt = st.text_input("Enter a prompt for image generation:")

# Surprise Me Prompts
surprise_prompts = [
    "An astronaut riding a horse on Mars",
    "A cyberpunk street food vendor in Tokyo",
    "A giant whale flying through the clouds",
    "A dragon working in a corporate office",
    "A futuristic city built inside a volcano"
]

generate_btn = st.button(" Generate Image")
surprise_btn = st.button(" Surprise Me!")

def generate_image(prompt_text):
    with st.spinner("Generating image..."):

        full_prompt = (
            f"{prompt_text}, make the art style: {art_style} style"
        )

        # Image Enhancement
        if magic_enhance:
            full_prompt += (
                ", masterpiece, 8k resolution, highly detailed, "
                "trending on artstation, unreal engine 5 render"
            )
        url = (
            f"https://image.pollinations.ai/prompt/"
            f"{full_prompt}?width={width}&height={height}"
        )

        response = requests.get(url)
        if response.status_code == 200:
            st.success(" Image generated successfully!")
            st.image(
                response.content,
                caption=f"{art_style} Style Image",
                use_container_width=True
            )
            st.download_button(
                label=" Download Image",
                data=response.content,
                file_name=f"{art_style}_image.png",
                mime="image/png"
            )
        else:
            st.error(" Failed to generate image. Please try again.")

if generate_btn:
    if user_prompt.strip():
        generate_image(user_prompt)
    else:
        st.warning("Please enter a prompt first.")

if surprise_btn:
    random_prompt = random.choice(surprise_prompts)
    st.info(f" Surprise Prompt: {random_prompt}")
    generate_image(random_prompt)