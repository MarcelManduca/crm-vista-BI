"""
Testes de Modelos
"""

import pytest
from sqlalchemy.orm import Session
from app.models.client import Client
from app.models.property import Property
from app.models.deal import Deal, DealStatus
from app.models.user import User


def test_create_client(db: Session, test_client_data: dict):
    """Testa criação de cliente"""
    client = Client(**test_client_data)
    db.add(client)
    db.commit()
    
    assert client.id is not None
    assert client.vista_client_id == test_client_data["vista_client_id"]
    assert client.name == test_client_data["name"]


def test_create_property(db: Session, test_property_data: dict):
    """Testa criação de imóvel"""
    property_obj = Property(**test_property_data)
    db.add(property_obj)
    db.commit()
    
    assert property_obj.id is not None
    assert property_obj.vista_property_id == test_property_data["vista_property_id"]
    assert property_obj.address == test_property_data["address"]


def test_create_user(db: Session, test_user_data: dict):
    """Testa criação de usuário"""
    user = User(**test_user_data)
    user.set_password(test_user_data["password"])
    db.add(user)
    db.commit()
    
    assert user.id is not None
    assert user.username == test_user_data["username"]
    assert user.hashed_password is not None


def test_verify_password(db: Session, test_user_data: dict):
    """Testa verificação de senha"""
    user = User(**test_user_data)
    user.set_password(test_user_data["password"])
    
    assert user.verify_password(test_user_data["password"])
    assert not user.verify_password("wrongpassword")


def test_create_deal(db: Session, test_deal_data: dict, test_client_data: dict, test_user_data: dict):
    """Testa criação de negócio"""
    # Criar cliente e usuário
    client = Client(**test_client_data)
    user = User(**test_user_data)
    user.set_password(test_user_data["password"])
    
    db.add(client)
    db.add(user)
    db.commit()
    
    # Criar negócio
    deal_data = test_deal_data.copy()
    deal_data["client_id"] = client.id
    deal_data["user_id"] = user.id
    
    deal = Deal(**deal_data)
    db.add(deal)
    db.commit()
    
    assert deal.id is not None
    assert deal.status == DealStatus.LEAD
    assert deal.value == test_deal_data["value"]


def test_soft_delete(db: Session, test_client_data: dict):
    """Testa soft delete"""
    from datetime import datetime
    
    client = Client(**test_client_data)
    db.add(client)
    db.commit()
    
    client_id = client.id
    
    # Soft delete
    client.deleted_at = datetime.utcnow()
    db.commit()
    
    # Verificar que o cliente ainda existe no banco
    deleted_client = db.query(Client).filter(Client.id == client_id).first()
    assert deleted_client is not None
    assert deleted_client.deleted_at is not None
