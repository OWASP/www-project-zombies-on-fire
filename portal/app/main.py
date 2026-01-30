"""
Main FastAPI application entry point.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse

from app.config import settings
from app.database import init_db
from app.api import api_router

# Create FastAPI application
app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="""
    OWASP Zombies on Fire - Tabletop Exercise Generation Portal

    An AI-powered platform for creating and managing tabletop cybersecurity exercises.

    ## Features

    - **Admin Authentication**: Secure login system for administrators
    - **Tabletop Creation**: 4-question guided creation flow
    - **AI Document Generation**: Specialized agents for each document type
    - **PDF Export**: Professional PDF output for all materials

    ## Document Types

    Each document type has its own specialized AI agent:

    - **Scenario Brief**: Main scenario overview
    - **Facilitator Guide**: Exercise leader instructions
    - **Participant Handbook**: Player materials
    - **Inject Cards**: Surprise events
    - **Assessment Rubric**: Evaluation criteria
    - **After Action Template**: Debrief materials
    """,
    docs_url="/api/docs",
    redoc_url="/api/redoc",
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API routes
app.include_router(api_router, prefix="/api")

# Mount static files
try:
    app.mount("/static", StaticFiles(directory="app/static"), name="static")
except RuntimeError:
    pass  # Static directory doesn't exist yet


@app.on_event("startup")
async def startup_event():
    """Initialize database on startup."""
    init_db()


@app.get("/", response_class=HTMLResponse)
async def root():
    """Serve the main application page."""
    return """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Zombies on Fire - Tabletop Portal</title>
        <meta http-equiv="refresh" content="0; url=/app">
    </head>
    <body>
        <p>Redirecting to application...</p>
    </body>
    </html>
    """


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "app": settings.APP_NAME,
        "version": settings.APP_VERSION,
    }


# Import and mount the frontend application
from app.frontend import frontend_router
app.include_router(frontend_router)
