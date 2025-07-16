import streamlit as st
import os
import re
import requests
import time

from backend.media_gen import generate_audio, generate_video  # Ensure these are cloud-compatible
from backend.pptx_gen import generate_rich_pptx  # Optional: Enable if needed

# ----- Function to generate image from Hugging Face Inference API -----
def generate_image_from_huggingface(prompt):
    api_token = st.secrets["HF_API_TOKEN"]
    API_URL = "https://api-inference.huggingface.co/models/stabilityai/stable-diffusion-2"
    headers = {"Authorization": f"Bearer {api_token}"}

    payload = {"inputs": prompt}
    response = requests.post(API_URL, headers=headers, json=payload)

    if response.status_code == 200:
        image_bytes = response.content
        return image_bytes
    else:
        st.error("❌ Failed to generate image.")
        st.code(response.text, language="json")
        return None

# ----- Streamlit UI -----
st.set_page_config(page_title="AI Gov Communication", layout="wide")
st.title("📢 AI-Powered Government Communication Suite")

# Prompt input
prompt = st.text_area("Enter prompt for image generation:", "Enter prompt here")

# Image generation
st.subheader("🖼️ Generate Image")
if st.button("Generate Image"):
    status_placeholder = st.empty()
    status_placeholder.text("Generating image... Please wait...")

    image_bytes = generate_image_from_huggingface(prompt)
    status_placeholder.empty()

    if image_bytes:
        st.image(image_bytes, caption="Generated Image", use_container_width=True)
    else:
        st.error("❌ Failed to generate image.")

# ----- Audio Generation -----
st.subheader("🎙️ Generate Audio")
audio_lang = st.selectbox("Select Audio Language", ["en", "hi", "te"])
if st.button("Generate Audio"):
    audio_path = generate_audio(prompt, lang=audio_lang)
    if audio_path:
        st.audio(audio_path)
        st.success("✅ Audio generated successfully!")
    else:
        st.error("❌ Failed to generate audio.")

# ----- Video Script -----
st.subheader("📝 Generate Video Script")
script = f"Video Script\n\n{prompt}\n\n[Add visuals here based on the narration]"
st.markdown(f"```\n{script}\n```")

# ----- Video Generation -----
st.subheader("🎥 Generate Video")
if 'audio_path' in locals() and image_bytes:
    video_path = generate_video(image_bytes, audio_path)
    if video_path:
        st.video(video_path)
    else:
        st.error("❌ Failed to generate video.")

# ----- PPTX Generation (Optional) -----
# st.subheader("📊 Generate PPTX Presentation")
# if st.button("Generate Presentation"):
#     pptx_path = generate_rich_pptx(prompt, image_url, script, audio_path)
#     st.success("✅ Presentation generated successfully!")
#     with open(pptx_path, "rb") as f:
#         st.download_button("📥 Download PPTX", f, file_name="ai_communication_slide.pptx")
