"""
Configuração de banco de dados PostgreSQL com SQLAlchemy
"""

from sqlalchemy import create_engine, event
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.pool import NullPool
import logging
from app.config import settings

logger = logging.getLogger(__name__)

# Create engine
engine = create_engine(
    settings.database_url,
    echo=settings.debug,
    poolclass=NullPool if settings.environment == "development" else None,
    pool_pre_ping=True,
    pool_recycle=3600,
)

# Create session factory
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
    expire_on_commit=False,
)

# Base class for models
Base = declarative_base()


def get_db() -> Session:
    """
    Dependency para obter sessão do banco de dados
    
    Yields:
        Session: Sessão do banco de dados
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_db():
    """Inicializa o banco de dados criando todas as tabelas"""
    try:
        Base.metadata.create_all(bind=engine)
        logger.info("Database initialized successfully")
    except Exception as e:
        logger.error(f"Error initializing database: {e}")
        raise


def drop_db():
    """Remove todas as tabelas do banco de dados (apenas para testes)"""
    Base.metadata.drop_all(bind=engine)
    logger.warning("Database dropped")


@event.listens_for(engine, "connect")
def set_sqlite_pragma(dbapi_conn, connection_record):
    """Configure PostgreSQL para melhor performance"""
    if "postgresql" in settings.database_url:
        cursor = dbapi_conn.cursor()
        cursor.execute("SET application_name = 'dashboard_gralha'")
        cursor.close()
