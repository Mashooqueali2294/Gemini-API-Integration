from sqlalchemy.orm import Session
from app.db import models
from app.services.ai_service import get_ai_summary
from app.services.sms_service import send_sms_alert
import json

def create_smart_audit(db: Session, user_id: int, table: str, old_val: dict, new_val: dict):

    summary_text = get_ai_summary(json.dump(old_val), json.dumps(new_val))

    new_log = models.AuditLog(
        user_id = user_id,
        table_name = table,
        old_value=json.dumps(old_val),
        new_value=json.dumps(new_val),
        summary=summary_text,
        action = "UPDATE"
    )

    db.add(new_log)
    db.commit()
    db.refresh(new_log)

    try:
        send_sms_alert(f"Audit Alert: {summary_text}")
    except Exception as e:
        print(f"SMS nhi ja saka: {e}")

    return new_log