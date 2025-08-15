from fastapi import FastAPI
from app.api.event_router import router as event_router

app = FastAPI()
app.include_router(event_router)
