"""
Endpoints de Clientes
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.client import Client
from app.models.user import User
from app.auth.security import get_current_active_user
from app.schemas.client import ClientRead, ClientCreate, ClientUpdate

router = APIRouter()


@router.get("", response_model=list[ClientRead])
async def list_clients(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
) -> list[ClientRead]:
    """Lista clientes com paginação"""
    clients = db.query(Client).filter(
        Client.deleted_at.is_(None)
    ).offset(skip).limit(limit).all()
    return clients


@router.get("/{client_id}", response_model=ClientRead)
async def get_client(
    client_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
) -> ClientRead:
    """Obtém um cliente por ID"""
    client = db.query(Client).filter(Client.id == client_id).first()
    if not client:
        raise HTTPException(status_code=404, detail="Client not found")
    return client


@router.post("", response_model=ClientRead)
async def create_client(
    client: ClientCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
) -> ClientRead:
    """Cria um novo cliente"""
    # Verificar duplicação por vista_client_id
    existing = db.query(Client).filter(
        Client.vista_client_id == client.vista_client_id
    ).first()
    
    if existing:
        raise HTTPException(
            status_code=400,
            detail="Client with this Vista ID already exists"
        )
    
    db_client = Client(**client.dict())
    db.add(db_client)
    db.commit()
    db.refresh(db_client)
    return db_client


@router.put("/{client_id}", response_model=ClientRead)
async def update_client(
    client_id: int,
    client_update: ClientUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
) -> ClientRead:
    """Atualiza um cliente"""
    db_client = db.query(Client).filter(Client.id == client_id).first()
    if not db_client:
        raise HTTPException(status_code=404, detail="Client not found")
    
    for key, value in client_update.dict(exclude_unset=True).items():
        setattr(db_client, key, value)
    
    db.commit()
    db.refresh(db_client)
    return db_client


@router.delete("/{client_id}")
async def delete_client(
    client_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    """Deleta um cliente (soft delete)"""
    db_client = db.query(Client).filter(Client.id == client_id).first()
    if not db_client:
        raise HTTPException(status_code=404, detail="Client not found")
    
    from datetime import datetime
    db_client.deleted_at = datetime.utcnow()
    db.commit()
    
    return {"message": "Client deleted"}
