"""
Schemas para Usuário
"""

from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from enum import Enum
from app.schemas.base import BaseSchema, BaseReadSchema


class UserRole(str, Enum):
    """Roles disponíveis"""
    ADMIN = "admin"
    MANAGER = "manager"
    BROKER = "broker"
    VIEWER = "viewer"


class UserCreate(BaseSchema):
    """Schema para criar usuário"""

    vista_user_id: str = Field(..., description="ID do usuário no Vista CRM")
    username: str = Field(..., min_length=3, max_length=255, description="Nome de usuário")
    email: EmailStr = Field(..., description="Email do usuário")
    full_name: Optional[str] = Field(None, max_length=255, description="Nome completo")
    password: str = Field(..., min_length=8, description="Senha")
    role: UserRole = Field(default=UserRole.BROKER, description="Role do usuário")


class UserUpdate(BaseSchema):
    """Schema para atualizar usuário"""

    email: Optional[EmailStr] = None
    full_name: Optional[str] = Field(None, max_length=255)
    role: Optional[UserRole] = None
    is_active: Optional[bool] = None


class UserRead(BaseReadSchema):
    """Schema para ler usuário"""

    vista_user_id: str
    username: str
    email: str
    full_name: Optional[str]
    role: UserRole
    is_active: bool
