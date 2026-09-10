from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from sqlalchemy import text
from . import database, models

app = FastAPI(title="Internship Intelligence Agent", version="0.1.0")

@app.get("/health")
def health_check(db: Session = Depends(database.get_db)):
    # Basic check to ensure the db is accessible
    try:
        db.execute(text("SELECT 1"))
        db_status = "ok"
    except Exception as e:
        db_status = f"failed: {str(e)}"

    return {"status": "ok", "db": db_status}

@app.get("/")
def read_root():
    return {"message": "Welcome to the Internship Intelligence Agent API"}
