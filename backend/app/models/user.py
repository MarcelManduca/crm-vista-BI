"""
Modelo de Usuário (Corretor/Gerente/Admin)
"""

from sqlalchemy import Column, String, Boolean, Index, Enum as SQLEnum
from sqlalchemy.orm import relationship
from app.database import Base
from app.models.base import BaseModel
from enum import Enum
from passlib.context import CryptContext

# Password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class UserRole(str, Enum):
    """Roles disponíveis"""
    ADMIN = "admin"
    MANAGER = "manager"
    BROKER = "broker"
    VIEWER = "viewer"


class User(Base, BaseModel):
    """Modelo de Usuário"""

    __tablename__ = "users"

    # Vista CRM ID (chave de deduplicação)
    vista_user_id = Column(String(255), unique=True, nullable=False, index=True)
    
    # Dados básicos
    username = Column(String(255), unique=True, nullable=False, index=True)
    email = Column(String(255), unique=True, nullable=False, index=True)
    full_name = Column(String(255), nullable=True)
    
    # Autenticação
    hashed_password = Column(String(255), nullable=True)
    is_active = Column(Boolean, default=True, index=True)
    
    # Autorização
    role = Column(SQLEnum(UserRole), nullable=False, default=UserRole.BROKER, index=True)
    
    # Relacionamentos
    deals = relationship("Deal", back_populates="user")

    # Índices
    __table_args__ = (
        Index("idx_user_vista_id", "vista_user_id"),
        Index("idx_user_username", "username"),
        Index("idx_user_email", "email"),
        Index("idx_user_role", "role"),
    )

    def __repr__(self) -> str:
        return f"<User id={self.id} username={self.username} role={self.role}>"

    def verify_password(self, plain_password: str) -> bool:
        """Verifica se a senha está correta"""
        if not self.hashed_password:
            return False
        return pwd_context.verify(plain_password, self.hashed_password)

    def set_password(self, plain_password: str) -> None:
        """Define a senha (hash)"""
        self.hashed_password = pwd_context.hash(plain_password)

    @staticmethod
    def hash_password(plain_password: str) -> str:
        """Hash uma senha"""
        return pwd_context.hash(plain_password)
