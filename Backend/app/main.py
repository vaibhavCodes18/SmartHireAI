from fastapi import FastAPI

app = FastAPI(title="Smart Hire AI - Resume Shortlister")


@app.get("/")
def health_check():
    return {"status": "running", "message": "Smart Hire AI Backend is Ready"}
