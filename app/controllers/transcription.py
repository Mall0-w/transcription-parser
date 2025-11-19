from fastapi import APIRouter, UploadFile, Form
from typing import Annotated
from app.service.transcription_service import transcribe_audio, parse_keywords
from app.util.text_cleaner import chunk_text
import asyncio

router = APIRouter(
    prefix="/transcription",
    tags=["transcription"],
    responses={404: {"description": "Not found"}}
)

@router.post("/")
@router.post("/primitive")
async def transcribe_call_primitive(audioFile: UploadFile, claimNumber: Annotated[str, Form()]):
    """
    Workflow:
    grab transcription
    chunk transcription so its digestible by the parse
    send each chunk to the parser and await all, extract all keywords for each chunk then combine them all.
    """

    #elevenlabs can take a file of up to 3GB according to their docs, so no need to chunk for now
    #a 90 minute call will be at worst around 1GB more likely than not; safe to assume calls will be under 3GB for now.
    transcription = await transcribe_audio(audioFile.file)
    #chunck the transcription if too long for llm.  

    #1 most models have a limit of 4,000 tokens (16,000 characters approx), go on side of error
    chunks = chunk_text(transcription, max_tokens=3000)  # e.g., 2000 token limit

    #pass all calls to the parser and wait for all to complete
    tasks = [parse_keywords(chunk) for chunk in chunks]
    all_keys = await asyncio.gather(*tasks)

    #combine all keyword dicts into one
    keyword_values = {key: value for chunk_keywords in all_keys for key, value in chunk_keywords.items()}

    return {"claimNumber": claimNumber, "fileName": audioFile.filename, "text": transcription, "keywords": keyword_values}