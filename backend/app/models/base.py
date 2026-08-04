"""
Base model com campos comuns
"""

from sqlalchemy import Column, Integer, DateTime, String
from sqlalchemy.orm import declarative_mixin
from datetime import datetime
import uuid


@declarative_mixin
class BaseModel:
    """Classe base com campos comuns a todos os modelos"""

    id = Column(Integer, primary_key=True, index=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    deleted_at = Column(DateTime, nullable=True)  # Soft delete

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__} id={self.id}>"
