from sqlalchemy import Column, Integer, String, Boolean
from app.db.session import Base

class ModerationResult(Base):
    __tablename__ = "moderation_results"
    id = Column(Integer, primary_key=True, index=True)
    text = Column(String, index=True)
    is_flagged = Column(Boolean)