from pydantic import BaseModel, ConfigDict, field_validator
from typing import Optional, List
from datetime import date, datetime
from decimal import Decimal
import enum
from src.models.audit_mixin import AuditMixin

class TipoContratoEnum(str, enum.Enum):
    obra = "obra"
    interventoria = "interventoria"
    convenio = "convenio"

class ContratoBase(BaseModel):
    id_proyecto: Optional[int] = None
    numero_contrato: str
    tipo_contrato: TipoContratoEnum
    fecha_contrato: Optional[date] = None
    objeto_contrato: Optional[str] = None
    fecha_inicio: Optional[date] = None
    fecha_terminacion: Optional[date] = None
    valor_contrato: Optional[Decimal] = None
    recursos_sostenibilidad: Optional[Decimal] = None

    model_config = ConfigDict(from_attributes=True)

class ContratoCreate(ContratoBase):
    
    @field_validator("id_proyecto", "valor_contrato", "recursos_sostenibilidad", mode="before")
    def campos_mayores_que_cero(cls, v, info):
        if v is None:
            return v  # No se valida si no se ingresa el campo opcional

        if v <= 0:
            raise ValueError(f"El campo '{info.field_name}' debe ser mayor que cero")
        return v
        
    @field_validator("numero_contrato")
    def validar_numero_contrato(cls, valor, info):
        if valor is None or valor.strip() == "":
            raise ValueError("El campo 'numero_contrato' se encuentra vacío, ingresa un dato válido")
        if len(valor.strip()) > 100:
            raise ValueError("El campo 'numero_contrato' no puede tener un rango mayor a 255 caracteres")
        return valor

class ContratoUpdate(ContratoBase):
    numero_contrato: Optional[str] = None
    tipo_contrato: Optional[TipoContratoEnum] = None

    @field_validator("id_proyecto", "valor_contrato", "recursos_sostenibilidad", mode="before")
    def campos_mayores_que_cero(cls, v, info):
        if v is None:
            return v  # No se valida si no se actualiza, el campo es opcional

        if v <= 0:
            raise ValueError(f"El campo '{info.field_name}' debe ser mayor que cero")
        return v
        
    @field_validator("numero_contrato", mode="before")
    def validar_numero_contrato(cls, v, info):
        if v is None:
            return v  # No se valida si no se actualiza, el campo es opcional

        if v is None or v.strip() == "":
            raise ValueError("El campo 'numero_contrato' se encuentra vacío, ingresa un dato válido")
        if len(v) > 255:
            raise ValueError("El campo 'numero_contrato' no puede tener un rango mayor a 255 caracteres")
        return v

class ContratoResponse(ContratoBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None


class LogEntityRead(AuditMixin, BaseModel):
    id: int
    id_proyecto: Optional[int]
    numero_contrato: str
    tipo_contrato: TipoContratoEnum
    fecha_contrato: Optional[date]
    objeto_contrato: Optional[str]
    fecha_inicio: Optional[date]
    fecha_terminacion: Optional[date]
    valor_contrato: Optional[Decimal]
    recursos_sostenibilidad: Optional[Decimal]

    model_config = ConfigDict(from_attributes=True)

class PaginacionSchema(BaseModel):
    skip: int
    limit: int
    total: int
    page: int
    pages: int

class ContratoListResponse(BaseModel):
    data: List[ContratoResponse]
    pagination: PaginacionSchema
