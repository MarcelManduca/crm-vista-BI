"""
API Endpoints
"""

from fastapi import APIRouter
from app.api.endpoints import auth, deals, clients, properties, users

router = APIRouter(prefix="/api", tags=["API"])

# Incluir rotas
router.include_router(auth.router, prefix="/auth", tags=["Authentication"])
router.include_router(deals.router, prefix="/deals", tags=["Deals"])
router.include_router(clients.router, prefix="/clients", tags=["Clients"])
router.include_router(properties.router, prefix="/properties", tags=["Properties"])
router.include_router(users.router, prefix="/users", tags=["Users"])

__all__ = ["router"]
