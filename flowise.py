import requests

FLOWISE_API_URL = "http://localhost:3000/api/v1/prediction/291a36f1-2421-492c-ad35-44cdc0eb2f6b"

def query_flowise(question: str) -> str:
    """Send a message to Flowise and get a response."""
    try:
        response = requests.post(FLOWISE_API_URL, json={"question": question})
        data = response.json()
        return data.get("text", "")
    except Exception as e:
        return ""

def get_flowise_memory(user_message: str) -> str:
    """Query Flowise to get memory context for the current message."""
    try:
        context_query = f"Based on our conversation history, what do you remember that is relevant to this: {user_message}"
        response = requests.post(FLOWISE_API_URL, json={"question": context_query})
        data = response.json()
        memory = data.get("text", "")
        if memory:
            return f"\n\nFlowise Memory Context:\n{memory}"
        return ""
    except Exception as e:
        return ""