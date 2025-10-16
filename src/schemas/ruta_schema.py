# src/schemas/ruta_schema.py
from pydantic import BaseModel, ConfigDict, constr
from typing import List, Optional
from datetime import datetime
from src.models.audit_mixin import AuditMixin

class RutaBase(BaseModel):
    nombre: constr(min_length=1, max_length=255)
    codigo: Optional[constr(max_length=20)] = None

    model_config = ConfigDict(from_attributes=True)

class RutaCreate(RutaBase):
    pass

class RutaUpdate(BaseModel):
    nombre: Optional[str] = None
    codigo: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)

class RutaResponse(RutaBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)

class LogEntityRead(AuditMixin, BaseModel):
    id: int
    nombre: str
    codigo: Optional[str]

    model_config = ConfigDict(from_attributes=True)

class PaginacionSchema(BaseModel):
    skip: int
    limit: int
    total: int
    page: int
    pages: int

class RutaListResponse(BaseModel):
    data: List[RutaResponse]
    pagination: PaginacionSchema
