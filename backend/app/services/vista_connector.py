"""
Connector para API Vista CRM (Loft)
"""

import httpx
import logging
from typing import Optional, Dict, List, Any
from app.config import settings

logger = logging.getLogger(__name__)


class VistaConnector:
    """Connector para integração com API Vista CRM"""

    def __init__(self):
        """Inicializa o connector"""
        self.base_url = settings.vista_api_base_url
        self.api_key = settings.vista_api_key
        self.tenant_id = settings.vista_tenant_id
        self.timeout = 30

    def _get_headers(self) -> Dict[str, str]:
        """Retorna headers padrão para requisições"""
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}",
        }
        if self.tenant_id:
            headers["X-Tenant-ID"] = self.tenant_id
        return headers

    async def _request(
        self,
        method: str,
        endpoint: str,
        **kwargs
    ) -> Optional[Dict[str, Any]]:
        """
        Realiza requisição HTTP à API Vista
        
        Args:
            method: Método HTTP (GET, POST, etc.)
            endpoint: Endpoint da API (ex: /clientes/listar)
            **kwargs: Argumentos adicionais para httpx
        
        Returns:
            Resposta JSON ou None se falhar
        """
        url = f"{self.base_url}{endpoint}"
        headers = self._get_headers()

        try:
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                response = await client.request(
                    method,
                    url,
                    headers=headers,
                    **kwargs
                )
                response.raise_for_status()
                return response.json()
        except httpx.HTTPError as e:
            logger.error(f"HTTP error calling Vista API: {e}")
            return None
        except Exception as e:
            logger.error(f"Error calling Vista API: {e}")
            return None

    async def get_clients(
        self,
        page: int = 1,
        limit: int = 100,
        filters: Optional[Dict] = None
    ) -> Optional[List[Dict]]:
        """
        Obtém lista de clientes
        
        Args:
            page: Número da página
            limit: Limite de registros por página
            filters: Filtros adicionais
        
        Returns:
            Lista de clientes ou None
        """
        params = {
            "page": page,
            "limit": limit,
        }
        if filters:
            params.update(filters)

        result = await self._request("GET", "/clientes/listar", params=params)
        
        if result and "data" in result:
            return result["data"]
        return None

    async def get_client_fields(self) -> Optional[Dict]:
        """Obtém schema de campos de cliente"""
        return await self._request("GET", "/clientes/listarcampos")

    async def get_properties(
        self,
        page: int = 1,
        limit: int = 100,
        filters: Optional[Dict] = None
    ) -> Optional[List[Dict]]:
        """
        Obtém lista de imóveis
        
        Args:
            page: Número da página
            limit: Limite de registros por página
            filters: Filtros adicionais
        
        Returns:
            Lista de imóveis ou None
        """
        params = {
            "page": page,
            "limit": limit,
        }
        if filters:
            params.update(filters)

        result = await self._request("GET", "/imoveis/listar", params=params)
        
        if result and "data" in result:
            return result["data"]
        return None

    async def get_property_fields(self) -> Optional[Dict]:
        """Obtém schema de campos de imóvel"""
        return await self._request("GET", "/imoveis/listarcampos")

    async def get_deals(
        self,
        page: int = 1,
        limit: int = 100,
        filters: Optional[Dict] = None
    ) -> Optional[List[Dict]]:
        """
        Obtém lista de negócios
        
        Args:
            page: Número da página
            limit: Limite de registros por página
            filters: Filtros adicionais
        
        Returns:
            Lista de negócios ou None
        """
        params = {
            "page": page,
            "limit": limit,
        }
        if filters:
            params.update(filters)

        result = await self._request("GET", "/negocios/listar", params=params)
        
        if result and "data" in result:
            return result["data"]
        return None

    async def get_deal_fields(self) -> Optional[Dict]:
        """Obtém schema de campos de negócio"""
        return await self._request("GET", "/negocios/listarcampos")

    async def get_users(
        self,
        page: int = 1,
        limit: int = 100
    ) -> Optional[List[Dict]]:
        """
        Obtém lista de usuários
        
        Args:
            page: Número da página
            limit: Limite de registros por página
        
        Returns:
            Lista de usuários ou None
        """
        params = {
            "page": page,
            "limit": limit,
        }

        result = await self._request("GET", "/usuarios/listar", params=params)
        
        if result and "data" in result:
            return result["data"]
        return None

    async def get_user_fields(self) -> Optional[Dict]:
        """Obtém schema de campos de usuário"""
        return await self._request("GET", "/usuarios/listarcampos")

    async def get_history(
        self,
        resource_type: str,
        resource_id: int,
        page: int = 1,
        limit: int = 100
    ) -> Optional[List[Dict]]:
        """
        Obtém histórico de um recurso
        
        Args:
            resource_type: Tipo de recurso (cliente, negócio, etc.)
            resource_id: ID do recurso
            page: Número da página
            limit: Limite de registros por página
        
        Returns:
            Lista de históricos ou None
        """
        params = {
            "page": page,
            "limit": limit,
        }

        result = await self._request(
            "GET",
            f"/historico/listar?resource_type={resource_type}&resource_id={resource_id}",
            params=params
        )
        
        if result and "data" in result:
            return result["data"]
        return None

    async def health_check(self) -> bool:
        """Verifica se a API Vista está disponível"""
        try:
            result = await self._request("GET", "/health")
            return result is not None
        except Exception:
            return False
