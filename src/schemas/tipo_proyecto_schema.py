# src/schemas/tipo_proyecto_schema.py
from pydantic import BaseModel, ConfigDict, field_validator
from typing import List, Optional
from datetime import datetime
from src.models.audit_mixin import AuditLogs
from src.models.paginacion_model import Paginacion

class TipoProyectoBase(BaseModel):
    nombre: str
    requiere_licencia: Optional[bool] = False

    model_config = ConfigDict(from_attributes=True)

class TipoProyectoCreate(TipoProyectoBase):
    @field_validator("nombre")
    def validar_nombre(cls, v):
        if v is None or v.strip() == "":
            raise ValueError("El campo nombre encuentra vacío; ingresa un dato válido")
        if len(v.strip()) > 50:
            raise ValueError("El campo nombre no puede tener un rango mayor a 50 caracteres")
        return v


class TipoProyectoUpdate(TipoProyectoBase):
    nombre: Optional[str] = None
    @field_validator("nombre", mode="before")
    def validar_nombre(cls, v):
        if v is None:
            return v
        if v.strip() == "":
            raise ValueError("El campo nombre encuentra vacío; ingresa un dato válido")
        if len(v.strip()) > 50:
            raise ValueError("El campo nombre no puede tener un rango mayor a 50 caracteres")
        return v

class TipoProyectoResponse(TipoProyectoBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)

class LogEntityRead(AuditLogs, BaseModel):
    id: int
    nombre: str
    requiere_licencia: Optional[bool]

    model_config = ConfigDict(from_attributes=True)

class TipoProyectoListResponse(BaseModel):
    data: List[TipoProyectoResponse]
    pagination: Paginacion
