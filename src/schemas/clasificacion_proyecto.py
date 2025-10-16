# src/schemas/clasificacion_proyecto_schema.py
from pydantic import BaseModel, ConfigDict, constr
from typing import List, Optional
from datetime import datetime
from src.models.audit_mixin import AuditMixin

class ClasificacionProyectoBase(BaseModel):
    nombre: constr(min_length=1, max_length=50)

    model_config = ConfigDict(from_attributes=True)

class ClasificacionProyectoCreate(ClasificacionProyectoBase):
    pass

class ClasificacionProyectoUpdate(BaseModel):
    nombre: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)

class ClasificacionProyectoResponse(ClasificacionProyectoBase):
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

class ClasificacionProyectoListResponse(BaseModel):
    data: List[ClasificacionProyectoResponse]
    pagination: PaginacionSchema
