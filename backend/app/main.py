"""
main.py
-------
FastAPI application entry point.

Responsibilities:
  - Create the FastAPI app instance with metadata.
  - Configure CORS so the React frontend (localhost:5173) can talk to the API.
  - Auto-create all database tables on startup (SQLAlchemy create_all).
  - Register all API routers under the /api/v1 prefix.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.database import engine
# Import all models so SQLAlchemy's create_all discovers them before running
from app.models import user, project, report, ai_chat  # noqa: F401
from app.core.database import Base
from app.routers import auth as auth_router

# ---------------------------------------------------------------------------
# App instance
# ---------------------------------------------------------------------------
app = FastAPI(
    title="Weekly Report Generator API",
    description=(
        "Backend API for the Weekly Report Generator & Team Dashboard. "
        "Supports JWT authentication, role-based access control (Team Member / Manager), "
        "weekly report lifecycle management, project tracking, and analytics."
    ),
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

# ---------------------------------------------------------------------------
# CORS Middleware
# WHY: The React dev server runs on port 5173, the API on 8000.
# Without CORS headers, browsers block cross-origin requests.
# In production, replace "*" origins with the actual deployed frontend URL.
# ---------------------------------------------------------------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://localhost:3000",
        "http://127.0.0.1:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---------------------------------------------------------------------------
# Database table creation on startup
# WHY create_all: For development convenience, tables are created automatically
# when the server boots. In production you would replace this with Alembic
# migrations for zero-downtime schema changes.
# ---------------------------------------------------------------------------
@app.on_event("startup")
def on_startup():
    Base.metadata.create_all(bind=engine)


# ---------------------------------------------------------------------------
# Routers — all versioned under /api/v1
# ---------------------------------------------------------------------------
API_PREFIX = "/api/v1"

app.include_router(auth_router.router, prefix=API_PREFIX)


# ---------------------------------------------------------------------------
# Health check
# ---------------------------------------------------------------------------
@app.get("/health", tags=["Health"])
def health_check():
    """Simple liveness probe — returns 200 OK if the server is running."""
    return {"status": "ok", "version": "1.0.0"}
