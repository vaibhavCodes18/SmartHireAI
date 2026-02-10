# backend/init_chroma.py
from app.db.vector_store import collection

print("Initializing ChromaDB...")
print(f"Collection Name: {collection.name}")
print("Success! The 'chroma_db' folder should now exist.")