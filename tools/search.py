from tavily import TavilyClient
from config import TAVILY_API_KEY

# Create the search client
search_client = TavilyClient(api_key=TAVILY_API_KEY)

def search_web(query):
    try:
        # Search the web and get results
        results = search_client.search(
            query=query,
            max_results=3
        )

        # Extract just the text from the results
        search_summary = ""
        for result in results["results"]:
            search_summary += f"Source: {result['url']}\n"
            search_summary += f"Content: {result['content']}\n\n"

        return search_summary
    
    except Exception as e:
        return "Search unavailable right now, answering from my own knowledge."
    