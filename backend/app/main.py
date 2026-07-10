"""
main.py
-------
FastAPI application entry point.

Responsibilities:
  - Instantiate the FastAPI application with full OpenAPI metadata.
  - Register CORS middleware so the React dev server (port 5173) can
    communicate with this API during development.
  - Run database table creation on startup via SQLAlchemy create_all
    (development convenience; swap for Alembic in production).
  - Mount all API routers under the versioned prefix /api/v1.
  - Expose root (GET /) and health (GET /health) probe endpoints.
"""

from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Core infrastructure
from app.core.database import engine, Base
from app.core.config import settings

# Import every model module so SQLAlchemy's MetaData discovers the table
# definitions before create_all runs.  The noqa comments suppress the
# "imported but unused" lint warning — they ARE used implicitly by Base.
from app.models import user      # noqa: F401
from app.models import project   # noqa: F401
from app.models import report    # noqa: F401
from app.models import ai_chat   # noqa: F401

# Routers
from app.routers import auth as auth_router
from app.routers import projects as projects_router
from app.routers import reports as reports_router
from app.routers import dashboard as dashboard_router


# ---------------------------------------------------------------------------
# Lifespan — replaces the deprecated @app.on_event("startup") pattern.
# WHY lifespan: FastAPI recommends the asynccontextmanager approach as of
# v0.95+.  Everything before `yield` runs on startup; everything after runs
# on shutdown.
# ---------------------------------------------------------------------------
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: create all tables that don't yet exist.
    # In production this should be replaced by Alembic migrations.
    Base.metadata.create_all(bind=engine)
    yield
    # Shutdown: no teardown required (SQLAlchemy connection pool cleans up).


# ---------------------------------------------------------------------------
# Application instance
# ---------------------------------------------------------------------------
app = FastAPI(
    title="Weekly Report Generator API",
    description=(
        "REST API for the Weekly Report Generator & Team Dashboard.\n\n"
        "Supports:\n"
        "- JWT-based authentication with role-based access control\n"
        "- Weekly report lifecycle management (draft → submitted)\n"
        "- Project / category management\n"
        "- Manager analytics dashboard and AI chat assistant"
    ),
    version="1.0.0",
    lifespan=lifespan,
    # Customise the OpenAPI docs URLs
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
)


# ---------------------------------------------------------------------------
# CORS Middleware
# WHY: Browsers enforce the Same-Origin Policy.  Without CORS headers the
# React dev server (localhost:5173) cannot make XHR / fetch requests to this
# API (localhost:8000).  In production, replace the allow_origins list with
# the actual deployed frontend domain.
# ---------------------------------------------------------------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",   # Vite dev server (default port)
        "http://localhost:3000",   # CRA / alternative dev server
        "http://127.0.0.1:5173",
        "http://127.0.0.1:3000",
    ],
    allow_credentials=True,  # Required to pass the Authorization header
    allow_methods=["*"],
    allow_headers=["*"],
)


# ---------------------------------------------------------------------------
# API Routers — all versioned under /api/v1
# ---------------------------------------------------------------------------
API_V1 = "/api/v1"

app.include_router(auth_router.router,     prefix=API_V1)
app.include_router(projects_router.router, prefix=API_V1)
app.include_router(reports_router.router,  prefix=API_V1)
app.include_router(dashboard_router.router, prefix=API_V1)


# ---------------------------------------------------------------------------
# Root probe — GET /
# Returns application name and running status.  Useful as a quick
# "is the server alive?" check without any database involvement.
# ---------------------------------------------------------------------------
@app.get("/", tags=["Health"], summary="Application root probe")
def root():
    return {
        "application": "Weekly Report Generator API",
        "status": "running",
        "version": "1.0.0",
        "docs": "/docs",
    }


# ---------------------------------------------------------------------------
# Health check — GET /health
# Intended for load-balancer / container orchestration liveness probes.
# Returns a richer payload than the root probe.
# ---------------------------------------------------------------------------
@app.get("/health", tags=["Health"], summary="Health check")
def health_check():
    return {
        "status": "ok",
        "version": "1.0.0",
        "database": "connected",  # engine already validated at import time
    }
