from pydantic import BaseModel, ConfigDict, field_validator
from typing import List, Optional
from datetime import datetime
from src.models.audit_mixin import AuditMixin

class DireccionTerritorialBase(BaseModel):
    nombre : str
    region : Optional[str]

class DireccionTerritorialCreate(DireccionTerritorialBase):

    @field_validator("nombre")
    def validar_nombre(cls, valor, info):
        if valor is None or valor.strip() == "":
            raise ValueError("El campo nombre de la unidad ejecutora se encuentra vacío; ingresa un dato válido")
        if len(valor.strip()) > 255:
            raise ValueError("El campo nombre no puede tener un rango mayor a 255 caracteres")
        return valor


class DireccionTerritorialUpdate(DireccionTerritorialBase):
    nombre : Optional[str] = None

    @field_validator("nombre", mode="before")
    def validar_nombre(cls, valor, info):
        if valor is None:
            return valor
        if valor is None or valor.strip() == "":
            raise ValueError("El campo nombre de la unidad ejecutora se encuentra vacío; ingresa un dato válido")
        if len(valor.strip()) > 255:
            raise ValueError("El campo nombre no puede tener un rango mayor a 255 caracteres")
        return valor


class DireccionTerritorialResponse(DireccionTerritorialBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

class LogEntityRead(AuditMixin, BaseModel):
    id: int
    nombre: str
    region: Optional[str]    

    model_config = ConfigDict(from_attributes=True)

class PaginacionSchema(BaseModel):
    skip: int
    limit: int
    total: int
    page: int
    pages: int

class DireccionTerritorialListResponse(BaseModel):
    data: List[DireccionTerritorialResponse]
    pagination: PaginacionSchema

