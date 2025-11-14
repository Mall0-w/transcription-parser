
from openai import AsyncOpenAI
from elevenlabs.client import ElevenLabs
import os
from io import BytesIO
from langchain.agents import create_agent
from app.models import constants

elevenlabs = ElevenLabs(
  api_key=os.getenv("ELEVENLABS_API_KEY"),
)

agent = create_agent(

)

client = AsyncOpenAI()

def transcribe_audio(audio_data: BytesIO):
    transcription_object =  elevenlabs.speech_to_text.convert(
        file=audio_data,
        model_id="scribe_v1", # Model to use
        tag_audio_events=True, # Tag audio events like laughter, applause, etc.
        language_code="eng", # Language of the audio file. If set to None, the model will detect the language automatically.
        diarize=True, # Whether to annotate who is speaking
    )

    return transcription_object.text

def parse_keywords(transcription: str, keywords: list[str] = constants.TRANSCRIPTION_KEYWORDS) -> dict[str, str]:
    """
    Takes a transcription of a call and a list of keywords and gives values for those keywords
    according to information found in the transcription
    """

    return {}