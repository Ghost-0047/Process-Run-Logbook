from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.database.connection import SessionLocal
from app.models.pipeline import Pipeline


router = APIRouter()


class PipelineCreate(BaseModel):
    """Data required to register a new pipeline."""
    name: str
    description: str | None = None


def get_db():
    """Provide a database session for each API request."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/pipelines")
def create_pipeline(
    pipeline: PipelineCreate,
    db: Session = Depends(get_db)
):
    """Register a new pipeline in the Process Run Logbook."""

    existing_pipeline = (
        db.query(Pipeline)
        .filter(Pipeline.name == pipeline.name)
        .first()
    )

    if existing_pipeline:
        raise HTTPException(
            status_code=400,
            detail="Pipeline with this name already exists"
        )

    new_pipeline = Pipeline(
        name=pipeline.name,
        description=pipeline.description
    )

    db.add(new_pipeline)
    db.commit()
    db.refresh(new_pipeline)

    return new_pipeline


@router.get("/pipelines")
def get_pipelines(db: Session = Depends(get_db)):
    """Return all registered pipelines."""

    return db.query(Pipeline).all()
