from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from app.db import models
from app.db.database import engine, get_db
from app.services.ai_service import get_ai_summary
from app.services.sms_service import send_sms_alert

models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="OpenAI & SMS learning Course")

@app.get("/")
def home():
    return {"message": "Welcome Mashooque! AI and SMS course is running"}

@app.post("/test-ai-system")
def test_system(old_val: str, new_val: str, db: Session = Depends(get_db)):

    summary = get_ai_summary(old_val, new_val)

    sms_id = send_sms_alert(f"Alert: {summary}")

    return{
        "status": "Success",
        "ai_summary": summary,
        "twilio_sid": sms_id
    }