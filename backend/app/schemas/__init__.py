"""
Pydantic Schemas
"""

from app.schemas.base import BaseSchema
from app.schemas.client import ClientCreate, ClientRead, ClientUpdate
from app.schemas.property import PropertyCreate, PropertyRead, PropertyUpdate
from app.schemas.deal import DealCreate, DealRead, DealUpdate, DealStatus
from app.schemas.user import UserCreate, UserRead, UserUpdate, UserRole
from app.schemas.auth import TokenResponse, LoginRequest

__all__ = [
    "BaseSchema",
    "ClientCreate",
    "ClientRead",
    "ClientUpdate",
    "PropertyCreate",
    "PropertyRead",
    "PropertyUpdate",
    "DealCreate",
    "DealRead",
    "DealUpdate",
    "DealStatus",
    "UserCreate",
    "UserRead",
    "UserUpdate",
    "UserRole",
    "TokenResponse",
    "LoginRequest",
]
