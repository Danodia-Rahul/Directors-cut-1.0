import os
import retrieval.search
from google import genai
from dotenv import load_dotenv


load_dotenv()


GOOGLE_API_KEY = os.environ.get("GOOGLE_API_KEY")
google_client = genai.Client(api_key=GOOGLE_API_KEY)

def get_response(question: str, model: str = 'gemini-2.5-flash'):

    input_prompt = """

        You are given:
        1. A question.
        2. Two context passages (context1 and context2).

        Your task:
        - Answer the question using only the given contexts.
        - If both contexts provide relevant information, combine them into a complete answer.
        - If the contexts are insufficient, explicitly state that the answer cannot be fully determined.
        - Make the response well-structured, clear, and directly connected to the question.

        Input format:

        question: {question}
        context1: {context1}
        context2: {context2}

    """.strip()

    context_docs = retrieval.search.rrf_search(question=question, collection_name='hybrid-search-collection')
    prompt = input_prompt.format(**context_docs)

    response = google_client.models.generate_content(
        model = model,
        contents = prompt
    )

    return response.text