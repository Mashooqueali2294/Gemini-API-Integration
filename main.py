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
        # Signal ko verify karein ke ye waqayi Stripe se aaya hai
        event = stripe.Webhook.construct_event(
            payload, stripe_signature, STRIPE_WEBHOOK_SECRET
        )
    except Exception as e:
        return {"error": str(e)}

    # Agar payment success ho jaye
    if event['type'] == 'checkout.session.completed':
        session = event['data']['object']
        print(f"💰 PAISA MIL GAYA! Customer: {session['customer_details']['email']}")
        # Yahan aap user ko email bhej sakte hain ya database update kar sakte hain

    return {"status": "success"}