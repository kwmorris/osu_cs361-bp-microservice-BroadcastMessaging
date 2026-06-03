from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from datetime import datetime

from app.database import get_db
from app.models import Message
from app.schemas import MessageData

router = APIRouter(prefix="/messages", tags=["messages"])

@router.get("/{application}")
async def get_message_ids(
    application: str,
    show_expired: bool = False,
    db: AsyncSession = Depends(get_db)):
    
    result = await db.execute(select(Message.id).where(Message.application == application).where(Message.expired == show_expired))
    id_list = result.all()
    
    ids = []
    for id in id_list:
        ids.append(id[0])

    return {"ids": str(ids)}


@router.get("/{application}/{message_id}")
async def get_message(
    application: str,
    message_id: str,
    show_expired: bool = False,
    db: AsyncSession = Depends(get_db)
):
    
    result = await db.execute(select(Message).where(Message.application == application).where(Message.id == message_id).where(Message.expired == show_expired))
    messages = result.first()
    
    if not messages:
        raise HTTPException(status_code=404, detail="No message found")
    
    message = messages[0]

    return {"id": message.id, "data":message.message}


@router.post("/{application}", status_code=201)
async def register_message(
    application: str,
    body: MessageData,
    db: AsyncSession = Depends(get_db)
):
    
    message = Message(id = str(hash(body.data)), application=application, message=body.data)
    db.add(message)
    await db.commit()
    return {"message": "Message registered"}