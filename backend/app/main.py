from fastapi import FastAPI

from app.database.connection import engine, Base
from app.models.pipeline import Pipeline
from app.models.process_run import ProcessRun
from app.routes.pipeline_routes import router as pipeline_router
from app.routes.process_run_routes import router as process_run_router

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(pipeline_router)
app.include_router(process_run_router)


@app.get("/")
def home():
    return {"message": "Process Run Logbook API is running"}
