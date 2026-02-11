import os
import pickle
from sentence_transformers import SentenceTransformer

# 1. Initialize the BERT Model (For Feature Extraction)
model = SentenceTransformer('all-MiniLM-L6-v2')

# 2. Load the Trained SVM Classifier and Label Encoder
MODEL_PATH = os.path.join(os.getcwd(), r"P:\SmartHireAI\Backend\app\ML_Model\resume_classifier_svm.pkl")
ENCODER_PATH = os.path.join(os.getcwd(), r"P:\SmartHireAI\Backend\app\ML_Model\label_encoder.pkl")

# We use global variables so they load only once when the server starts
clf = None
label_encoder = None

try:
    if os.path.exists(MODEL_PATH) and os.path.exists(ENCODER_PATH):
        with open(MODEL_PATH, "rb") as f:
            clf = pickle.load(f)
        with open(ENCODER_PATH, "rb") as f:
            label_encoder = pickle.load(f)
        print("ML Classifier and Encoder loaded successfully!")
    else:
        print("Warning: .pkl files not found. Run the Jupyter Notebook first.")
except Exception as e:
    print(f"Error loading models: {e}")

# 3. Functions
def get_embedding(text: str):
    """Converts text into a BERT vector."""
    if not text or len(text) < 10:
        return []
    embedding = model.encode(text)
    return embedding.tolist()

def predict_category(embedding: list) -> str:
    """Uses the trained SVM to predict the job category from the vector."""
    if not clf or not label_encoder or not embedding:
        return "Uncategorized"
    
    # The classifier expects a 2D array (a list of lists)
    prediction = clf.predict([embedding])
    
    # Convert the predicted number back to the text label (e.g., "Java_Developer")
    category = label_encoder.inverse_transform(prediction)[0]
    return category