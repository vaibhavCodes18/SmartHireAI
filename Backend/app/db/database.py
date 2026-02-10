from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# 1. Create the database file (resumes.db) in the root folder
SQLALCHEMY_DATABASE_URL = "sqlite:///./resumes.db"

# 2. Initialize the Engine
# check_same_thread=False is needed only for SQLite
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

# 3. Create a SessionLocal class (we use this to talk to the DB)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 4. Create a Base class (all our models will inherit from this)
Base = declarative_base()

# Dependency function to get a DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()