"""
Schemas para Autenticação
"""

from pydantic import BaseModel, EmailStr, Field
from typing import Optional


class LoginRequest(BaseModel):
    """Schema para login"""

    username: str = Field(..., description="Nome de usuário ou email")
    password: str = Field(..., description="Senha")


class TokenResponse(BaseModel):
    """Schema para resposta de token"""

    access_token: str = Field(..., description="Token JWT")
    token_type: str = Field(default="bearer", description="Tipo de token")
    expires_in: int = Field(..., description="Tempo de expiração em segundos")
