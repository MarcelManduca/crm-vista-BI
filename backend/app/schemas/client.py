"""
Schemas para Cliente
"""

from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from app.schemas.base import BaseSchema, BaseReadSchema


class ClientCreate(BaseSchema):
    """Schema para criar cliente"""

    vista_client_id: str = Field(..., description="ID do cliente no Vista CRM")
    name: str = Field(..., min_length=1, max_length=255, description="Nome do cliente")
    email: Optional[EmailStr] = Field(None, description="Email do cliente")
    phone: Optional[str] = Field(None, max_length=20, description="Telefone do cliente")
    origin: Optional[str] = Field(None, max_length=100, description="Origem de captação (primeiro toque)")
    last_origin: Optional[str] = Field(None, max_length=100, description="Origem de captação (último toque)")
    notes: Optional[str] = Field(None, description="Notas sobre o cliente")


class ClientUpdate(BaseSchema):
    """Schema para atualizar cliente"""

    name: Optional[str] = Field(None, min_length=1, max_length=255)
    email: Optional[EmailStr] = None
    phone: Optional[str] = Field(None, max_length=20)
    origin: Optional[str] = Field(None, max_length=100)
    last_origin: Optional[str] = Field(None, max_length=100)
    notes: Optional[str] = None


class ClientRead(BaseReadSchema):
    """Schema para ler cliente"""

    vista_client_id: str
    name: str
    email: Optional[str]
    phone: Optional[str]
    origin: Optional[str]
    last_origin: Optional[str]
    notes: Optional[str]
