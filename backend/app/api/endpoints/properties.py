"""
Endpoints de Imóveis
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.property import Property
from app.models.user import User
from app.auth.security import get_current_active_user
from app.schemas.property import PropertyRead, PropertyCreate, PropertyUpdate

router = APIRouter()


@router.get("", response_model=list[PropertyRead])
async def list_properties(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
) -> list[PropertyRead]:
    """Lista imóveis com paginação"""
    properties = db.query(Property).filter(
        Property.deleted_at.is_(None)
    ).offset(skip).limit(limit).all()
    return properties


@router.get("/{property_id}", response_model=PropertyRead)
async def get_property(
    property_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
) -> PropertyRead:
    """Obtém um imóvel por ID"""
    property_obj = db.query(Property).filter(Property.id == property_id).first()
    if not property_obj:
        raise HTTPException(status_code=404, detail="Property not found")
    return property_obj


@router.post("", response_model=PropertyRead)
async def create_property(
    property_obj: PropertyCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
) -> PropertyRead:
    """Cria um novo imóvel"""
    # Verificar duplicação por vista_property_id
    existing = db.query(Property).filter(
        Property.vista_property_id == property_obj.vista_property_id
    ).first()
    
    if existing:
        raise HTTPException(
            status_code=400,
            detail="Property with this Vista ID already exists"
        )
    
    db_property = Property(**property_obj.dict())
    db.add(db_property)
    db.commit()
    db.refresh(db_property)
    return db_property


@router.put("/{property_id}", response_model=PropertyRead)
async def update_property(
    property_id: int,
    property_update: PropertyUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
) -> PropertyRead:
    """Atualiza um imóvel"""
    db_property = db.query(Property).filter(Property.id == property_id).first()
    if not db_property:
        raise HTTPException(status_code=404, detail="Property not found")
    
    for key, value in property_update.dict(exclude_unset=True).items():
        setattr(db_property, key, value)
    
    db.commit()
    db.refresh(db_property)
    return db_property


@router.delete("/{property_id}")
async def delete_property(
    property_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    """Deleta um imóvel (soft delete)"""
    db_property = db.query(Property).filter(Property.id == property_id).first()
    if not db_property:
        raise HTTPException(status_code=404, detail="Property not found")
    
    from datetime import datetime
    db_property.deleted_at = datetime.utcnow()
    db.commit()
    
    return {"message": "Property deleted"}
