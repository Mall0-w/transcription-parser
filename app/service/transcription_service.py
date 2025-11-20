
from openai import AsyncOpenAI
from elevenlabs.client import ElevenLabs
import os
from typing import Optional, List, Dict
from io import BytesIO
from app.chains import keyword_parser
import json

elevenlabs = ElevenLabs(
  api_key=os.getenv("ELEVENLABS_API_KEY"),
)


client = AsyncOpenAI()

async def transcribe_audio(audio_data: BytesIO):
    transcription_object =  elevenlabs.speech_to_text.convert(
        file=audio_data,
        model_id="scribe_v1", # Model to use
        tag_audio_events=True, # Tag audio events like laughter, applause, etc.
        language_code="eng", # Language of the audio file. If set to None, the model will detect the language automatically.
        diarize=True, # Whether to annotate who is speaking
    )

    return transcription_object.text

async def parse_keywords(transcription: str) -> Dict[str, str]:
    """
    Takes a transcription of a call and a list of keywords and gives values for those keywords
    according to information found in the transcription
    """
    response = await keyword_parser.primitive_chain.ainvoke({
        "transcription": transcription
    })
    return response.model_dump()

async def parse_keywords_rolling(transcription: str, existing_keywords: Optional[Dict[str, str]] = None, existing_context: Optional[str] = None) -> Dict[str, str]:
    """
    Takes a transcription of a call and a list of keywords and gives values for those keywords
    according to information found in the transcription.  Uses existing keywords to fill in any missing info.
    """
    if existing_keywords is None:
        existing_keywords = {}

    response = await keyword_parser.rolling_chain.ainvoke({
        "transcription": transcription,
        "existing_keywords": existing_keywords,
        "existing_context": existing_context
    })
    response_dict = response.model_dump()
    summary = response_dict.pop("summary", "")
    return response_dict, summary