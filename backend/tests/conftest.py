"""
Configuração de testes com pytest
"""

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from app.database import Base, get_db
from app.main import app
from app.config import settings

# Usar banco de dados em memória para testes
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture(scope="function")
def db():
    """Fixture para sessão de banco de dados"""
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
        Base.metadata.drop_all(bind=engine)


@pytest.fixture(scope="function")
def client(db: Session):
    """Fixture para cliente de teste"""
    def override_get_db():
        try:
            yield db
        finally:
            db.close()

    app.dependency_overrides[get_db] = override_get_db
    
    with TestClient(app) as test_client:
        yield test_client
    
    app.dependency_overrides.clear()


@pytest.fixture(scope="function")
def test_user_data():
    """Fixture com dados de usuário de teste"""
    return {
        "vista_user_id": "test_user_1",
        "username": "testuser",
        "email": "test@example.com",
        "full_name": "Test User",
        "password": "testpassword123",
        "role": "broker",
    }


@pytest.fixture(scope="function")
def test_client_data():
    """Fixture com dados de cliente de teste"""
    return {
        "vista_client_id": "test_client_1",
        "name": "Test Client",
        "email": "client@example.com",
        "phone": "11999999999",
        "origin": "Google Ads",
    }


@pytest.fixture(scope="function")
def test_property_data():
    """Fixture com dados de imóvel de teste"""
    return {
        "vista_property_id": "test_property_1",
        "address": "Rua Teste, 123",
        "city": "São Paulo",
        "state": "SP",
        "property_type": "Apartamento",
        "area": 100.0,
        "bedrooms": 2,
        "bathrooms": 1,
        "price": 500000.0,
    }


@pytest.fixture(scope="function")
def test_deal_data():
    """Fixture com dados de negócio de teste"""
    return {
        "vista_deal_id": "test_deal_1",
        "client_id": 1,
        "property_id": 1,
        "user_id": 1,
        "status": "Lead",
        "value": 500000.0,
    }
