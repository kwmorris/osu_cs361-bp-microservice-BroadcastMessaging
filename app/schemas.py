from pydantic import BaseModel
from datetime import datetime

class MessageData(BaseModel):
    data: str

class MessageResponse(BaseModel):
    message: str
    creation_date: datetime
    expired: bool