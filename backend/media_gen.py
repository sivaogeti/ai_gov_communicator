import os
from dotenv import load_dotenv
import requests
from gtts import gTTS
from moviepy.editor import ImageClip, AudioFileClip
from pathlib import Path

from datetime import datetime
import random
import string

def generate_unique_filename(extension):
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    random_str = ''.join(random.choices(string.ascii_letters + string.digits, k=8))
    return f"{timestamp}_{random_str}{extension}"

# Load the .env file
load_dotenv()

# Output directory for generated files
output_dir = Path("generated_media")
output_dir.mkdir(parents=True, exist_ok=True)

# 🧹 Remove emojis to avoid encoding issues
def remove_emojis(text):
    import re
    emoji_pattern = re.compile(
        "["
        u"\U0001F600-\U0001F64F"  # emoticons
        u"\U0001F300-\U0001F5FF"  # symbols & pictographs
        u"\U0001F680-\U0001F6FF"  # transport & map symbols
        u"\U0001F1E0-\U0001F1FF"  # flags
        "]+", flags=re.UNICODE
    )
    return emoji_pattern.sub(r'', text)

# 🎙️ Generate audio (gTTS)
def generate_audio(text, lang="en"):
    clean_text = remove_emojis(text)
    audio_path = str(output_dir / generate_unique_filename(".mp3"))
    tts = gTTS(clean_text, lang=lang)
    tts.save(audio_path)
    return str(audio_path)

# 🖼️ Generate image using Hugging Face API
def generate_image(prompt):
    api_key = os.getenv("hugging_face_apikey")  # Get API key from .env
    if not api_key:
        raise ValueError("API key not found in environment variables")

    headers = {"Authorization": f"Bearer {api_key}"}
    url = "https://api-inference.huggingface.co/models/stabilityai/stable-diffusion-3.5-large"

    payload = {"inputs": prompt}  # Use the actual prompt here

    try:
        response = requests.post(url, headers=headers, json=payload)
        if response.status_code == 200:
            image_path = str(output_dir / generate_unique_filename(".png"))
            with open(image_path, "wb") as f:
                f.write(response.content)
            return str(image_path)
        else:
            print(f"Error: {response.text}")
            return None
    except Exception as e:
        print(f"Error generating image: {e}")
        return None


# 🎥 Create a video using moviepy and FFmpeg
def generate_video(image_path, audio_path):
    try:
        # Load image and audio files
        img_clip = ImageClip(image_path).set_duration(5)  # Set video duration (5 seconds)
        audio_clip = AudioFileClip(audio_path)

        # Set the audio for the video
        video = img_clip.set_audio(audio_clip)

        # Output video path
        video_path = str(output_dir / generate_unique_filename(".mp4"))
        video.write_videofile(str(video_path), fps=24)

        return str(video_path)
    except Exception as e:
        print(f"Error generating video: {e}")
        return None
