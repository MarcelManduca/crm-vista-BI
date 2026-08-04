"""
Modelo de Log de Auditoria
"""

from sqlalchemy import Column, String, Integer, Text, Index, JSON
from app.database import Base
from app.models.base import BaseModel


class AuditLog(Base, BaseModel):
    """Modelo de Log de Auditoria"""

    __tablename__ = "audit_logs"

    # Quem fez a ação
    user_id = Column(Integer, nullable=True, index=True)
    
    # O que foi feito
    action = Column(String(50), nullable=False, index=True)  # create, read, update, delete
    
    # Em qual recurso
    resource_type = Column(String(50), nullable=False, index=True)  # client, deal, property, etc.
    resource_id = Column(Integer, nullable=False, index=True)
    
    # Detalhes
    details = Column(JSON, nullable=True)  # Dados adicionais da ação
    
    # IP e User Agent (opcional)
    ip_address = Column(String(45), nullable=True)
    user_agent = Column(String(500), nullable=True)

    # Índices
    __table_args__ = (
        Index("idx_audit_user_id", "user_id"),
        Index("idx_audit_action", "action"),
        Index("idx_audit_resource", "resource_type", "resource_id"),
        Index("idx_audit_timestamp", "created_at"),
    )

    def __repr__(self) -> str:
        return f"<AuditLog id={self.id} user_id={self.user_id} action={self.action} resource={self.resource_type}:{self.resource_id}>"
