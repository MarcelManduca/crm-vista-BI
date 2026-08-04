"""
Serviço de Auditoria
"""

import logging
from typing import Optional, Dict, Any
from sqlalchemy.orm import Session
from app.models.audit_log import AuditLog

logger = logging.getLogger(__name__)


class AuditService:
    """Serviço para registrar ações de auditoria"""

    def __init__(self, db: Session):
        """
        Inicializa o serviço de auditoria
        
        Args:
            db: Sessão do banco de dados
        """
        self.db = db

    def log_action(
        self,
        user_id: Optional[int],
        action: str,
        resource_type: str,
        resource_id: int,
        details: Optional[Dict[str, Any]] = None,
        ip_address: Optional[str] = None,
        user_agent: Optional[str] = None,
    ) -> AuditLog:
        """
        Registra uma ação de auditoria
        
        Args:
            user_id: ID do usuário que realizou a ação
            action: Tipo de ação (create, read, update, delete)
            resource_type: Tipo de recurso (client, deal, property, etc.)
            resource_id: ID do recurso
            details: Detalhes adicionais em JSON
            ip_address: Endereço IP do cliente
            user_agent: User-Agent do cliente
        
        Returns:
            Log de auditoria criado
        """
        try:
            audit_log = AuditLog(
                user_id=user_id,
                action=action,
                resource_type=resource_type,
                resource_id=resource_id,
                details=details,
                ip_address=ip_address,
                user_agent=user_agent,
            )
            self.db.add(audit_log)
            self.db.commit()
            self.db.refresh(audit_log)
            
            logger.info(
                f"Audit log created: user={user_id} action={action} "
                f"resource={resource_type}:{resource_id}"
            )
            
            return audit_log
        except Exception as e:
            logger.error(f"Error creating audit log: {e}")
            self.db.rollback()
            raise

    def get_logs(
        self,
        user_id: Optional[int] = None,
        resource_type: Optional[str] = None,
        resource_id: Optional[int] = None,
        action: Optional[str] = None,
        skip: int = 0,
        limit: int = 100,
    ) -> list[AuditLog]:
        """
        Obtém logs de auditoria com filtros
        
        Args:
            user_id: Filtrar por ID do usuário
            resource_type: Filtrar por tipo de recurso
            resource_id: Filtrar por ID do recurso
            action: Filtrar por tipo de ação
            skip: Número de registros a pular
            limit: Limite de registros
        
        Returns:
            Lista de logs de auditoria
        """
        query = self.db.query(AuditLog)

        if user_id:
            query = query.filter(AuditLog.user_id == user_id)
        if resource_type:
            query = query.filter(AuditLog.resource_type == resource_type)
        if resource_id:
            query = query.filter(AuditLog.resource_id == resource_id)
        if action:
            query = query.filter(AuditLog.action == action)

        return query.order_by(AuditLog.created_at.desc()).offset(skip).limit(limit).all()

    def get_user_actions(
        self,
        user_id: int,
        skip: int = 0,
        limit: int = 100,
    ) -> list[AuditLog]:
        """
        Obtém todas as ações de um usuário
        
        Args:
            user_id: ID do usuário
            skip: Número de registros a pular
            limit: Limite de registros
        
        Returns:
            Lista de logs de auditoria do usuário
        """
        return self.get_logs(user_id=user_id, skip=skip, limit=limit)

    def get_resource_history(
        self,
        resource_type: str,
        resource_id: int,
    ) -> list[AuditLog]:
        """
        Obtém histórico completo de um recurso
        
        Args:
            resource_type: Tipo de recurso
            resource_id: ID do recurso
        
        Returns:
            Lista de logs de auditoria do recurso
        """
        return self.get_logs(
            resource_type=resource_type,
            resource_id=resource_id,
            limit=1000,
        )
