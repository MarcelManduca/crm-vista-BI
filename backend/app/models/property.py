"""
Modelo de Imóvel
"""

from sqlalchemy import Column, String, Float, Integer, Text, Index
from sqlalchemy.orm import relationship
from app.database import Base
from app.models.base import BaseModel


class Property(Base, BaseModel):
    """Modelo de Imóvel"""

    __tablename__ = "properties"

    # Vista CRM ID (chave de deduplicação)
    vista_property_id = Column(String(255), unique=True, nullable=False, index=True)
    
    # Dados básicos
    address = Column(String(500), nullable=False, index=True)
    city = Column(String(100), nullable=True)
    state = Column(String(2), nullable=True)
    zip_code = Column(String(10), nullable=True)
    
    # Características
    property_type = Column(String(50), nullable=True)  # Apartamento, Casa, Lote, etc.
    area = Column(Float, nullable=True)  # m²
    bedrooms = Column(Integer, nullable=True)
    bathrooms = Column(Integer, nullable=True)
    parking_spaces = Column(Integer, nullable=True)
    
    # Preço
    price = Column(Float, nullable=True)
    
    # Descrição
    description = Column(Text, nullable=True)
    
    # Relacionamentos
    deals = relationship("Deal", back_populates="property", cascade="all, delete-orphan")

    # Índices
    __table_args__ = (
        Index("idx_property_vista_id", "vista_property_id"),
        Index("idx_property_address", "address"),
        Index("idx_property_type", "property_type"),
        Index("idx_property_city", "city"),
    )

    def __repr__(self) -> str:
        return f"<Property id={self.id} address={self.address} vista_id={self.vista_property_id}>"
