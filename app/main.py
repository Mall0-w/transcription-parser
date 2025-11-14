from fastapi import FastAPI
from dotenv import load_dotenv
import os

load_dotenv()

from app.controllers import transcription

app = FastAPI()
app.include_router(transcription.router)

@app.get("/")
async def test_connection():
    return {"message": "Hello, World!"}