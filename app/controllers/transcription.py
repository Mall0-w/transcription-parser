from fastapi import APIRouter, UploadFile, Form
from typing import Annotated
from app.service.transcription_service import transcribe_audio, parse_keywords

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
    
    transcription = await transcribe_audio(audioFile.file)
    keyword_values = await parse_keywords(transcription)
    return {"claimNumber": claimNumber, "fileName": audioFile.filename, "text": transcription, "keywords": keyword_values}