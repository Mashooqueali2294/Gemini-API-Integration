import os
from dotenv import load_dotenv
import google.generativeai as genai

# .env file se saari settings load karo
load_dotenv()

# Key ko environment variable se uthao
api_key = os.getenv("GEMINI_API_KEY")

genai.configure(api_key=api_key)

def get_ai_summary(old_val, new_val):
    try:
        model = genai.GenerativeModel("gemini-pro")
        prompt = f"""
        Analyze this data change and give a 1-sentence professional summary:
        old_value: {old_val}
        new_value: {new_val}
        summary:
        """

        response = model.generate_content(prompt)
        return response.text.strip()
    except Exception as e:
        return "Summary unavailable at the moment"