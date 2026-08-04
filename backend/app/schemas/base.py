"""
Base Pydantic Schema
"""

from pydantic import BaseModel, ConfigDict
from datetime import datetime
from typing import Optional


class BaseSchema(BaseModel):
    """Base schema com campos comuns"""

    model_config = ConfigDict(from_attributes=True)


class BaseReadSchema(BaseSchema):
    """Base schema para leitura (inclui campos de auditoria)"""

    id: int
    created_at: datetime
    updated_at: datetime
    deleted_at: Optional[datetime] = None
