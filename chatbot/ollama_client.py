import requests


OLLAMA_URL = "http://127.0.0.1:11434/api/generate"
OLLAMA_MODEL = "llama3.2:3b"


def ask_ollama(prompt):
    """
    Send a prompt to the local Ollama model
    and return the generated response.
    """

    payload = {
        "model": OLLAMA_MODEL,
        "prompt": prompt,
        "stream": False,
    }

    try:

        response = requests.post(
            OLLAMA_URL,
            json=payload,
            timeout=120,
        )

        response.raise_for_status()

        data = response.json()

        return data.get(
            "response",
            "Sorry, I could not generate a response.",
        )

    except requests.RequestException as error:

        return (
            "Unable to connect to the AI service. "
            f"Error: {error}"
        )