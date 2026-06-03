from datetime import datetime, timezone
from sqlalchemy import Column, String, DateTime, Boolean
from app.database import Base

class Message(Base):
    __tablename__ = "messages"

    id            = Column(String, primary_key=True)
    application   = Column(String, nullable=False)
    message       = Column(String, nullable=False)
    created_at    = Column(DateTime, default=datetime.now(timezone.utc))
    expired       = Column(Boolean, default=False)
