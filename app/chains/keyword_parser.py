from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from langchain_ollama import ChatOllama
import os

# llm = ChatOpenAI(
#     model="gpt-4o-mini",
#     api_key=os.getenv("OPENAI_API_KEY"),
#     temperature=0
# )

llm = ChatOllama(
    model="mistral",
    temperature=0,
    # other params...
)

prompt = ChatPromptTemplate.from_messages([
    (
        "system",
        "You extract structured information from transcriptions. "
        "Return ONLY valid JSON following this schema: "
        "{{keyword: extracted_value_or_empty_string}}."
    ),
    (
        "user",
        "Transcription:\n{transcription}\n\n"
        "Keywords:\n{keywords}\n\n"
        "Extract one value per keyword. If not found, return an empty string."
    )
])

chain = prompt | llm
