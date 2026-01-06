import os
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

genai.configure(api_key=api_key)

def get_ai_summary(old_val, new_val):
    try:
        model = genai.GenerativeModel("gemini-pro")

        prompt = f"""
        Analyze this data change and give a 1-sentence professional summary:
        old_val: {old_val}
        new_val: {new_val}
        summary:
        """

        response = model.generate_content(prompt)
        return response.text.strip()
    except Exception as e:
        return "Summary unavailable at the moment."