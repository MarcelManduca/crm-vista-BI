#!/usr/bin/env python3
"""
Script para inicializar o banco de dados
"""

import sys
import os
from pathlib import Path

# Adicionar diretório pai ao path
sys.path.insert(0, str(Path(__file__).parent.parent))

from app.database import init_db, SessionLocal
from app.models.user import User, UserRole
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def create_default_users():
    """Cria usuários padrão"""
    db = SessionLocal()
    
    try:
        # Verificar se admin já existe
        admin = db.query(User).filter(User.username == "admin").first()
        if admin:
            logger.info("Admin user already exists")
            return
        
        # Criar admin
        admin_user = User(
            vista_user_id="admin_default",
            username="admin",
            email="admin@gralha.dev",
            full_name="Administrator",
            role=UserRole.ADMIN,
            is_active=True,
        )
        admin_user.set_password("admin123")
        db.add(admin_user)
        
        # Criar manager
        manager_user = User(
            vista_user_id="manager_default",
            username="manager",
            email="manager@gralha.dev",
            full_name="Manager",
            role=UserRole.MANAGER,
            is_active=True,
        )
        manager_user.set_password("manager123")
        db.add(manager_user)
        
        # Criar broker
        broker_user = User(
            vista_user_id="broker_default",
            username="broker",
            email="broker@gralha.dev",
            full_name="Broker",
            role=UserRole.BROKER,
            is_active=True,
        )
        broker_user.set_password("broker123")
        db.add(broker_user)
        
        db.commit()
        logger.info("Default users created successfully")
        
    except Exception as e:
        logger.error(f"Error creating default users: {e}")
        db.rollback()
    finally:
        db.close()


def main():
    """Função principal"""
    logger.info("Initializing database...")
    
    try:
        # Inicializar banco de dados
        init_db()
        logger.info("Database initialized successfully")
        
        # Criar usuários padrão
        create_default_users()
        
        logger.info("Database setup completed successfully")
        
    except Exception as e:
        logger.error(f"Error initializing database: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
