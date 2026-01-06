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