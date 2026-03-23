import requests

FLOWISE_API_URL = "http://localhost:3000/api/v1/prediction/291a36f1-2421-492c-ad35-44cdc0eb2f6b"

def query_flowise(question: str) -> str:
    try:
        response = requests.post(FLOWISE_API_URL, json={"question": question})
        data = response.json()
        return data.get("text", "Sorry, I could not get a response from the pipeline.")
    except Exception as e:
        return f"Flowise connection error: {str(e)}"
