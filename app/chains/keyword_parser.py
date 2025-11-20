from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from langchain_ollama import ChatOllama
from app.models.callinfo import CallInfo, RollingCallInfo

# llm = ChatOpenAI(
#     model="gpt-4o-mini",
#     api_key=os.getenv("OPENAI_API_KEY"),
#     temperature=0
# )

llm = ChatOllama(
    model="mistral",
    temperature=0,
)

structured_llm = structured_llm = llm.with_structured_output(CallInfo)
structured_llm_rolling = llm.with_structured_output(RollingCallInfo)

primitive_prompt = ChatPromptTemplate.from_messages([
    (
        "system",
        "You are an expert information extraction engine. "
        "Extract *every possible field* from the transcription and map it "
        "to the schema exactly.\n\n"
        "Rules:\n"
        "- Do NOT omit fields if the information clearly appears.\n"
        "- If the value is implied, infer it.\n"
        "- If the value is completely missing, only then return null.\n"
        "- Use the transcription wording as the source of truth.\n\n"
        f"Schema fields to extract: {CallInfo.model_fields.keys()}"
    ),
    ("user", "Transcription:\n{transcription}")
])

rolling_prompt = ChatPromptTemplate.from_messages([
    (
        "system",
        "You are an expert information extraction engine. "
        "Extract *every possible field* from the transcription and map it "
        "to the schema exactly.\n\n"
        "Rules:\n"
        "- Do NOT omit fields if the information clearly appears.\n"
        "- If the value is implied, infer it.\n"
        "- If the value is completely missing, only then return null.\n"
        "- Use the transcription wording as the source of truth.\n\n"
        f"Schema fields to extract: {CallInfo.model_fields.keys()}"
        f"also provide a summary of the call up to this point"
        f"{'- Use the existing keywords to fill in any missing information.' if '{existing_keywords}' else ''}"
        f"{'- use the existing context to inform your extraction and improve your summary.' if '{existing_context}' else ''}"
    ),
    ("user", "Transcription:\n{transcription}")
])

primitive_chain = primitive_prompt | structured_llm

rolling_chain = rolling_prompt | structured_llm_rolling
