import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

genai.configure(api_key=os.getenv("AIzaSyC2duxKFeQ9STHv83NbPbU4HElPGybHsH0"))

model = genai.GenerativeModel("gemini-pro")

def analyze_emergency(message):
    prompt = f"""
    Analyze this emergency message and return JSON with:
    category, severity(1-5), urgency, risk, authority

    Message: {message}
    """

    response = model.generate_content(prompt)
    return response.text
