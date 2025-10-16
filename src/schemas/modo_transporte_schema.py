# src/schemas/modo_transporte_schema.py
from pydantic import BaseModel, ConfigDict, constr
from typing import List, Optional
from datetime import datetime
from src.models.audit_mixin import AuditMixin

class ModoTransporteBase(BaseModel):
    nombre: constr(min_length=1, max_length=50)

    model_config = ConfigDict(from_attributes=True)

class ModoTransporteCreate(ModoTransporteBase):
    pass

class ModoTransporteUpdate(BaseModel):
    nombre: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)

class ModoTransporteResponse(ModoTransporteBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)

class LogEntityRead(AuditMixin, BaseModel):
    id: int
    nombre: str

    model_config = ConfigDict(from_attributes=True)

class PaginacionSchema(BaseModel):
    skip: int
    limit: int
    total: int
    page: int
    pages: int

class ModoTransporteListResponse(BaseModel):
    data: List[ModoTransporteResponse]
    pagination: PaginacionSchema
