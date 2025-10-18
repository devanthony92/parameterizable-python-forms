# src/schemas/ruta_schema.py
from pydantic import BaseModel, ConfigDict, field_validator
from typing import List, Optional
from datetime import datetime
from src.models.audit_mixin import AuditLogs
from src.models.paginacion_model import Paginacion

class RutaBase(BaseModel):
    nombre: str
    codigo: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)

class RutaCreate(RutaBase):
    @field_validator("nombre")
    def validar_nombre(cls, v):
        if v is None or v.strip() == "":
            raise ValueError("El campo nombre encuentra vacío; ingresa un dato válido")
        if len(v.strip()) > 255:
            raise ValueError("El campo nombre no puede tener un rango mayor a 255 caracteres")
        return v
    @field_validator("codigo", mode="before")
    def validar_codigo(cls, v):
        if v is None:
            return v
        if v is None or v.strip() == "":
            raise ValueError("El campo codigo encuentra vacío; ingresa un dato válido")
        if len(v.strip()) > 20:
            raise ValueError("El campo codigo no puede tener un rango mayor a 20 caracteres")
        return v

class RutaUpdate(RutaBase):
    nombre: Optional[str] = None

    @field_validator("nombre")
    def validar_nombre(cls, v):
        if v is None:
            return v
        if v is None or v.strip() == "":
            raise ValueError("El campo nombre encuentra vacío; ingresa un dato válido")
        if len(v.strip()) > 255:
            raise ValueError("El campo nombre no puede tener un rango mayor a 255 caracteres")
        return v
    @field_validator("codigo", mode="before")
    def validar_codigo(cls, v):
        if v is None:
            return v
        if v is None or v.strip() == "":
            raise ValueError("El campo codigo encuentra vacío; ingresa un dato válido")
        if len(v.strip()) > 20:
            raise ValueError("El campo codigo no puede tener un rango mayor a 20 caracteres")
        return v


class RutaResponse(RutaBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)

class LogEntityRead(AuditLogs, BaseModel):
    id: int
    nombre: str
    codigo: Optional[str]

    model_config = ConfigDict(from_attributes=True)

class RutaListResponse(BaseModel):
    data: List[RutaResponse]
    pagination: Paginacion
