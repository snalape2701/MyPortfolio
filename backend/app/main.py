import json
import os
from datetime import datetime
from typing import List, Optional
from fastapi import FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, EmailStr, Field

# Initialize FastAPI App
app = FastAPI(
    title="Luxury Portfolio Backend API",
    description="High-fidelity API to power contact form submissions, analytics, and projects metadata.",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Enable CORS for frontend integration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify frontend origin
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# File path for saving submissions
SUBMISSIONS_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "submissions.json")

# Pydantic Schemas
class ContactSubmission(BaseModel):
    name: str = Field(..., min_length=2, max_length=100, example="John Doe")
    email: EmailStr = Field(..., example="john.doe@example.com")
    message: str = Field(..., min_length=10, max_length=2000, example="Hi Sahil! I would love to collaborate on a luxury real-estate website.")

class ContactResponse(BaseModel):
    success: bool
    message: str
    submission_id: str
    timestamp: str

class MetaResponse(BaseModel):
    name: str
    role: str
    tech_stack: List[str]
    status: str

# Endpoints
@app.get("/", response_model=MetaResponse, status_code=status.HTTP_200_OK)
def read_root():
    """
    Root endpoint serving basic developer and API metadata.
    """
    return MetaResponse(
        name="Sahil Talape",
        role="Full Stack Developer",
        tech_stack=["HTML5", "Tailwind CSS", "JavaScript", "Python", "FastAPI"],
        status="API running smoothly"
    )

@app.post("/api/contact", response_model=ContactResponse, status_code=status.HTTP_201_CREATED)
def submit_contact(submission: ContactSubmission):
    """
    Saves a contact form submission to a localized persistent JSON store and echoes validation.
    """
    try:
        # Load existing submissions
        submissions = []
        if os.path.exists(SUBMISSIONS_FILE):
            with open(SUBMISSIONS_FILE, "r", encoding="utf-8") as f:
                try:
                    submissions = json.load(f)
                except json.JSONDecodeError:
                    pass  # If file is empty or corrupted, start fresh

        # Build new submission record
        submission_id = f"sub_{int(datetime.utcnow().timestamp())}"
        timestamp = datetime.utcnow().isoformat() + "Z"
        
        record = {
            "id": submission_id,
            "name": submission.name,
            "email": submission.email,
            "message": submission.message,
            "timestamp": timestamp
        }
        
        # Append and save
        submissions.append(record)
        with open(SUBMISSIONS_FILE, "w", encoding="utf-8") as f:
            json.dump(submissions, f, indent=4, ensure_ascii=False)
            
        return ContactResponse(
            success=True,
            message="Your message has been safely received. Sahil will get back to you shortly!",
            submission_id=submission_id,
            timestamp=timestamp
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An unexpected server error occurred: {str(e)}"
        )

@app.get("/api/submissions", status_code=status.HTTP_200_OK)
def get_submissions():
    """
    Utility endpoint to read past submissions (For review/debugging).
    """
    if os.path.exists(SUBMISSIONS_FILE):
        with open(SUBMISSIONS_FILE, "r", encoding="utf-8") as f:
            try:
                return json.load(f)
            except json.JSONDecodeError:
                return []
    return []
