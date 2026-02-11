from pydantic import BaseModel
from typing import List

# Input format for the Job Description
class JobDescriptionInput(BaseModel):
    text: str
    top_k: int = 5  # Number of candidates to return (default 5)

# Output format for the matched candidates
class MatchResult(BaseModel):
    filename: str
    match_score: float