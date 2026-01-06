import os 
from twilio.rest import Client
from dotenv import load_dotenv

load_dotenv()

def send_sms_alert(message_body):
    account_sid = os.getenv("TWILIO_ACCOUNT_SID")
    auth_token = os.getenv("TWILIO_AUTH_TOKEN")
    from_num = os.getenv("TWILIO_FROM_NUMBER")
    to_num = os.getenv("MY_PERSONAL_NUMBER")

    client = Client(account_sid, auth_token)

    message = client.messages.create(
        body=message_body,
        from_=from_num,
        to=to_num
    )
    return message.sid

def send_sms_alert(message_body):
    load_dotenv() # Ensure it's called
    
    account_sid = os.getenv("TWILIO_ACCOUNT_SID")
    auth_token = os.getenv("TWILIO_AUTH_TOKEN")
    
    # --- YE DO LINES DEBUGGING KE LIYE ADD KAREIN ---
    print(f"DEBUG: Account SID is {account_sid}")
    print(f"DEBUG: Auth Token is {auth_token}")
    # -----------------------------------------------

    if not account_sid or not auth_token:
        return "Error: Credentials nahi mile!"