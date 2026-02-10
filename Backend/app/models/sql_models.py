from sqlalchemy import Column, Integer, String, Float, DateTime
from datetime import datetime
from app.db.database import Base

class Candidate(Base):
    __tablename__ = "candidates"

    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String, nullable=True)
    email = Column(String, nullable=True)
    filename = Column(String, unique=True, index=True)
    file_path = Column(String)
    upload_date = Column(DateTime, default=datetime.utcnow)
    
    # We can store the vector ID here to link with ChromaDB if needed
    vector_id = Column(String, unique=True)