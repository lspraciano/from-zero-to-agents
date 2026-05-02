import os

from dotenv import load_dotenv
from langchain_openai import OpenAIEmbeddings

load_dotenv()


def get_embeddings_model(
    model_name: str = "text-embedding-3-small",
) -> OpenAIEmbeddings:
    return OpenAIEmbeddings(
        model=model_name,
        api_key=os.getenv("OPENAI_API_KEY"),
    )
