from typing import List 
import os
import shutil
import uuid
from fastapi import APIRouter, UploadFile, File, HTTPException

from app.services.pdf_parser import extract_text_from_pdf
from app.services.text_cleaner import clean_text
from app.services.ai_model import get_embedding, predict_category
from app.db.vector_store import add_resume_to_vector_db, query_resumes
from app.models.schemas import JobDescriptionInput, MatchResult

router = APIRouter()

# Ensure uploads directory exists
UPLOAD_DIR = os.path.join(os.getcwd(), "uploads")
os.makedirs(UPLOAD_DIR, exist_ok=True)

# ... (keep your UPLOAD_DIR setup) ...

@router.post("/upload")
async def upload_multiple_resumes(files: List[UploadFile] = File(...)):
    """
    Accepts MULTIPLE PDF files at once.
    Processes each one: extracts text, predicts category, and saves to Vector DB.
    """
    if not files:
        raise HTTPException(status_code=400, detail="No files uploaded.")

    processed_results = []

    # Loop through every uploaded file
    for file in files:
        if not file.filename.endswith(".pdf"):
            processed_results.append({"filename": file.filename, "status": "Failed - Not a PDF"})
            continue # Skip to the next file

        try:
            # 1. Save locally
            file_path = os.path.join(UPLOAD_DIR, file.filename)
            with open(file_path, "wb") as buffer:
                shutil.copyfileobj(file.file, buffer)

            # 2. Extract & Clean
            raw_text = extract_text_from_pdf(file_path)
            if not raw_text:
                processed_results.append({"filename": file.filename, "status": "Failed - Empty/Unreadable PDF"})
                continue

            cleaned_text = clean_text(raw_text)
            
            # 3. AI Processing (Vector + Prediction)
            embedding = get_embedding(cleaned_text)
            predicted_category = predict_category(embedding)

            # 4. Save to ChromaDB
            vector_id = str(uuid.uuid4())
            metadata = {
                "filename": file.filename, 
                "filepath": file_path,
                "predicted_category": predicted_category
            }
            
            add_resume_to_vector_db(
                resume_id=vector_id, 
                text=cleaned_text, 
                embedding=embedding, 
                metadata=metadata
            )

            # Record success
            processed_results.append({
                "filename": file.filename, 
                "status": "Success",
                "predicted_category": predicted_category
            })

        except Exception as e:
            processed_results.append({"filename": file.filename, "status": f"Error: {str(e)}"})

    # Return a summary of the batch upload
    return {
        "message": f"Batch processed {len(files)} files.",
        "results": processed_results
    }

# ... (keep your /match route exactly the same as before) ...

@router.post("/match", response_model=list[MatchResult])
async def match_resumes(jd: JobDescriptionInput):
    """
    1. Cleans the Job Description.
    2. Generates AI Vector for the JD.
    3. Queries ChromaDB for the closest resume vectors.
    """
    # 1. Clean and Vectorize the JD
    cleaned_jd = clean_text(jd.text)
    jd_embedding = get_embedding(cleaned_jd)

    # 2. Query the Vector Database
    results = query_resumes(query_embedding=jd_embedding, n_results=jd.top_k)

    # 3. Format the Results
    matches = []
    
    # ChromaDB returns a dictionary with lists of ids, distances, and metadatas
    if results and results['distances'] and len(results['distances'][0]) > 0:
        distances = results['distances'][0]
        metadatas = results['metadatas'][0]
        
        for i in range(len(distances)):
            # Convert distance to a similarity percentage (roughly)
            # Cosine distance ranges from 0 to 2. Smaller distance = higher similarity.
            similarity_score = max(0.0, 1.0 - distances[i]) * 100
            
            matches.append(MatchResult(
                filename=metadatas[i].get("filename", "Unknown"),
                match_score=round(similarity_score, 2)
            ))
            
    return matches