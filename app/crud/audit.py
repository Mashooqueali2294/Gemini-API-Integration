from sqlalchemy.orm import Session
from app.db import models
from app.services.ai_service import get_ai_summary
from app.services.sms_service import send_sms_alert
import json

def create_smart_audit_log(db: Session, user_id: int, action: str, table: str, target_id: int, old_data: dict, new_data: dict):

    summary_text = get_ai_summary(json.dumps(old_data), json.dumps(new_data))

    new_log = models.AuditLog(
        user_id=user_id,
        action=action,
        table_name=table,
        target_id=target_id,
        old_value=json.dumps(old_data),
        new_value=json.dumps(new_data)
    )
    db.add(new_log)
    db.commit()
    db.refresh(new_log)


    try:
        send_sms_alert(f"Audit Alert: {summary_text}")
    except Exception as e:
        print(f"SMS nhi ja saka: {e}")
    
    return new_log