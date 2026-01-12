import os
from dotenv import load_dotenv
from google import genai

app =load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    raise RuntimeError("GEMINI_API_KEY missing in .env file")

client = genai.Client(api_key=api_key)

def get_ai_summary(old_val, new_val):
    try:
        response = client.models.generate_content(
            model = "gemini-2.5-flash",
            contents=f"Write a 1-sentence professional summnary for a payment of {old_val} to {new_val}."
        )
        return response.text.strip()
    except Exception as e:
        print("AI ERROR", e)
        return "summary unavailable at the moment"