"""
Configurações da aplicação FastAPI
"""

from pydantic_settings import BaseSettings
from typing import Optional
import os


class Settings(BaseSettings):
    """Configurações da aplicação"""

    # Application
    app_name: str = "Dashboard Gralha"
    app_version: str = "1.0.0"
    debug: bool = False
    environment: str = "development"

    # Database
    database_url: str = "postgresql://gralha:gralha_password@db:5432/dashboard_gralha"
    db_host: str = "db"
    db_port: int = 5432
    db_user: str = "gralha"
    db_password: str = "gralha_password"
    db_name: str = "dashboard_gralha"

    # Redis
    redis_url: str = "redis://redis:6379/0"
    redis_host: str = "redis"
    redis_port: int = 6379

    # FastAPI
    api_host: str = "0.0.0.0"
    api_port: int = 8000
    api_workers: int = 4

    # JWT
    secret_key: str = "your-secret-key-change-in-production"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30

    # API Vista CRM
    vista_api_base_url: str = "https://novovista-rest.vistahost.com.br/api"
    vista_api_key: Optional[str] = None
    vista_tenant_id: Optional[str] = None

    # Synchronization
    sync_interval_hours: int = 24
    sync_batch_size: int = 100
    sync_retry_attempts: int = 3
    sync_retry_delay_seconds: int = 5

    # CORS
    cors_origins: list = ["http://localhost:3000", "http://localhost:8000"]
    cors_allow_credentials: bool = True
    cors_allow_methods: list = ["*"]
    cors_allow_headers: list = ["*"]

    # Logging
    log_level: str = "INFO"
    log_format: str = "json"

    # Security
    allowed_hosts: list = ["localhost", "127.0.0.1"]
    secure_ssl_redirect: bool = False
    session_cookie_secure: bool = False
    csrf_cookie_secure: bool = False

    # Feature Flags
    enable_webhooks: bool = False
    enable_alerts: bool = False
    enable_export: bool = True

    class Config:
        env_file = ".env"
        case_sensitive = False


# Load settings from environment
settings = Settings()
