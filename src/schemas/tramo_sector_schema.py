# src/schemas/tramo_sector_schema.py
from pydantic import BaseModel, ConfigDict, field_validator, condecimal
from typing import List, Optional
from datetime import datetime
from src.models.audit_mixin import AuditLogs
from src.models.paginacion_model import Paginacion

class TramoSectorBase(BaseModel):
    id_ruta: Optional[int] = None
    nombre: str
    kilometraje_inicial: Optional[condecimal(max_digits=10, decimal_places=3)] = None
    kilometraje_final: Optional[condecimal(max_digits=10, decimal_places=3)] = None

    model_config = ConfigDict(from_attributes=True)

class TramoSectorCreate(TramoSectorBase):
    @field_validator("nombre")
    def validar_nombre(cls, v):
        if v is None or v.strip() == "":
            raise ValueError("El campo nombre encuentra vacío; ingresa un dato válido")
        if len(v.strip()) > 255:
            raise ValueError("El campo nombre no puede tener un rango mayor a 255 caracteres")
        return v
    @field_validator("id_ruta","kilometraje_inicial","kilometraje_final")
    def id_mayor_que_cero(cls, v,info):
        if v is None:
            return v
        if v <= 0:
            raise ValueError(f"El campo '{info.field_name}' debe ser mayor que cero")
        return v


class TramoSectorUpdate(TramoSectorBase):
    nombre: Optional[str] = None

    @field_validator("nombre", mode="before")
    def validar_nombre(cls, v):
        if v is None:
            return v
        if v.strip() == "":
            raise ValueError("El campo nombre encuentra vacío; ingresa un dato válido")
        if len(v.strip()) > 255:
            raise ValueError("El campo nombre no puede tener un rango mayor a 255 caracteres")
        return v
    @field_validator("id_ruta","kilometraje_inicial","kilometraje_final")
    def id_mayor_que_cero(cls, v,info):
        if v is None:
            return v
        if v <= 0:
            raise ValueError(f"El campo '{info.field_name}' debe ser mayor que cero")
        return v
    

class TramoSectorResponse(TramoSectorBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)

class LogEntityRead(AuditLogs, BaseModel):
    id: int
    id_ruta: Optional[int]
    nombre: str
    kilometraje_inicial: Optional[float]
    kilometraje_final: Optional[float]

    model_config = ConfigDict(from_attributes=True)

class TramoSectorListResponse(BaseModel):
    data: List[TramoSectorResponse]
    pagination: Paginacion
