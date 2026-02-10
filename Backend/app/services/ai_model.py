from sentence_transformers import SentenceTransformer

# Initialize the model globally so we don't reload it for every request
# 'all-MiniLM-L6-v2' is fast and accurate for semantic similarity
model = SentenceTransformer('all-MiniLM-L6-v2')

def get_embedding(text: str):
    """
    Converts a text string into a vector embedding (list of floats).
    """
    if not text or len(text) < 10:
        return []
    
    # Generate embedding
    embedding = model.encode(text)
    
    # Convert numpy array to simple list (for JSON serialization)
    return embedding.tolist()