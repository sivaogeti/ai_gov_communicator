import streamlit as st
import os
import subprocess
import re
from backend.media_gen import generate_audio, generate_video  # Ensure your imports are correct

# Function to check if the image exists
def check_image_exists(image_path):
    return os.path.exists(image_path)

# Function to generate a unique filename based on the prompt
def generate_unique_filename_for_image(prompt, output_dir="C:/Users/fimba/OneDrive/Desktop/PythonProjects/ai_gov_comm/outputs"):
    clean_prompt = re.sub(r'\W+', '_', prompt)  # Clean the prompt to make it safe for filenames
    filename = f"{clean_prompt}.png"
    return os.path.join(output_dir, filename)

# Function to run the generate_image.py script as a subprocess
def generate_image_subprocess(prompt):
    python_executable = r"C:\Users\fimba\OneDrive\Desktop\stable-diffusion\venv\Scripts\python.exe"
    command = [
        python_executable,
        r"C:\Users\fimba\OneDrive\Desktop\stable-diffusion\generate_image.py",
        prompt
    ]

    try:
        result = subprocess.run(command, check=True, capture_output=True, text=True)
        print(result.stdout)  # Print stdout from the subprocess
        print(result.stderr)  # Print stderr from the subprocess
    except subprocess.CalledProcessError as e:
        print(f"Error occurred: {e}")
        print(f"Standard Output: {e.stdout}")
        print(f"Standard Error: {e.stderr}")
        st.error(f"Error generating image: {e.stderr}")

# Streamlit setup
st.set_page_config(page_title="AI Gov Communication", layout="wide")
st.title("📢 AI-Powered Government Communication Suite")

# Get user input for the prompt
prompt = st.text_area("Enter prompt for image generation:", "Enter prompt here")

# Path to check if the image exists
output_dir = "C:/Users/fimba/OneDrive/Desktop/PythonProjects/ai_gov_comm/outputs"
image_path = generate_unique_filename_for_image(prompt, output_dir)

# Check if the image exists and display it if available
if check_image_exists(image_path):
    st.image(image_path, caption="Generated Image", use_container_width=True)
else:
    if st.button("Generate Image"):
        # Show generating message
        status_placeholder = st.empty()
        status_placeholder.text("Generating image... Please wait...")

        # Run the subprocess to generate the image
        generate_image_subprocess(prompt)

        # Clear the generating message once the image is generated
        status_placeholder.empty()

        if check_image_exists(image_path):
            st.image(image_path, caption="Generated Image", use_container_width=True)
        else:
            st.error("❌ Failed to generate the image.")

# Generate Audio section
st.subheader("🎙️ Generate Audio")
audio_lang = st.selectbox("Select Audio Language", ["en", "hi", "te"])
if st.button("Generate Audio"):
    audio_path = generate_audio(prompt, lang=audio_lang)  # Assuming generate_audio takes the prompt and language
    st.audio(audio_path)
    st.success("Audio generated successfully!")

# Generate Video Script section
st.subheader("📝 Generate Video Script")
script = f"Video Script\n\n{prompt}\n\n[Add visuals here based on the narration]"
st.markdown(f"```\n{script}\n```")

# Generate Video section
st.subheader("🎥 Generate Video")
if check_image_exists(image_path) and 'audio_path' in locals():
    video_path = generate_video(image_path, audio_path)  # Assuming generate_video function is available
    if video_path:
        st.video(video_path)
    else:
        st.error("❌ Failed to generate video.")
