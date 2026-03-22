from langchain_anthropic import ChatAnthropic
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage
from config import ANTHROPIC_API_KEY
from search import search_web
from memory import add_conversation, get_memory_summary

# Create the Claude AI model
llm = ChatAnthropic(
    model="claude-sonnet-4-20250514",
    api_key=ANTHROPIC_API_KEY,
    temperature=0.7
)

# Store conversation history for current session
chat_history = []

def chat(user_message, image_data=None, image_media_type=None):
    # Load memory summary from past conversations
    memory_summary = get_memory_summary()

    # Build system message with memory included
    system_message = SystemMessage(content=f"""
You are a helpful personal assistant with memory of past conversations.
When you need current information or facts you don't know,
use the search results provided to you.
Always be friendly, clear and concise.

{memory_summary}
""")

    # Search the web for relevant information
    search_results = search_web(user_message)

    # Combine user message with search results
    enhanced_text = f"""
User question: {user_message}

Here are some relevant search results to help answer:
{search_results}

Please answer the user's question using the search results where relevant.
"""

    # Build message content — multimodal if image provided
    if image_data and image_media_type:
        message_content = [
            {
                "type": "image_url",
                "image_url": {"url": f"data:{image_media_type};base64,{image_data}"}
            },
            {"type": "text", "text": enhanced_text}
        ]
    else:
        message_content = enhanced_text

    # Add to current session history
    chat_history.append(HumanMessage(content=message_content))

    # Get response from Claude
    response = llm.invoke([system_message] + chat_history)

    # Add response to current session history
    chat_history.append(AIMessage(content=response.content))

    # Save to long term memory
    add_conversation("user", user_message)
    add_conversation("assistant", response.content)

    return response.content