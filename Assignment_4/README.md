# AI Image Studio

An AI-powered image generation web application built with **Streamlit** and **Pollinations AI**. Users can generate images from text prompts, customize image dimensions, choose artistic styles, enhance prompts automatically, and even generate random creative artwork with a single click.

## Features

### Multiple Art Styles

Choose from a variety of artistic styles:

* Realistic
* Cartoon
* Abstract
* Fantasy
* Sci-Fi
* Vintage
* Anime

### Custom Image Dimensions

Adjust image width and height using interactive sliders.

* Minimum: 256 px
* Maximum: 1024 px
* Adjustable in 64 px increments

### Magic Enhance

Automatically improves prompts by adding professional-quality keywords such as:

* masterpiece
* 8k resolution
* highly detailed
* trending on artstation
* unreal engine 5 render

This helps generate higher-quality AI artwork even from simple prompts.

### Surprise Me

Feeling creative but don't know what to generate?

Click the **Surprise Me** button to instantly generate an image from a randomly selected creative prompt.

Examples:

* An astronaut riding a horse on Mars
* A cyberpunk street food vendor in Tokyo
* A giant whale flying through the clouds
* A dragon working in a corporate office
* A futuristic city built inside a volcano

### Image Download

Generated images can be downloaded directly as PNG files.

The downloaded filename is automatically generated based on the selected art style.

Example:

```text
Anime_image.png
Fantasy_image.png
Sci-Fi_image.png
```

---

## Technologies Used

* Python
* Streamlit
* Requests
* Pollinations AI Image API

---

## Project Structure

```text
AI-Image-Studio/
│
├── app.py
├── README.md
└── Demo.mp4
```

---

## Installation

### Clone the Repository

```bash
git clone https://github.com/your-username/AI-Image-Studio.git
cd AI-Image-Studio
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

### Run the Application

```bash
streamlit run app.py
```

---

## Usage

1. Select an art style.
2. Choose image width and height.
3. Enter a text prompt.
4. Optionally enable **Magic Enhance**.
5. Click **Generate Image**.
6. Download the generated image as a PNG file.

Or simply click **🎲 Surprise Me** for a random AI-generated creation.

---

## Assignment Objectives Completed

* Fixed width and height slider functionality
* Added image size parameters to API URL
* Fixed PNG file extension issue
* Added dynamic download filenames
* Implemented Magic Enhance feature
* Implemented Surprise Me feature
* Improved user experience and interface

---

## Author

**Hemendra Sharma**

B.Tech Computer Science & Engineering Student

MirAI School of Technology – AI Builder Track (Virtual Summer Internship 2026)
