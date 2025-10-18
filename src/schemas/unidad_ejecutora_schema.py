from typing import List, Optional
from datetime import date, datetime
from pydantic import BaseModel, ConfigDict, field_validator
from src.models.audit_mixin import AuditLogs
from src.models.paginacion_model import Paginacion


class UnidadEjecutoraBase(BaseModel):
    nombre: str
    descripcion: Optional[str]


    model_config = ConfigDict(from_attributes=True)


class UnidadEjecutoraCreate(UnidadEjecutoraBase):
    @field_validator("nombre")
    def validar_nombre(cls, v):
        if v.strip() == "":
            raise ValueError("El campo nombre de la unidad ejecutora se encuentra vacío; ingresa un dato válido")
        if len(v.strip()) > 255:
            raise ValueError("El campo nombre no puede tener un rango mayor a 255 caracteres")
        return v


class UnidadEjecutoraUpdate(UnidadEjecutoraBase):
    nombre : Optional[str] = None

    @field_validator("nombre", mode="before")
    def validar_nombre(cls, v):
        if v is None:
            return v
        if v.strip() == "":
            raise ValueError("El campo nombre de la unidad ejecutora se encuentra vacío; ingresa un dato válido")
        if len(v.strip()) > 255:
            raise ValueError("El campo nombre no puede tener un rango mayor a 255 caracteres")
        return v


class UnidadEjecutoraResponse(UnidadEjecutoraBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)

class LogEntityRead(AuditLogs, BaseModel):
    id: int
    nombre: str
    descripcion: str

    model_config = ConfigDict(from_attributes=True)


class UnidadEjecutoraListResponse(BaseModel):
    data: List[UnidadEjecutoraResponse]
    pagination: Paginacion
