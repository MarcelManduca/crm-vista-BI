"""
Testes de Autenticação
"""

import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from app.models.user import User
from app.auth.security import create_access_token, verify_token


def test_create_access_token():
    """Testa criação de JWT token"""
    data = {"sub": 1}
    token = create_access_token(data)
    
    assert token is not None
    assert isinstance(token, str)


def test_verify_token():
    """Testa verificação de JWT token"""
    data = {"sub": 1}
    token = create_access_token(data)
    
    payload = verify_token(token)
    assert payload["sub"] == 1


def test_verify_invalid_token():
    """Testa verificação de token inválido"""
    with pytest.raises(Exception):
        verify_token("invalid_token")


def test_login_success(client: TestClient, db: Session, test_user_data: dict):
    """Testa login com sucesso"""
    # Criar usuário
    user = User(**test_user_data)
    user.set_password(test_user_data["password"])
    db.add(user)
    db.commit()
    
    # Fazer login
    response = client.post(
        "/api/auth/login",
        json={
            "username": test_user_data["username"],
            "password": test_user_data["password"],
        }
    )
    
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"


def test_login_invalid_credentials(client: TestClient):
    """Testa login com credenciais inválidas"""
    response = client.post(
        "/api/auth/login",
        json={
            "username": "nonexistent",
            "password": "wrongpassword",
        }
    )
    
    assert response.status_code == 401
