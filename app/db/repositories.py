from sqlalchemy.orm import Session
from app.db.models import ModerationResult

class ModerationRepository:
    def __init__(self, db: Session):
        self.db = db

    def save_result(self, text: str, result: dict):
        is_flagged = result.get("flagged", False)
        db_result = ModerationResult(text=text, is_flagged=is_flagged)
        self.db.add(db_result)
        self.db.commit()
        self.db.refresh(db_result)