import sys

from dotenv import load_dotenv
from openai import OpenAI

from ingest import load_faq_data, build_index
from metrics import RAGWithMetrics

def create_assistant():
    load_dotenv()

    documents = load_faq_data()
    index = build_index(documents)

    return RAGWithMetrics(
        index=index,
        llm_client=OpenAI()
    )