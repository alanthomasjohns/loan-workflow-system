import json
import requests


OLLAMA_URL = "http://localhost:11434/api/generate"


def extract_document_data(text: str) -> dict:

    prompt = f"""
        You are a document extraction system.
        Extract information from the document.
        Return ONLY valid JSON.
        Fields:
        - document_type
        - name
        - dob
        - id_number

        Document Text:
        {text}
    """

    response = requests.post(
        OLLAMA_URL,
        json={
            "model": "qwen2.5:3b",
            "prompt": prompt,
            "stream": False
        },
        timeout=120
    )

    result = response.json()

    try:
        return json.loads(result["response"])
    except Exception:
        return {
            "error": "invalid_json",
            "raw_response": result["response"]
        }