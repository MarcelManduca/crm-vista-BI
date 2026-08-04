"""
Schemas para Negócio (Deal)
"""

from pydantic import BaseModel, Field
from typing import Optional
from datetime import date
from enum import Enum
from app.schemas.base import BaseSchema, BaseReadSchema


class DealStatus(str, Enum):
    """Status possíveis de um negócio"""
    LEAD = "Lead"
    NEGOTIATION = "Em Negociação"
    PROPOSAL_SENT = "Proposta Enviada"
    CONTRACT_SIGNED = "Contrato Assinado"
    CLOSED = "Fechado"
    CANCELLED = "Cancelado"


class DealCreate(BaseSchema):
    """Schema para criar negócio"""

    vista_deal_id: str = Field(..., description="ID do negócio no Vista CRM")
    client_id: int = Field(..., description="ID do cliente")
    property_id: Optional[int] = Field(None, description="ID do imóvel")
    user_id: int = Field(..., description="ID do corretor/usuário")
    status: DealStatus = Field(default=DealStatus.LEAD, description="Status do negócio")
    value: Optional[float] = Field(None, ge=0, description="Valor do negócio")
    commission_value: Optional[float] = Field(None, ge=0, description="Valor da comissão")
    commission_percentage: Optional[float] = Field(None, ge=0, le=100, description="Percentual da comissão")
    date_signed: Optional[date] = Field(None, description="Data de assinatura do contrato")
    date_closed: Optional[date] = Field(None, description="Data de fechamento")
    notes: Optional[str] = Field(None, description="Notas sobre o negócio")


class DealUpdate(BaseSchema):
    """Schema para atualizar negócio"""

    status: Optional[DealStatus] = None
    value: Optional[float] = Field(None, ge=0)
    commission_value: Optional[float] = Field(None, ge=0)
    commission_percentage: Optional[float] = Field(None, ge=0, le=100)
    date_signed: Optional[date] = None
    date_closed: Optional[date] = None
    notes: Optional[str] = None


class DealRead(BaseReadSchema):
    """Schema para ler negócio"""

    vista_deal_id: str
    client_id: int
    property_id: Optional[int]
    user_id: int
    status: DealStatus
    value: Optional[float]
    commission_value: Optional[float]
    commission_percentage: Optional[float]
    date_signed: Optional[date]
    date_closed: Optional[date]
    notes: Optional[str]
