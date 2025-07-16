import streamlit as st
import os
import re
import requests

from backend.media_gen import generate_audio, generate_video  # Ensure these exist
from backend.pptx_gen import generate_rich_pptx  # Optional: Enable if needed

# ----- Function to get Unsplash image URL -----
def get_unsplash_image(prompt):
    # Returns a dynamic image based on prompt from Unsplash
    return f"https://source.unsplash.com/512x512/?{prompt.replace(' ', '+')}"

# ----- Streamlit UI -----
st.set_page_config(page_title="AI Gov Communication", layout="wide")
st.title("📢 AI-Powered Government Communication Suite")

# Prompt input
prompt = st.text_area("Enter prompt for image generation:", "Enter prompt here")

# Image generation
st.subheader("🖼️ Generate Image from Unsplash")
if st.button("Generate Image"):
    status_placeholder = st.empty()
    status_placeholder.text("Fetching image... Please wait...")

    image_url = get_unsplash_image(prompt)
    status_placeholder.empty()

    if image_url:
        st.image(image_url, caption=f"Image for: {prompt}", use_container_width=True)
    else:
        st.error("❌ Failed to fetch image.")

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
if 'audio_path' in locals() and 'image_url' in locals():
    video_path = generate_video(image_url, audio_path)
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
