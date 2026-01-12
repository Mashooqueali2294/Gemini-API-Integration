import os
from pathlib import Path
from dotenv import load_dotenv
from app.services.stripe_service import create_checkout_session
from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from app.db import models
from app.db.database import engine, get_db
from app.services.ai_service import get_ai_summary
from app.services.sms_service import send_sms_alert
import stripe
from fastapi import Request, Header

env_path = Path(".") / ".env"
load_dotenv(dotenv_path=env_path)
print(f"TEST GEMINI KEY: {os.getenv("GEMINI_API_KEY")}")


models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="OpenAI & SMS Learning Course")

@app.get("/")
def home():
    return {"message": "Welcome Mashooque! AI and SMS course is running."}

@app.post("/test-ai-system")
def test_system(old_val: str, new_val: str, db: Session = Depends(get_db)):

    summary = get_ai_summary(old_val, new_val)

    sms_id = send_sms_alert(f"Alert: {summary}")

    return{
        "status": "success",
        "ai_summary": summary,
        "twilio_sid": sms_id
    }

@app.post("/create-payment")
def pay_now(item: str, price: int):
    checkout_url = create_checkout_session(item, price)
    return {"checkout_url": checkout_url}

STRIPE_WEBHOOK_SECRET = os.getenv("STRIPE_WEBHOOK_SECRET")

@app.post("/stripe-webhook")
async def stripe_webhook(request: Request, stripe_signature: str = Header(None)):
    payload = await request.body()
    try:
        event = stripe.Webhook.construct_event(
            payload, stripe_signature, STRIPE_WEBHOOK_SECRET
        )
    except Exception as e:
        return {"error": str(e)}
    
    if event["type"] == "checkout.session.completed":
        session = event["data"]["object"]
        customer_email = session["customer_details"]["email"]
        amount = session["amount_total"] / 100

        print(f"DEBUG: Data collected for {customer_email}")

        ai_response = get_ai_summary(
            old_val="No Payment",
            new_val=f"Success Payment of {amount} PKR from {customer_email}"
        )

        print(f"DEBUG: AI Response is: {ai_response}")

        sms_body = f"MASH_DEV ALERT: {ai_response}"
        send_sms_alert(sms_body)

        print(f"MISSION SUCCESS: Payment recieved and SMS sent to user!")
    return {"status": "success"}

@app.post("/create-subscription")
async def create_sub(email: str, price_id: str):

    checkout_url = create_subscription_session(email, price_id)
    return {"checkout_url": checkout_url}