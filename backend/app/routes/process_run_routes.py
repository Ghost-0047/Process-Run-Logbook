from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.database.connection import SessionLocal
from app.models.pipeline import Pipeline
from app.models.process_run import ProcessRun

router = APIRouter()


class ProcessRunCreate(BaseModel):
    pipeline_id: int


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/runs/start")
def start_process_run(
    run: ProcessRunCreate,
    db: Session = Depends(get_db)
):
    pipeline = (
        db.query(Pipeline)
        .filter(Pipeline.id == run.pipeline_id)
        .first()
    )

    if not pipeline:
        raise HTTPException(
            status_code=404,
            detail="Pipeline not found"
        )

    new_run = ProcessRun(
        pipeline_id=run.pipeline_id,
        status="running"
    )

    db.add(new_run)
    db.commit()
    db.refresh(new_run)

    return new_run
