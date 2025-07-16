import streamlit as st
import requests
from PIL import Image
from io import BytesIO

from backend.media_gen import generate_audio, generate_video  # Ensure these are cloud-compatible
from backend.pptx_gen import generate_rich_pptx  # Optional

# --- 🔁 Unsplash image fetch with fallback ---
def get_unsplash_image(prompt):
    try:
        if prompt.strip():
            url = f"https://source.unsplash.com/random/512x512/?{prompt.strip().lower().replace(' ', '+')}"
        else:
            url = "https://source.unsplash.com/random/512x512"

        response = requests.get(url, timeout=10)

        if response.status_code == 200 and response.headers['Content-Type'].startswith("image"):
            return Image.open(BytesIO(response.content))
        else:
            st.warning(f"⚠️ Unsplash did not return an image for prompt '{prompt}'.")
    except Exception as e:
        st.warning(f"⚠️ Error fetching image: {e}")
    return None

# --- 🖥️ Streamlit UI ---
st.set_page_config(page_title="AI Gov Communication", layout="wide")
st.title("📢 AI-Powered Government Communication Suite")

# Prompt input
prompt = st.text_area("Enter prompt for image generation:", "Enter prompt here")

# Image generation
st.subheader("🖼️ Generate Image")
image = None
if st.button("Generate Image"):
    status = st.empty()
    status.text("Generating image... Please wait...")
    image = get_unsplash_image(prompt)
    status.empty()

    if image:
        st.image(image, caption="Generated Image", use_container_width=True)
    else:
        st.error("❌ Failed to fetch image from Unsplash.")

# Audio generation
st.subheader("🎙️ Generate Audio")
audio_lang = st.selectbox("Select Audio Language", ["en", "hi", "te"])
if st.button("Generate Audio"):
    audio_path = generate_audio(prompt, lang=audio_lang)
    if audio_path:
        st.audio(audio_path)
        st.success("✅ Audio generated successfully!")
    else:
        st.error("❌ Failed to generate audio.")

# Video script
st.subheader("📝 Generate Video Script")
script = f"Video Script\n\n{prompt}\n\n[Add visuals here based on the narration]"
st.markdown(f"```\n{script}\n```")

# Video generation
st.subheader("🎥 Generate Video")
if 'audio_path' in locals() and image:
    video_path = generate_video(image, audio_path)
    if video_path:
        st.video(video_path)
    else:
        st.error("❌ Failed to generate video.")

# Optional: PPTX generation
# st.subheader("📊 Generate PPTX Presentation")
# if st.button("Generate Presentation"):
#     pptx_path = generate_rich_pptx(prompt, image, script, audio_path)
#     st.success("✅ Presentation generated successfully!")
#     with open(pptx_path, "rb") as f:
#         st.download_button("📥 Download PPTX", f, file_name="ai_communication_slide.pptx")
