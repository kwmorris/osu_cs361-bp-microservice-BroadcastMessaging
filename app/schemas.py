from pydantic import BaseModel

class MessageData(BaseModel):
    data: str

class MessageResponse(BaseModel):
    id: str
    application: str
    data: str
    expired: bool