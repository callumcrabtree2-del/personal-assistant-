from langchain_anthropic import ChatAnthropic
from langchain_core.messages import HumanMessage, AIMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.tools import tool
from langchain_classic.agents import create_tool_calling_agent, AgentExecutor
from config import ANTHROPIC_API_KEY
from search import search_web as _search_web
from memory import add_conversation, get_memory_summary

# Wrap search as a proper LangChain tool so the agent decides when to call it
@tool
def search_web(query: str) -> str:
    """Search the web for current information about a topic."""
    return _search_web(query)

# Declarative prompt template
prompt = ChatPromptTemplate.from_messages([
    ("system", """You are a helpful personal assistant with memory of past conversations.
Use the search_web tool when you need current information or facts you don't know.
Always be friendly, clear and concise.

{memory_summary}"""),
    MessagesPlaceholder("chat_history"),
    ("human", "{input}"),
    MessagesPlaceholder("agent_scratchpad"),
])

# LLM, agent, and executor
llm = ChatAnthropic(
    model="claude-sonnet-4-20250514",
    api_key=ANTHROPIC_API_KEY,
    temperature=0.7
)
agent = create_tool_calling_agent(llm, [search_web], prompt)
agent_executor = AgentExecutor(agent=agent, tools=[search_web], verbose=True)

# Store conversation history for current session
chat_history = []

def chat(user_message, image_data=None, image_media_type=None):
    memory_summary = get_memory_summary()

    # For multimodal messages, build a HumanMessage with image content directly
    if image_data and image_media_type:
        multimodal_message = HumanMessage(content=[
            {
                "type": "image_url",
                "image_url": {"url": f"data:{image_media_type};base64,{image_data}"}
            },
            {"type": "text", "text": user_message}
        ])
        # Invoke the LLM directly for image messages (AgentExecutor doesn't support multimodal input)
        from langchain_core.messages import SystemMessage
        system_message = SystemMessage(content=f"""You are a helpful personal assistant with memory of past conversations.
Always be friendly, clear and concise.

{memory_summary}""")
        response = llm.invoke([system_message] + chat_history + [multimodal_message])
        content = response.content
        if isinstance(content, list):
            response_text = "".join(
                block.get("text", "") if isinstance(block, dict) else str(block)
                for block in content
            )
        else:
            response_text = content
        chat_history.append(multimodal_message)
        chat_history.append(AIMessage(content=response_text))
    else:
        result = agent_executor.invoke({
            "input": user_message,
            "chat_history": chat_history,
            "memory_summary": memory_summary,
        })
        output = result["output"]
        if isinstance(output, list):
            response_text = "".join(
                block.get("text", "") if isinstance(block, dict) else str(block)
                for block in output
            )
        else:
            response_text = output
        chat_history.append(HumanMessage(content=user_message))
        chat_history.append(AIMessage(content=response_text))

    # Save to long-term memory
    add_conversation("user", user_message)
    add_conversation("assistant", response_text)

    return response_text