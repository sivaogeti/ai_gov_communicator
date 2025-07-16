import streamlit as st
import os
import re
import time
import requests
from PIL import Image
from io import BytesIO

from backend.media_gen import generate_audio, generate_video
from backend.pptx_gen import generate_rich_pptx  # Optional: Enable if needed

# ----- Function to get an image from Unsplash -----
def get_unsplash_image(prompt):
    try:
        # Lowercase + strip spaces
        sanitized_prompt = prompt.strip().lower().replace(' ', '+')
        
        # Use fallback if prompt is too vague or fails
        if not sanitized_prompt:
            sanitized_prompt = "nature"

        # This URL returns a random image for the keyword
        search_url = f"https://source.unsplash.com/random/512x512/?{sanitized_prompt}"

        # Follow redirect to get actual image
        response = requests.get(search_url, allow_redirects=False, timeout=10)
        if response.status_code == 302:
            image_url = response.headers["Location"]
            image_response = requests.get(image_url, timeout=10)
            if image_response.status_code == 200:
                return Image.open(BytesIO(image_response.content))
            else:
                st.warning("⚠️ Image download failed.")
        else:
            st.warning(f"⚠️ No redirect received from Unsplash for prompt '{prompt}'")
    except Exception as e:
        st.warning(f"⚠️ Could not fetch image: {e}")
    return None



# ----- Streamlit UI -----
st.set_page_config(page_title="AI Gov Communication", layout="wide")
st.title("📢 AI-Powered Government Communication Suite")

# Prompt input
prompt = st.text_area("Enter prompt for image generation:", "Enter prompt here")

# Image generation
st.subheader("🖼️ Generate Image")
image = None
temp_image_path = None

if st.button("Generate Image"):
    status_placeholder = st.empty()
    status_placeholder.text("Fetching image... Please wait...")

    image = get_unsplash_image(prompt)
    status_placeholder.empty()

    if image:
        st.image(image, caption=f"Image for: {prompt}", use_container_width=True)
        # Save image for video use
        temp_image_path = "temp_unsplash_image.jpg"
        image.save(temp_image_path)
    else:
        st.error("❌ Failed to fetch image from Unsplash.")

# ----- Audio Generation -----
st.subheader("🎙️ Generate Audio")
audio_lang = st.selectbox("Select Audio Language", ["en", "hi", "te"])
audio_path = None

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
if audio_path and temp_image_path and os.path.exists(temp_image_path):
    video_path = generate_video(temp_image_path, audio_path)
    if video_path:
        st.video(video_path)
    else:
        st.error("❌ Failed to generate video.")
else:
    st.info("ℹ️ Please generate both image and audio to create the video.")

# ----- PPTX Generation (Optional) -----
# st.subheader("📊 Generate PPTX Presentation")
# if st.button("Generate Presentation"):
#     pptx_path = generate_rich_pptx(prompt, temp_image_path, script, audio_path)
#     st.success("✅ Presentation generated successfully!")
#     with open(pptx_path, "rb") as f:
#         st.download_button("📥 Download PPTX", f, file_name="ai_communication_slide.pptx")
