import spacy
import re

# Load the English model we downloaded
nlp = spacy.load("en_core_web_sm")

def clean_text(text: str) -> str:
    """
    Cleans raw text by:
    1. Lowercasing everything.
    2. Removing special characters and emails.
    3. Removing stop words (the, and, is) and punctuation.
    4. Lemmatization (converting 'running' -> 'run').
    """
    # 1. Basic cleanup: Lowercase & remove newlines
    text = text.lower().strip()
    
    # 2. Remove emails (privacy/noise reduction)
    text = re.sub(r'\S+@\S+', '', text)
    
    # 3. Remove special characters (keep only words and numbers)
    text = re.sub(r'[^a-z0-9\s]', '', text)
    
    # 4. SpaCy processing
    doc = nlp(text)
    
    # 5. Filter tokens: Keep only if NOT stopword AND NOT punctuation
    cleaned_tokens = [
        token.lemma_ for token in doc 
        if not token.is_stop and not token.is_punct and len(token.text) > 2
    ]
    
    return " ".join(cleaned_tokens)