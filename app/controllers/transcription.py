from fastapi import APIRouter, UploadFile, Form
from typing import Annotated
from app.service.transcription_service import transcribe_audio

router = APIRouter(
    prefix="/transcription",
    tags=["transcription"],
    responses={404: {"description": "Not found"}}
)

@router.get("/")
async def get_transcripiton():
    return {"message": "example"}

@router.post("/")
async def transcribe_call(audioFile: UploadFile, claimNumber: Annotated[str, Form()]):
    
    transcription = transcribe_audio(audioFile.file)
    return {"claimNumber": claimNumber, "fileName": audioFile.filename, "text": transcription}