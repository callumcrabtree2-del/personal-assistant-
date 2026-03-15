import chromadb
import os

# Connect to ChromaDB
os.makedirs("memory_store", exist_ok=True)
client = chromadb.PersistentClient(path="memory_store")
collection = client.get_or_create_collection(name="documents")

def load_text_file(file_path):
    # Read a text file
    with open(file_path, "r") as f:
        return f.read()

def split_into_chunks(text, chunk_size=500):
    # Split text into smaller pieces
    words = text.split()
    chunks = []
    current_chunk = []
    current_size = 0
    
    for word in words:
        current_chunk.append(word)
        current_size += 1
        if current_size >= chunk_size:
            chunks.append(" ".join(current_chunk))
            current_chunk = []
            current_size = 0
    
    if current_chunk:
        chunks.append(" ".join(current_chunk))
    
    return chunks

def store_document(file_path):
    # Read and store a document in ChromaDB
    text = load_text_file(file_path)
    chunks = split_into_chunks(text)
    filename = os.path.basename(file_path)
    
    for i, chunk in enumerate(chunks):
        collection.add(
            documents=[chunk],
            ids=[f"{filename}_chunk_{i}"],
            metadatas=[{"source": filename}]
        )
    
    return f"Stored {len(chunks)} chunks from {filename}"

def search_documents(query, n_results=3):
    # Search your documents for relevant info
    count = collection.count()
    if count == 0:
        return "No documents loaded yet."
    
    results = collection.query(
        query_texts=[query],
        n_results=min(n_results, count)
    )
    
    context = ""
    for i, doc in enumerate(results["documents"][0]):
        source = results["metadatas"][0][i]["source"]
        context += f"From {source}:\n{doc}\n\n"
    
    return context
