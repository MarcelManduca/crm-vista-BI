"""
Serviço de ETL para sincronização de dados
"""

import logging
from typing import Optional, Dict, Any
from datetime import datetime
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from app.models.client import Client
from app.models.property import Property
from app.models.deal import Deal, DealStatus
from app.models.user import User
from app.services.vista_connector import VistaConnector
from app.config import settings

logger = logging.getLogger(__name__)


class ETLService:
    """Serviço de ETL para sincronização com Vista CRM"""

    def __init__(self, db: Session):
        """
        Inicializa o serviço ETL
        
        Args:
            db: Sessão do banco de dados
        """
        self.db = db
        self.connector = VistaConnector()
        self.batch_size = settings.sync_batch_size
        self.retry_attempts = settings.sync_retry_attempts

    async def sync_clients(self) -> Dict[str, Any]:
        """
        Sincroniza clientes da API Vista
        
        Returns:
            Dicionário com estatísticas de sincronização
        """
        logger.info("Starting client synchronization")
        stats = {
            "created": 0,
            "updated": 0,
            "failed": 0,
            "total": 0,
        }

        page = 1
        while True:
            try:
                clients_data = await self.connector.get_clients(
                    page=page,
                    limit=self.batch_size
                )

                if not clients_data:
                    break

                for client_data in clients_data:
                    try:
                        vista_id = client_data.get("id")
                        
                        # Verificar se cliente já existe (idempotência)
                        existing = self.db.query(Client).filter(
                            Client.vista_client_id == vista_id
                        ).first()

                        if existing:
                            # Atualizar cliente existente
                            existing.name = client_data.get("name", existing.name)
                            existing.email = client_data.get("email", existing.email)
                            existing.phone = client_data.get("phone", existing.phone)
                            existing.origin = client_data.get("origin", existing.origin)
                            stats["updated"] += 1
                        else:
                            # Criar novo cliente
                            new_client = Client(
                                vista_client_id=vista_id,
                                name=client_data.get("name", "Unknown"),
                                email=client_data.get("email"),
                                phone=client_data.get("phone"),
                                origin=client_data.get("origin"),
                            )
                            self.db.add(new_client)
                            stats["created"] += 1

                        stats["total"] += 1

                    except IntegrityError:
                        logger.warning(f"Duplicate client: {vista_id}")
                        self.db.rollback()
                        stats["failed"] += 1

                self.db.commit()
                page += 1

            except Exception as e:
                logger.error(f"Error syncing clients: {e}")
                self.db.rollback()
                break

        logger.info(f"Client sync completed: {stats}")
        return stats

    async def sync_properties(self) -> Dict[str, Any]:
        """
        Sincroniza imóveis da API Vista
        
        Returns:
            Dicionário com estatísticas de sincronização
        """
        logger.info("Starting property synchronization")
        stats = {
            "created": 0,
            "updated": 0,
            "failed": 0,
            "total": 0,
        }

        page = 1
        while True:
            try:
                properties_data = await self.connector.get_properties(
                    page=page,
                    limit=self.batch_size
                )

                if not properties_data:
                    break

                for property_data in properties_data:
                    try:
                        vista_id = property_data.get("id")
                        
                        # Verificar se imóvel já existe (idempotência)
                        existing = self.db.query(Property).filter(
                            Property.vista_property_id == vista_id
                        ).first()

                        if existing:
                            # Atualizar imóvel existente
                            existing.address = property_data.get("address", existing.address)
                            existing.property_type = property_data.get("type", existing.property_type)
                            existing.price = property_data.get("price", existing.price)
                            stats["updated"] += 1
                        else:
                            # Criar novo imóvel
                            new_property = Property(
                                vista_property_id=vista_id,
                                address=property_data.get("address", "Unknown"),
                                city=property_data.get("city"),
                                state=property_data.get("state"),
                                property_type=property_data.get("type"),
                                area=property_data.get("area"),
                                bedrooms=property_data.get("bedrooms"),
                                price=property_data.get("price"),
                            )
                            self.db.add(new_property)
                            stats["created"] += 1

                        stats["total"] += 1

                    except IntegrityError:
                        logger.warning(f"Duplicate property: {vista_id}")
                        self.db.rollback()
                        stats["failed"] += 1

                self.db.commit()
                page += 1

            except Exception as e:
                logger.error(f"Error syncing properties: {e}")
                self.db.rollback()
                break

        logger.info(f"Property sync completed: {stats}")
        return stats

    async def sync_deals(self) -> Dict[str, Any]:
        """
        Sincroniza negócios da API Vista
        
        Returns:
            Dicionário com estatísticas de sincronização
        """
        logger.info("Starting deal synchronization")
        stats = {
            "created": 0,
            "updated": 0,
            "failed": 0,
            "total": 0,
        }

        page = 1
        while True:
            try:
                deals_data = await self.connector.get_deals(
                    page=page,
                    limit=self.batch_size
                )

                if not deals_data:
                    break

                for deal_data in deals_data:
                    try:
                        vista_id = deal_data.get("id")
                        
                        # Verificar se negócio já existe (idempotência)
                        existing = self.db.query(Deal).filter(
                            Deal.vista_deal_id == vista_id
                        ).first()

                        # Mapear status
                        status_map = {
                            "lead": DealStatus.LEAD,
                            "negotiation": DealStatus.NEGOTIATION,
                            "proposal": DealStatus.PROPOSAL_SENT,
                            "contract": DealStatus.CONTRACT_SIGNED,
                            "closed": DealStatus.CLOSED,
                            "cancelled": DealStatus.CANCELLED,
                        }
                        status = status_map.get(
                            deal_data.get("status", "").lower(),
                            DealStatus.LEAD
                        )

                        if existing:
                            # Atualizar negócio existente
                            existing.status = status
                            existing.value = deal_data.get("value", existing.value)
                            existing.date_signed = deal_data.get("date_signed", existing.date_signed)
                            stats["updated"] += 1
                        else:
                            # Criar novo negócio
                            new_deal = Deal(
                                vista_deal_id=vista_id,
                                client_id=deal_data.get("client_id"),
                                property_id=deal_data.get("property_id"),
                                user_id=deal_data.get("user_id"),
                                status=status,
                                value=deal_data.get("value"),
                                date_signed=deal_data.get("date_signed"),
                            )
                            self.db.add(new_deal)
                            stats["created"] += 1

                        stats["total"] += 1

                    except IntegrityError:
                        logger.warning(f"Duplicate deal: {vista_id}")
                        self.db.rollback()
                        stats["failed"] += 1

                self.db.commit()
                page += 1

            except Exception as e:
                logger.error(f"Error syncing deals: {e}")
                self.db.rollback()
                break

        logger.info(f"Deal sync completed: {stats}")
        return stats

    async def sync_users(self) -> Dict[str, Any]:
        """
        Sincroniza usuários da API Vista
        
        Returns:
            Dicionário com estatísticas de sincronização
        """
        logger.info("Starting user synchronization")
        stats = {
            "created": 0,
            "updated": 0,
            "failed": 0,
            "total": 0,
        }

        page = 1
        while True:
            try:
                users_data = await self.connector.get_users(
                    page=page,
                    limit=self.batch_size
                )

                if not users_data:
                    break

                for user_data in users_data:
                    try:
                        vista_id = user_data.get("id")
                        
                        # Verificar se usuário já existe (idempotência)
                        existing = self.db.query(User).filter(
                            User.vista_user_id == vista_id
                        ).first()

                        if existing:
                            # Atualizar usuário existente
                            existing.email = user_data.get("email", existing.email)
                            existing.full_name = user_data.get("name", existing.full_name)
                            stats["updated"] += 1
                        else:
                            # Criar novo usuário
                            new_user = User(
                                vista_user_id=vista_id,
                                username=user_data.get("username", f"user_{vista_id}"),
                                email=user_data.get("email", f"user_{vista_id}@gralha.dev"),
                                full_name=user_data.get("name"),
                            )
                            self.db.add(new_user)
                            stats["created"] += 1

                        stats["total"] += 1

                    except IntegrityError:
                        logger.warning(f"Duplicate user: {vista_id}")
                        self.db.rollback()
                        stats["failed"] += 1

                self.db.commit()
                page += 1

            except Exception as e:
                logger.error(f"Error syncing users: {e}")
                self.db.rollback()
                break

        logger.info(f"User sync completed: {stats}")
        return stats

    async def sync_all(self) -> Dict[str, Any]:
        """
        Sincroniza todos os dados
        
        Returns:
            Dicionário com estatísticas de sincronização
        """
        logger.info("Starting full synchronization")
        
        results = {
            "timestamp": datetime.utcnow().isoformat(),
            "clients": await self.sync_clients(),
            "properties": await self.sync_properties(),
            "users": await self.sync_users(),
            "deals": await self.sync_deals(),
        }

        logger.info(f"Full sync completed: {results}")
        return results
