from fastapi import FastAPI
from app.db.database import engine, Base
from app.models import sql_models # Import your models so SQL knows about them

# Create the database tables automatically on startup
Base.metadata.create_all(bind=engine)

app = FastAPI(title="AI Resume Shortlister")

@app.get("/")
def health_check():
    return {"status": "running", "message": "Database & Backend Ready"}