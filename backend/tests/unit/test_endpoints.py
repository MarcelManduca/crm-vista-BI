"""
Testes de Endpoints
"""

import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from app.models.client import Client
from app.models.user import User


def test_health_check(client: TestClient):
    """Testa endpoint de health check"""
    response = client.get("/health")
    
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"


def test_root_endpoint(client: TestClient):
    """Testa endpoint raiz"""
    response = client.get("/")
    
    assert response.status_code == 200
    data = response.json()
    assert "message" in data


def test_list_clients_unauthorized(client: TestClient):
    """Testa listagem de clientes sem autenticação"""
    response = client.get("/api/clients")
    
    assert response.status_code == 403


def test_list_clients_authorized(client: TestClient, db: Session, test_user_data: dict, test_client_data: dict):
    """Testa listagem de clientes com autenticação"""
    # Criar usuário
    user = User(**test_user_data)
    user.set_password(test_user_data["password"])
    db.add(user)
    db.commit()
    
    # Fazer login
    login_response = client.post(
        "/api/auth/login",
        json={
            "username": test_user_data["username"],
            "password": test_user_data["password"],
        }
    )
    token = login_response.json()["access_token"]
    
    # Criar cliente
    client_obj = Client(**test_client_data)
    db.add(client_obj)
    db.commit()
    
    # Listar clientes
    response = client.get(
        "/api/clients",
        headers={"Authorization": f"Bearer {token}"}
    )
    
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)


def test_create_client(client: TestClient, db: Session, test_user_data: dict, test_client_data: dict):
    """Testa criação de cliente"""
    # Criar usuário
    user = User(**test_user_data)
    user.set_password(test_user_data["password"])
    db.add(user)
    db.commit()
    
    # Fazer login
    login_response = client.post(
        "/api/auth/login",
        json={
            "username": test_user_data["username"],
            "password": test_user_data["password"],
        }
    )
    token = login_response.json()["access_token"]
    
    # Criar cliente
    response = client.post(
        "/api/clients",
        json=test_client_data,
        headers={"Authorization": f"Bearer {token}"}
    )
    
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == test_client_data["name"]


def test_get_client(client: TestClient, db: Session, test_user_data: dict, test_client_data: dict):
    """Testa obtenção de cliente"""
    # Criar usuário
    user = User(**test_user_data)
    user.set_password(test_user_data["password"])
    db.add(user)
    db.commit()
    
    # Fazer login
    login_response = client.post(
        "/api/auth/login",
        json={
            "username": test_user_data["username"],
            "password": test_user_data["password"],
        }
    )
    token = login_response.json()["access_token"]
    
    # Criar cliente
    client_obj = Client(**test_client_data)
    db.add(client_obj)
    db.commit()
    
    # Obter cliente
    response = client.get(
        f"/api/clients/{client_obj.id}",
        headers={"Authorization": f"Bearer {token}"}
    )
    
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == client_obj.id
