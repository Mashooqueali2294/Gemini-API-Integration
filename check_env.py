import os
from dotenv import load_dotenv


load_dotenv()

print("--- Enviroment Check ---")
print(f"Current Directory: {os.getcwd}")
print(f"Gemini Key: {os.getenv("GEMINI_API_KEY")}")
print(f"Twilio SID: {os.getenv("TWILIO_ACCOUNT_SID")}")