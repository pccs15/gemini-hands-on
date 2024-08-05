import logging
import os

import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

YOUTUBE_API_KEY = os.getenv("YOUTUBE_API_KEY")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
TRANSCRIPT_LANGUAGES = os.getenv("TRANSCRIPT_LANGUAGES", "ja,en").split(",")

genai.configure(api_key=GEMINI_API_KEY)

logging.basicConfig(
    format="[%(asctime)s][%(levelname)s] %(message)s in %(pathname)s:%(lineno)d",
    level=logging.DEBUG
)
