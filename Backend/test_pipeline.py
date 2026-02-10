from app.services.text_cleaner import clean_text
from app.services.ai_model import get_embedding

# 1. Simulate Raw Text (as if it came from a PDF)
raw_resume = """
Vaibhav Sathe. 
Email: vaibhav@example.com. 
Experience: 5 years in Python, Machine Learning, and Data Science. 
Skills: React, FastAPI, SQL.
"""

print("--- Step 1: Raw Text ---")
print(raw_resume)

# 2. Test Cleaning
cleaned = clean_text(raw_resume)
print("\n--- Step 2: Cleaned Text ---")
print(cleaned)

# 3. Test Vectorization
vector = get_embedding(cleaned)
print("\n--- Step 3: Vector Embedding (First 10 numbers) ---")
print(vector[:10])  # Should print a list of floats like [0.012, -0.45, ...]
print(f"Total Dimensions: {len(vector)}")