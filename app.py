import streamlit as st
import os
import re
import requests

from backend.media_gen import generate_audio, generate_video  # Make sure these are cloud-compatible
from backend.pptx_gen import generate_rich_pptx  # Optional: Enable if needed

# ----- Function to generate image from Replicate -----
def generate_image_from_replicate(prompt):
    url = "https://api.replicate.com/v1/predictions"
    headers = {
        "Authorization": f"Token {st.secrets['REPLICATE_API_TOKEN']}",
        "Content-Type": "application/json"
    }
    data = {
        "version": "stability-ai/stable-diffusion:b3d14e1c",
        "input": {
            "prompt": prompt,
            "image_dimensions": "512x512",
            "num_outputs": 1,
            "num_inference_steps": 50,
            "guidance_scale": 7.5}
    }

    response = requests.post(url, json=data, headers=headers)
    if response.status_code != 201:
        st.error("❌ Failed to start image generation.")
        st.code(response.text, language="json")  # Show error details
        return None

    prediction = response.json()
    get_url = prediction["urls"]["get"]

    # Polling for result
    while True:
        result = requests.get(get_url, headers=headers)
        result_json = result.json()
        if result_json["status"] == "succeeded":
            return result_json["output"][0]  # Actual image URL
        elif result_json["status"] == "failed":
            st.error("❌ Image generation failed.")
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

    image_url = generate_image_from_replicate(prompt)
    status_placeholder.empty()

    if image_url:
        st.image(image_url, caption="Generated Image", use_container_width=True)
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
if 'audio_path' in locals() and image_url:
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
