from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from datetime import datetime

from app.database import get_db
from app.models import Message
from app.schemas import MessageData, MessageResponse

router = APIRouter(prefix="/messages", tags=["messages"])

@router.get("/{application}")
async def get_message_ids(
    application: str,
    show_expired: bool = False,
    db: AsyncSession = Depends(get_db)):
    
    result = await db.execute(select(Message.id).where(Message.application == application).where(Message.expired == show_expired))
    stored_message_ids = result.all()
    
    ids = [id for (id,) in stored_message_ids]

    return {"ids": str(ids)}


@router.get("/{application}/all")
async def get_all_messages(
    application: str,
    show_expired: bool = False,
    db: AsyncSession = Depends(get_db)
):
    
    result = await db.execute(select(Message).where(Message.application == application).where(Message.expired == show_expired))
    stored_messages = result.all()

    if not stored_messages:
        raise HTTPException(status_code=404, detail="No message found")
    
    messages = dict()
    for (message,) in stored_messages:
        messages[message.id] = message.data

    return messages


@router.get("/{application}/{message_id}")
async def get_message(
    application: str,
    message_id: str,
    show_expired: bool = False,
    db: AsyncSession = Depends(get_db)
):
    
    result = await db.execute(select(Message).where(Message.application == application).where(Message.id == message_id).where(Message.expired == show_expired))
    message = result.first()
    
    if not message:
        raise HTTPException(status_code=404, detail="No message found")
    
    (message,) = message

    return {"id": message.id, "data":message.data}


@router.post("/{application}", status_code=201)
async def register_message(
    application: str,
    body: MessageData,
    db: AsyncSession = Depends(get_db)
):
    
    message = Message(id = str(hash(body.data)), application=application, data=body.data)
    db.add(message)
    await db.commit()
    return {"message": "Message registered"}


@router.patch("/{application}")
async def update_message(
    application: str,
    body: MessageResponse,
    db: AsyncSession = Depends(get_db)
):
    
    result = await db.execute(select(Message).where(Message.application == application))
    stored_message = result.scalar()

    if not stored_message:
        raise HTTPException(status_code=404, detail="No message found")
    
    stored_message.id = body.id
    stored_message.application = body.application
    stored_message.data = body.data
    stored_message.expired = body.expired

    await db.commit()
    return {"message": "Message updated"}