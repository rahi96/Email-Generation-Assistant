"""
main.py - FastAPI Application Entry Point.

Initializes the FastAPI app, registers routers, creates database tables,
and configures CORS middleware.

Run with: uvicorn app.main:app --reload
Docs at:  http://127.0.0.1:8000/docs
"""

import logging
import sys

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.database import engine, Base
from app.models.email_log import EmailLog  # noqa: F401 — needed for table creation
from app.api.routes import email as email_router
from app.api.routes import evaluation as evaluation_router

# --- Logging Setup ---
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)-7s | %(name)s | %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)],
)
logger = logging.getLogger(__name__)

# --- Create database tables ---
Base.metadata.create_all(bind=engine)
logger.info("Database tables created (if not existing)")

# --- FastAPI App Initialization ---
app = FastAPI(
    title="Email Generation Assistant",
    description=(
        "An LLM-powered Email Generation Assistant with advanced prompt engineering "
        "and a custom evaluation framework. Built with FastAPI and OpenAI GPT-4o-mini."
    ),
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

# --- CORS Middleware ---
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- Register Routers ---
API_V1_PREFIX = "/api/v1"
app.include_router(email_router.router, prefix=API_V1_PREFIX)
app.include_router(evaluation_router.router, prefix=API_V1_PREFIX)


@app.get("/", tags=["Health"])
def root():
    """Health check endpoint."""
    return {
        "service": "Email Generation Assistant",
        "version": "1.0.0",
        "status": "healthy",
        "docs": "/docs",
    }


@app.get("/health", tags=["Health"])
def health_check():
    """Detailed health check."""
    return {
        "status": "healthy",
        "database": "sqlite (emails.db)",
        "model": "gpt-4o-mini",
        "endpoints": [
            "POST /api/v1/email/generate",
            "POST /api/v1/evaluation/run",
        ],
    }
