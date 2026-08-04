"""
Schemas para Imóvel
"""

from pydantic import BaseModel, Field
from typing import Optional
from app.schemas.base import BaseSchema, BaseReadSchema


class PropertyCreate(BaseSchema):
    """Schema para criar imóvel"""

    vista_property_id: str = Field(..., description="ID do imóvel no Vista CRM")
    address: str = Field(..., min_length=1, max_length=500, description="Endereço do imóvel")
    city: Optional[str] = Field(None, max_length=100, description="Cidade")
    state: Optional[str] = Field(None, max_length=2, description="Estado (UF)")
    zip_code: Optional[str] = Field(None, max_length=10, description="CEP")
    property_type: Optional[str] = Field(None, max_length=50, description="Tipo de imóvel")
    area: Optional[float] = Field(None, ge=0, description="Área em m²")
    bedrooms: Optional[int] = Field(None, ge=0, description="Número de quartos")
    bathrooms: Optional[int] = Field(None, ge=0, description="Número de banheiros")
    parking_spaces: Optional[int] = Field(None, ge=0, description="Número de vagas")
    price: Optional[float] = Field(None, ge=0, description="Preço do imóvel")
    description: Optional[str] = Field(None, description="Descrição do imóvel")


class PropertyUpdate(BaseSchema):
    """Schema para atualizar imóvel"""

    address: Optional[str] = Field(None, min_length=1, max_length=500)
    city: Optional[str] = Field(None, max_length=100)
    state: Optional[str] = Field(None, max_length=2)
    zip_code: Optional[str] = Field(None, max_length=10)
    property_type: Optional[str] = Field(None, max_length=50)
    area: Optional[float] = Field(None, ge=0)
    bedrooms: Optional[int] = Field(None, ge=0)
    bathrooms: Optional[int] = Field(None, ge=0)
    parking_spaces: Optional[int] = Field(None, ge=0)
    price: Optional[float] = Field(None, ge=0)
    description: Optional[str] = None


class PropertyRead(BaseReadSchema):
    """Schema para ler imóvel"""

    vista_property_id: str
    address: str
    city: Optional[str]
    state: Optional[str]
    zip_code: Optional[str]
    property_type: Optional[str]
    area: Optional[float]
    bedrooms: Optional[int]
    bathrooms: Optional[int]
    parking_spaces: Optional[int]
    price: Optional[float]
    description: Optional[str]
