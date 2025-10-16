# src/schemas/categorizacion_carretera_schema.py
from pydantic import BaseModel, ConfigDict, constr
from typing import List, Optional
from datetime import datetime

class CategorizacionCarreteraBase(BaseModel):
    nombre: constr(min_length=1, max_length=100)

    model_config = ConfigDict(from_attributes=True)

class CategorizacionCarreteraCreate(CategorizacionCarreteraBase):
    pass

class CategorizacionCarreteraUpdate(BaseModel):
    nombre: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)

class CategorizacionCarreteraResponse(CategorizacionCarreteraBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)

class LogEntityRead(BaseModel):
    id: int
    nombre: str
    id_persona: Optional[int]
    activo: bool
    created_at: datetime
    updated_at: Optional[datetime] = None
    deleted_at: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)

class PaginacionSchema(BaseModel):
    skip: int
    limit: int
    total: int
    page: int
    pages: int

class CategorizacionCarreteraListResponse(BaseModel):
    data: List[CategorizacionCarreteraResponse]
    pagination: PaginacionSchema
