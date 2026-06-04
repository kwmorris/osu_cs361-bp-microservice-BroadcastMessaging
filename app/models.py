from sqlalchemy import Column, String, Boolean
from app.database import Base

class Message(Base):
    __tablename__ = "messages"

    id            = Column(String, primary_key=True)
    application   = Column(String, nullable=False)
    data          = Column(String, nullable=False)
    expired       = Column(Boolean, default=False)
