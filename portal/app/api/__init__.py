"""
API routes package.
"""

from fastapi import APIRouter

from app.api import auth, users, tabletops, documents

api_router = APIRouter()

api_router.include_router(auth.router, prefix="/auth", tags=["Authentication"])
api_router.include_router(users.router, prefix="/users", tags=["Users"])
api_router.include_router(tabletops.router, prefix="/tabletops", tags=["Tabletops"])
api_router.include_router(documents.router, prefix="/documents", tags=["Documents"])
