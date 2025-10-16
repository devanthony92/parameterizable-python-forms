from pydantic import BaseModel, ConfigDict
from typing import List, Optional
from datetime import datetime
from src.models.audit_mixin import AuditMixin

class UnidadEjecutoraSchema(BaseModel):
    nombre: str
    descripcion: Optional[str]

class UnidadEjecutoraCreate(UnidadEjecutoraSchema):
    pass

class UnidadEjecutoraUpdate(UnidadEjecutoraSchema):
    pass

class UnidadEjecutoraResponse(UnidadEjecutoraSchema):
    id: int

class LogEntityRead(AuditMixin, BaseModel):
    id: int
    nombre: str
    descripcion: Optional[str]

    model_config = ConfigDict(from_attributes=True)

class PaginacionSchema(BaseModel):
    skip: int
    limit: int
    total: int
    page: int
    pages: int

class UnidadEjecutoraListResponse(BaseModel):
    data: List[UnidadEjecutoraSchema]
    pagination: PaginacionSchema

