import chromadb
from chromadb.config import Settings
import os

# Define where to save the database locally
CHROMA_DB_DIR = os.path.join(os.getcwd(), "chroma_db")

# Initialize the Client (Persistent = saves to disk)
client = chromadb.PersistentClient(path=CHROMA_DB_DIR)

# Create or Get a Collection (think of this like a "Table" in SQL)
# We call it "resumes_collection"
collection = client.get_or_create_collection(
    name="resumes_collection",
    metadata={"hnsw:space": "cosine"}  # Use Cosine Similarity
)

def add_resume_to_vector_db(resume_id: str, text: str, embedding: list, metadata: dict):
    """
    Saves a resume's vector and metadata to ChromaDB.
    """
    collection.add(
        ids=[resume_id],            # Unique ID (e.g., filename)
        documents=[text],           # The raw text (optional, but good for reference)
        embeddings=[embedding],     # The AI Vector (List of floats)
        metadatas=[metadata]        # Extra info (Name, Email, etc.)
    )

def query_resumes(query_embedding: list, n_results=5):
    """
    Searches for the top N most similar resumes.
    """
    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=n_results
    )
    return results