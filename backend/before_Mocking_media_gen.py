import os
import re
from openai import OpenAI

client = OpenAI(api_key=api_key)
from pathlib import Path

# 📁 Ensure output directory exists
output_dir = Path("generated_media")
output_dir.mkdir(parents=True, exist_ok=True)

# 🧹 Remove emojis to avoid encoding issues
def remove_emojis(text):
    emoji_pattern = re.compile(
        "["
        u"\U0001F600-\U0001F64F"  # emoticons
        u"\U0001F300-\U0001F5FF"  # symbols & pictographs
        u"\U0001F680-\U0001F6FF"  # transport & map symbols
        u"\U0001F1E0-\U0001F1FF"  # flags
        u"\U00002500-\U00002BEF"  # Chinese characters
        "]+", flags=re.UNICODE
    )
    return emoji_pattern.sub(r'', text)


# 🎙️ Generate audio (placeholder or plug in gTTS)
def generate_audio(text, lang="en"):
    clean_text = remove_emojis(text)
    audio_path = output_dir / "narration.mp3"
    with open(audio_path, "wb") as f:
        f.write(b"")  # Replace with actual TTS logic
    return str(audio_path)


# 📝 Generate video script text
def generate_script(text):
    clean_text = remove_emojis(text)
    script_path = output_dir / "generated_script.txt"
    script = f"Video Script\n\n{clean_text}\n\n[Add visuals here based on the narration]"
    with open(script_path, "w", encoding="utf-8") as f:
        f.write(script)
    return str(script_path)


# 🖼️ Generate an image using OpenAI DALL·E

# backend/media_gen.py
from openai import OpenAI

client = OpenAI(api_key=api_key)

def generate_image(prompt, api_key):
    try:
        # Ensure you are using the correct OpenAI API key

        # Request the image generation
        response = client.images.generate(model="dall-e-2",  # You can also try "dall-e-3"
        prompt=prompt,
        n=1,
        size="1024x1024")

        # Save the generated image URL
        image_url = response.data[0].url
        return image_url

    except Exception as e:
        print(f"🔥 Error generating image: {e}")
        return None
