# src/schemas/tipo_proyecto_schema.py
from pydantic import BaseModel, ConfigDict, constr
from typing import List, Optional
from datetime import datetime
from src.models.audit_mixin import AuditMixin

class TipoProyectoBase(BaseModel):
    nombre: constr(min_length=1, max_length=50)
    requiere_licencia: Optional[bool] = False

    model_config = ConfigDict(from_attributes=True)

class TipoProyectoCreate(TipoProyectoBase):
    pass

class TipoProyectoUpdate(BaseModel):
    nombre: Optional[str] = None
    requiere_licencia: Optional[bool] = None

    model_config = ConfigDict(from_attributes=True)

class TipoProyectoResponse(TipoProyectoBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)

class LogEntityRead(AuditMixin, BaseModel):
    id: int
    nombre: str
    requiere_licencia: Optional[bool]

    model_config = ConfigDict(from_attributes=True)

class PaginacionSchema(BaseModel):
    skip: int
    limit: int
    total: int
    page: int
    pages: int

class TipoProyectoListResponse(BaseModel):
    data: List[TipoProyectoResponse]
    pagination: PaginacionSchema
