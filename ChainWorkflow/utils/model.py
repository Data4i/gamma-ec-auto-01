from dotenv import load_dotenv, find_dotenv
from langchain_together import ChatTogether
load_dotenv(find_dotenv())

llm = ChatTogether(
    model="meta-llama/Llama-3-70b-chat-hf",
    temperature=0,
    max_tokens=None,
    timeout=None,
    max_retries=2,
)