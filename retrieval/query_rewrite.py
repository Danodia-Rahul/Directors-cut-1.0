from retrieval.response import google_client

def rewrite_query(text_input: str):
    prompt = """

    You will be given an input text string that may contain spelling mistakes, grammatical errors, or awkward sentence structure. 
    Your task is to rewrite the text to make it clear, grammatically correct, and well-structured, while preserving the original meaning and intent. 
    Do not add new ideas or change the message; only improve readability and correctness.

    Input:
    {text}

    Output:
    A polished, error-free version of the input text.

    """.strip()
    
    modified_query = google_client.models.generate_content(
        model = 'gemini-2.5-flash-lite',
        contents = prompt.format(text=text_input)
    )

    return modified_query
