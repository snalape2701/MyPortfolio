import json
import os
import logging
from datetime import datetime
from typing import List, Optional
from fastapi import FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, EmailStr, Field

# Load env variables at the absolute top before any internal package imports
from dotenv import load_dotenv
load_dotenv()

# Safe absolute imports
try:
    from app.supabase_client import get_supabase_client
except ImportError:
    from supabase_client import get_supabase_client

# Configure Logger
logger = logging.getLogger("main")
logging.basicConfig(level=logging.INFO)

# Initialize FastAPI App
app = FastAPI(
    title="Luxury Portfolio Backend API",
    description="High-fidelity API to power contact form submissions, analytics, projects, and work experience.",
    version="1.1.0",
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

# File path for saving local submissions (Fallback Store)
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
    database_mode: str

class ProjectResponse(BaseModel):
    id: Optional[str] = None
    title: str
    description: str
    technologies: List[str]
    github_url: str
    demo_url: str
    image_url: str

class ExperienceResponse(BaseModel):
    id: Optional[str] = None
    role: str
    company: str
    duration: str
    description: str


# FALLBACK SEED DATA (Used if Supabase is unconfigured or tables don't exist yet)
MOCK_PROJECTS = [
    {
        "id": "mock_p1",
        "title": "Aether Dashboard",
        "description": "A premium developer workspace containing advanced charts, deep memory usage telemetry, and customizable widget canvases.",
        "technologies": ["HTML5", "Tailwind CSS", "JS"],
        "github_url": "#",
        "demo_url": "#",
        "image_url": "assets/project-1.png"
    },
    {
        "id": "mock_p2",
        "title": "Helios Database Visualizer",
        "description": "A highly advanced developer dashboard displaying database schemas, custom node-linking flowcharts, and lightning fast FastAPI queries.",
        "technologies": ["FastAPI", "Python", "Git"],
        "github_url": "#",
        "demo_url": "#",
        "image_url": "assets/project-2.png"
    },
    {
        "id": "mock_p3",
        "title": "Vesper luxury shop",
        "description": "A premium e-commerce platform incorporating frosted-glass cards, fluid layouts, rose-gold accents, and dynamic catalog filters.",
        "technologies": ["HTML5", "Tailwind CSS", "REST API"],
        "github_url": "#",
        "demo_url": "#",
        "image_url": "assets/project-3.png"
    },
    {
        "id": "mock_p4",
        "title": "Synapse Prompt Engine",
        "description": "An advanced playground visualizer creating neural nodes, glowing AI output matrices, and responsive prompt debugging inputs.",
        "technologies": ["JavaScript", "Python", "Database"],
        "github_url": "#",
        "demo_url": "#",
        "image_url": "assets/project-4.png"
    },
    {
        "id": "mock_p5",
        "title": "Chronos Canvas",
        "description": "A real-time vector sketching and collaborative editing application designed with glowing UI pens, translucent rulers, and rapid responsive performance.",
        "technologies": ["HTML5", "JavaScript", "Git"],
        "github_url": "#",
        "demo_url": "#",
        "image_url": "assets/project-5.png"
    },
    {
        "id": "mock_p6",
        "title": "Zephyr DevOps Monitor",
        "description": "A premium cloud monitoring dashboard rendering active nodes, real-time error telemetry logs, and optimized server routing statistics.",
        "technologies": ["FastAPI", "Python", "REST API"],
        "github_url": "#",
        "demo_url": "#",
        "image_url": "https://images.unsplash.com/photo-1558494949-ef010cbdcc31?auto=format&fit=crop&w=800&q=80"
    }
]

MOCK_EXPERIENCES = [
    {
        "id": "mock_e1",
        "role": "Senior Full Stack Developer",
        "company": "TechNova Solutions",
        "duration": "2024 - Present",
        "description": "Architecting high-fidelity cloud dashboards using FastAPI and custom-styled glassmorphic frontend layouts. Optimized query responsiveness by 40%."
    },
    {
        "id": "mock_e2",
        "role": "Full Stack Engineer",
        "company": "Quantum Labs",
        "duration": "2021 - 2024",
        "description": "Built reactive backend APIs using Python and designed custom responsive landing systems. Successfully managed microservices scaling up to 10k DAU."
    }
]


# Endpoints
@app.get("/", response_model=MetaResponse, status_code=status.HTTP_200_OK)
def read_root():
    """
    Root endpoint serving developer meta-information and active database modes.
    """
    supabase = get_supabase_client()
    db_mode = "SUPABASE_ACTIVE" if supabase else "LOCAL_JSON_FALLBACK"
    return MetaResponse(
        name="Sahil Talape",
        role="Full Stack Developer",
        tech_stack=["HTML5", "Tailwind CSS", "JavaScript", "Python", "FastAPI", "Supabase"],
        status="API running smoothly",
        database_mode=db_mode
    )

@app.get("/api/projects", response_model=List[ProjectResponse], status_code=status.HTTP_200_OK)
def get_projects():
    """
    Fetches portfolio projects from Supabase. Falls back to static mock seed data if disconnected.
    """
    supabase = get_supabase_client()
    if not supabase:
        logger.info("Serving projects from local fallback database.")
        return MOCK_PROJECTS
    
    try:
        response = supabase.table("projects").select("*").execute()
        # If response has elements, return them, else return mock data to prevent blank screen
        if response.data and len(response.data) > 0:
            return response.data
        logger.warning("Supabase table 'projects' is empty. Serving seed mock projects.")
        return MOCK_PROJECTS
    except Exception as e:
        logger.error(f"Supabase Projects query failure: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail=f"Supabase connection query failed: {str(e)}. Ensure 'projects' table is defined."
        )

@app.get("/api/experiences", response_model=List[ExperienceResponse], status_code=status.HTTP_200_OK)
def get_experiences():
    """
    Fetches experience rows from Supabase. Falls back to local structural array if disconnected.
    """
    supabase = get_supabase_client()
    if not supabase:
        logger.info("Serving experiences from local fallback database.")
        return MOCK_EXPERIENCES
    
    try:
        response = supabase.table("experiences").select("*").execute()
        if response.data and len(response.data) > 0:
            return response.data
        logger.warning("Supabase table 'experiences' is empty. Serving seed mock experience.")
        return MOCK_EXPERIENCES
    except Exception as e:
        logger.error(f"Supabase Experience query failure: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail=f"Supabase connection query failed: {str(e)}. Ensure 'experiences' table is defined."
        )

@app.post("/api/contact", response_model=ContactResponse, status_code=status.HTTP_201_CREATED)
def submit_contact(submission: ContactSubmission):
    """
    Saves a contact form submission directly to Supabase, falling back to a local JSON file.
    """
    supabase = get_supabase_client()
    timestamp = datetime.utcnow().isoformat() + "Z"
    submission_id = f"sub_{int(datetime.utcnow().timestamp())}"

    # 1. Try writing to Supabase
    if supabase:
        try:
            data = {
                "name": submission.name,
                "email": submission.email,
                "message": submission.message
            }
            # Perform write
            db_response = supabase.table("contact_submissions").insert(data).execute()
            if db_response.data:
                logger.info("Submission successfully saved in Supabase.")
                return ContactResponse(
                    success=True,
                    message="Your message has been received and saved securely in our Supabase database!",
                    submission_id=submission_id,
                    timestamp=timestamp
                )
        except Exception as e:
            logger.warning(f"Failed to write to Supabase. Falling back to local JSON logger. Error: {str(e)}")
            # Fall through to local logger if DB write failed
            
    # 2. Local Fallback Logging (If Supabase is unconfigured or table write fails)
    try:
        submissions = []
        if os.path.exists(SUBMISSIONS_FILE):
            with open(SUBMISSIONS_FILE, "r", encoding="utf-8") as f:
                try:
                    submissions = json.load(f)
                except json.JSONDecodeError:
                    pass

        record = {
            "id": submission_id,
            "name": submission.name,
            "email": submission.email,
            "message": submission.message,
            "timestamp": timestamp,
            "storage": "Local JSON Fallback"
        }
        
        submissions.append(record)
        with open(SUBMISSIONS_FILE, "w", encoding="utf-8") as f:
            json.dump(submissions, f, indent=4, ensure_ascii=False)
            
        return ContactResponse(
            success=True,
            message="Your message is safely received! Running in Local JSON fallback mode.",
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
    Utility endpoint to read past local submissions (For review/debugging).
    """
    if os.path.exists(SUBMISSIONS_FILE):
        with open(SUBMISSIONS_FILE, "r", encoding="utf-8") as f:
            try:
                return json.load(f)
            except json.JSONDecodeError:
                return []
    return []
