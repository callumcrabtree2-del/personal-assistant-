import chromadb
import os

# Create a folder to store memories
os.makedirs("memory_store", exist_ok=True)

# Connect to ChromaDB
client = chromadb.PersistentClient(path="memory_store")

# Create a collection to store conversations
collection = client.get_or_create_collection(name="chat_history")

def save_memory(user_message, assistant_response):
    # Save the conversation to ChromaDB
    collection.add(
        documents=[f"User: {user_message}\nAssistant: {assistant_response}"],
        ids=[str(collection.count() + 1)]
    )

def get_relevant_memories(query, n_results=3):
    # Search for relevant past conversations
    count = collection.count()
    if count == 0:
        return ""
    
    results = collection.query(
        query_texts=[query],
        n_results=min(n_results, count)
    )
    
    memories = ""
    for doc in results["documents"][0]:
        memories += f"{doc}\n\n"
    
    return memories
