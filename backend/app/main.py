from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from sqlalchemy import text
from . import database, models

app = FastAPI(title="Internship Intelligence Agent", version="0.1.0")

# Ensure database tables exist (Development fallback)
models.Base.metadata.create_all(bind=database.engine)

@app.get("/health")
def health_check(db: Session = Depends(database.get_db)):
    # Basic check to ensure the db is accessible
    try:
        db.execute(text("SELECT 1"))
        db_status = "ok"
    except Exception as e:
        db_status = f"failed: {str(e)}"

    return {"status": "ok", "db": db_status}

from pydantic import BaseModel
from typing import List
from .orchestrator import Orchestrator
from .parser import RequestParser

class NaturalLanguageRequest(BaseModel):
    query: str

class IngestRequest(BaseModel):
    file_path: str

@app.get("/")
def read_root():
    return {"message": "Welcome to the Internship Intelligence Agent API"}

@app.post("/api/research")
def natural_language_research(request: NaturalLanguageRequest, db: Session = Depends(database.get_db)):
    """Handles natural language queries (Phase 28)."""
    parser = RequestParser()
    structured_query = parser.parse_natural_language(request.query)
    # In a full app, this would trigger background Redis tasks.
    return {"status": "accepted", "query": structured_query}

@app.get("/api/opportunities")
def get_opportunities(db: Session = Depends(database.get_db)):
    """Returns opportunities for the dashboard (Phase 24)."""
    ops = db.query(models.Opportunity).order_by(models.Opportunity.overall_score.desc()).limit(50).all()

    # Format for the frontend
    results = []
    for op in ops:
        results.append({
            "id": op.id,
            "company": op.company.name if op.company else "Unknown",
            "contact": op.person.name if op.person else "Unknown",
            "status": op.status,
            "score": op.overall_score,
            "date": op.created_at.strftime("%Y-%m-%d")
        })
    return {"opportunities": results}

@app.post("/api/ingest")
async def ingest_contacts(request: IngestRequest, db: Session = Depends(database.get_db)):
    """Triggers the orchestrator pipeline manually on an ingested list."""
    # This is a stub showing how the orchestrator integrates.
    orch = Orchestrator(db)

    # Mock data for demonstration
    raw = {"name": "Jane Doe", "company": "Acme AI", "title": "CTO"}
    profile = {"skills": ["Python"]}
    template = "Hi {contact_name}..."

    result = await orch.run_pipeline(raw, profile, template)
    return result
