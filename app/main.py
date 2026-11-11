
from dotenv import load_dotenv

load_dotenv()

from fastapi import FastAPI

from app.routes.mailroom import router
from app.database.db import initialize_database


app = FastAPI(
    title="AI Mailroom Agent",
    description="AI-powered secure email analysis and routing",
    version="1.0.0"
)


@app.on_event("startup")
def startup():

    initialize_database()


app.include_router(router)


@app.get("/")
def home():

    return {
        "service": "AI Mailroom Agent",
        "status": "running"
    }


@app.get("/health")
def health():

    return {
        "status": "healthy"
    }
