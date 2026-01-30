"""
Frontend routes for the admin interface.
"""

from fastapi import APIRouter, Request, Depends, Form, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from pathlib import Path

templates = Jinja2Templates(directory=Path(__file__).parent / "templates")

frontend_router = APIRouter()


@frontend_router.get("/app", response_class=HTMLResponse)
async def app_home(request: Request):
    """Main application page."""
    return templates.TemplateResponse("index.html", {"request": request})


@frontend_router.get("/app/login", response_class=HTMLResponse)
async def login_page(request: Request):
    """Login page."""
    return templates.TemplateResponse("login.html", {"request": request})


@frontend_router.get("/app/register", response_class=HTMLResponse)
async def register_page(request: Request):
    """Registration page."""
    return templates.TemplateResponse("register.html", {"request": request})


@frontend_router.get("/app/dashboard", response_class=HTMLResponse)
async def dashboard_page(request: Request):
    """Dashboard page."""
    return templates.TemplateResponse("dashboard.html", {"request": request})


@frontend_router.get("/app/tabletop/new", response_class=HTMLResponse)
async def new_tabletop_page(request: Request):
    """Create new tabletop page."""
    return templates.TemplateResponse("tabletop_create.html", {"request": request})


@frontend_router.get("/app/tabletop/{tabletop_id}", response_class=HTMLResponse)
async def tabletop_detail_page(request: Request, tabletop_id: int):
    """Tabletop detail page."""
    return templates.TemplateResponse(
        "tabletop_detail.html",
        {"request": request, "tabletop_id": tabletop_id}
    )


@frontend_router.get("/app/tabletop/{tabletop_id}/questions", response_class=HTMLResponse)
async def tabletop_questions_page(request: Request, tabletop_id: int):
    """Tabletop questions page."""
    return templates.TemplateResponse(
        "tabletop_questions.html",
        {"request": request, "tabletop_id": tabletop_id}
    )


@frontend_router.get("/app/tabletop/{tabletop_id}/documents", response_class=HTMLResponse)
async def tabletop_documents_page(request: Request, tabletop_id: int):
    """Tabletop documents page."""
    return templates.TemplateResponse(
        "tabletop_documents.html",
        {"request": request, "tabletop_id": tabletop_id}
    )
