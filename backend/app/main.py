from fastapi import FastAPI

from app.database.connection import engine, Base
from app.models.pipeline import Pipeline
from app.routes.pipeline_routes import router as pipeline_router

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(pipeline_router)

@app.get("/")
def home():
    return {"message": "Process Run Logbook API is running"}
