from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from langchain_ollama import ChatOllama
from app.models.callinfo import CallInfo

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

prompt = ChatPromptTemplate.from_messages([
    (
        "system",
        "Extract the fields required by the schema from the call transcription. "
        "If information is missing, return null or an empty value."
    ),
    (
        "user",
        "Transcription:\n{transcription}"
    )
])

primitive_chain = prompt | structured_llm
