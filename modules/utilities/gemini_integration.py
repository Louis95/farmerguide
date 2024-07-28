import os

import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()


genai.configure(api_key=os.environ["GEMINI_API_KEY"])


def call_gemini(prompt: dict):
    model = genai.GenerativeModel("gemini-1.5-flash")
    response = model.generate_content([prompt["text"], prompt["img"]], stream=True)
    return response
