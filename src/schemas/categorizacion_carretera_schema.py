# src/schemas/categorizacion_carretera_schema.py
from pydantic import BaseModel, ConfigDict, field_validator
from typing import List, Optional
from src.models.paginacion_model import Paginacion
from src.models.audit_mixin import AuditLogs
from datetime import datetime

class CategorizacionCarreteraBase(BaseModel):
    nombre: str

    model_config = ConfigDict(from_attributes=True)

class CategorizacionCarreteraCreate(CategorizacionCarreteraBase):
    @field_validator("nombre")
    def validar_nombre(cls,v):
        if v is None or v.strip() == "":
            raise ValueError("El campo nombre de la categorizacion se encuentra vacío; ingresa un dato válido")
        if len(v.strip()) > 100:
            raise ValueError("El campo nombre no puede tener un rango mayor a 100 caracteres")
        return v
        

class CategorizacionCarreteraUpdate(CategorizacionCarreteraBase):
    nombre: Optional[str] = None
    
    @field_validator("nombre", mode="before")
    def validar_nombre(cls, v):
        if v is None:
            return v
        if v.strip() == "":
            raise ValueError("El campo nombre de la categorizacion se encuentra vacío; ingresa un dato válido")
        if len(v.strip()) > 100:
            raise ValueError("El campo nombre no puede tener un rango mayor a 100 caracteres")
        return v
    
class CategorizacionCarreteraResponse(CategorizacionCarreteraBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

class LogEntityRead(AuditLogs, BaseModel):
    id: int
    nombre: str

    model_config = ConfigDict(from_attributes=True)


class CategorizacionCarreteraListResponse(BaseModel):
    data: List[CategorizacionCarreteraResponse]
    pagination: Paginacion
