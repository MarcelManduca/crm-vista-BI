"""
Modelo de Cliente
"""

from sqlalchemy import Column, String, Text, Index
from sqlalchemy.orm import relationship
from app.database import Base
from app.models.base import BaseModel


class Client(Base, BaseModel):
    """Modelo de Cliente (Leads)"""

    __tablename__ = "clients"

    # Vista CRM ID (chave de deduplicação)
    vista_client_id = Column(String(255), unique=True, nullable=False, index=True)
    
    # Dados básicos
    name = Column(String(255), nullable=False, index=True)
    email = Column(String(255), nullable=True, index=True)
    phone = Column(String(20), nullable=True)
    
    # Origem de captação (primeiro toque)
    origin = Column(String(100), nullable=True)
    
    # Origem de captação (último toque)
    last_origin = Column(String(100), nullable=True)
    
    # Dados adicionais
    notes = Column(Text, nullable=True)
    
    # Relacionamentos
    deals = relationship("Deal", back_populates="client", cascade="all, delete-orphan")

    # Índices
    __table_args__ = (
        Index("idx_client_vista_id", "vista_client_id"),
        Index("idx_client_name", "name"),
        Index("idx_client_email", "email"),
        Index("idx_client_origin", "origin"),
    )

    def __repr__(self) -> str:
        return f"<Client id={self.id} name={self.name} vista_id={self.vista_client_id}>"
