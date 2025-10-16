# src/schemas/tramo_sector_schema.py
from pydantic import BaseModel, ConfigDict, constr, condecimal
from typing import List, Optional
from datetime import datetime

class TramoSectorBase(BaseModel):
    id_ruta: Optional[int] = None
    nombre: constr(min_length=1, max_length=255)
    kilometraje_inicial: Optional[condecimal(max_digits=10, decimal_places=3)] = None
    kilometraje_final: Optional[condecimal(max_digits=10, decimal_places=3)] = None

    model_config = ConfigDict(from_attributes=True)

class TramoSectorCreate(TramoSectorBase):
    pass

class TramoSectorUpdate(BaseModel):
    id_ruta: Optional[int] = None
    nombre: Optional[str] = None
    kilometraje_inicial: Optional[condecimal(max_digits=10, decimal_places=3)] = None
    kilometraje_final: Optional[condecimal(max_digits=10, decimal_places=3)] = None

    model_config = ConfigDict(from_attributes=True)

class TramoSectorResponse(TramoSectorBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)

class LogEntityRead(BaseModel):
    id: int
    id_ruta: Optional[int]
    nombre: str
    kilometraje_inicial: Optional[float]
    kilometraje_final: Optional[float]
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

class TramoSectorListResponse(BaseModel):
    data: List[TramoSectorResponse]
    pagination: PaginacionSchema
