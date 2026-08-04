"""
Modelo de Negócio (Deal)
"""

from sqlalchemy import Column, String, Float, Date, Integer, ForeignKey, Text, Index, Enum as SQLEnum
from sqlalchemy.orm import relationship
from app.database import Base
from app.models.base import BaseModel
from enum import Enum
from datetime import date


class DealStatus(str, Enum):
    """Status possíveis de um negócio"""
    LEAD = "Lead"
    NEGOTIATION = "Em Negociação"
    PROPOSAL_SENT = "Proposta Enviada"
    CONTRACT_SIGNED = "Contrato Assinado"
    CLOSED = "Fechado"
    CANCELLED = "Cancelado"


class Deal(Base, BaseModel):
    """Modelo de Negócio (Deal)"""

    __tablename__ = "deals"

    # Vista CRM ID (chave de deduplicação)
    vista_deal_id = Column(String(255), unique=True, nullable=False, index=True)
    
    # Relacionamentos
    client_id = Column(Integer, ForeignKey("clients.id"), nullable=False, index=True)
    property_id = Column(Integer, ForeignKey("properties.id"), nullable=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    
    # Status do negócio
    status = Column(SQLEnum(DealStatus), nullable=False, index=True, default=DealStatus.LEAD)
    
    # Valores
    value = Column(Float, nullable=True)  # Valor do negócio
    commission_value = Column(Float, nullable=True)  # Valor da comissão
    commission_percentage = Column(Float, nullable=True)  # Percentual da comissão
    
    # Datas
    date_signed = Column(Date, nullable=True, index=True)  # Data de assinatura do contrato
    date_closed = Column(Date, nullable=True, index=True)  # Data de fechamento
    
    # Notas
    notes = Column(Text, nullable=True)
    
    # Relacionamentos
    client = relationship("Client", back_populates="deals")
    property = relationship("Property", back_populates="deals")
    user = relationship("User", back_populates="deals")
    history = relationship("DealHistory", back_populates="deal", cascade="all, delete-orphan")

    # Índices
    __table_args__ = (
        Index("idx_deal_vista_id", "vista_deal_id"),
        Index("idx_deal_status", "status"),
        Index("idx_deal_date_signed", "date_signed"),
        Index("idx_deal_client_id", "client_id"),
        Index("idx_deal_property_id", "property_id"),
        Index("idx_deal_user_id", "user_id"),
    )

    def __repr__(self) -> str:
        return f"<Deal id={self.id} status={self.status} value={self.value} vista_id={self.vista_deal_id}>"


class DealHistory(Base, BaseModel):
    """Histórico de mudanças de status de um negócio"""

    __tablename__ = "deal_history"

    # Relacionamento
    deal_id = Column(Integer, ForeignKey("deals.id"), nullable=False, index=True)
    
    # Status anterior e novo
    status_from = Column(SQLEnum(DealStatus), nullable=True)
    status_to = Column(SQLEnum(DealStatus), nullable=False)
    
    # Quem mudou
    changed_by = Column(Integer, ForeignKey("users.id"), nullable=True)
    
    # Notas da mudança
    notes = Column(Text, nullable=True)

    # Relacionamentos
    deal = relationship("Deal", back_populates="history")
    user = relationship("User")

    # Índices
    __table_args__ = (
        Index("idx_deal_history_deal_id", "deal_id"),
        Index("idx_deal_history_status_to", "status_to"),
    )

    def __repr__(self) -> str:
        return f"<DealHistory id={self.id} deal_id={self.deal_id} {self.status_from} -> {self.status_to}>"
