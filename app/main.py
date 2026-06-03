from fastapi import FastAPI
from app.routes import messages
from app.database import engine, Base

app = FastAPI(title="Message Broadcast Service")

@app.on_event("startup")
async def startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

app.include_router(messages.router)

@app.get("/health")
async def health():
    return {"status": "ok"}