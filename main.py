from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from routes.projects import router as projects_router

# Database configuration
SQLALCHEMY_DATABASE_URL = "sqlite:///./projects.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Initialize FastAPI app
app = FastAPI(
    title="iOS Compliance Project Management API",
    description="API for managing iOS projects with compliance tracking",
    version="1.0.0"
)

# CORS Configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(projects_router, prefix="/api/v1", tags=["projects"])

# Database tables creation (run once)
@app.on_event("startup")
def startup():
    Base.metadata.create_all(bind=engine)

# Health check endpoint
@app.get("/health")
async def health_check():
    return {"status": "healthy"}