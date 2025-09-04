import os
import hybrid.search
from google import genai


GOOGLE_API_KEY = os.environ.get("GOOGLE_API_KEY")

google_client = genai.Client(api_key=GOOGLE_API_KEY)

def get_response(question: str, model: str = 'gemini-2.5-flash-lite'):

    input_prompt = """

        You will be given:
        1. A question.  
        2. Five context paragraphs (labeled context1 through context5).  

        Your task:  
        - Answer the question **using only the information provided in the contexts**.  
        - Do not use outside knowledge.  
        - If the contexts do not contain enough information to fully answer, say so explicitly.  
        - Make the answer clear, concise, and directly related to the question.  

        Input format:  

        question: {question}  
        context1: {context1}  
        context2: {context2}  
        context3: {context3}  
        context4: {context4}  
        context5: {context5}  

    """.strip()

    context_docs = hybrid.search.rrf_search(question=question, collection_name='hybrid-search-collection')
    prompt = input_prompt.format(**context_docs)

    response = google_client.models.generate_content(
        model = model,
        contents = prompt
    )

    return response.text