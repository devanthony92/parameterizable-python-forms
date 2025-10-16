from pydantic import BaseModel, ConfigDict, constr
from typing import Optional, List
from datetime import date, datetime
from decimal import Decimal
import enum

class TipoContratoEnum(str, enum.Enum):
    obra = "obra"
    interventoria = "interventoria"
    convenio = "convenio"

class ContratoBase(BaseModel):
    id_proyecto: Optional[int] = None
    numero_contrato: constr(min_length=1, max_length=100)
    tipo_contrato: TipoContratoEnum
    fecha_contrato: Optional[date] = None
    objeto_contrato: Optional[str] = None
    fecha_inicio: Optional[date] = None
    fecha_terminacion: Optional[date] = None
    valor_contrato: Optional[Decimal] = None
    recursos_sostenibilidad: Optional[Decimal] = None

    model_config = ConfigDict(from_attributes=True)

class ContratoCreate(ContratoBase):
    pass

class ContratoUpdate(BaseModel):
    id_proyecto: Optional[int] = None
    numero_contrato: Optional[str] = None
    tipo_contrato: Optional[TipoContratoEnum] = None
    fecha_contrato: Optional[date] = None
    objeto_contrato: Optional[str] = None
    fecha_inicio: Optional[date] = None
    fecha_terminacion: Optional[date] = None
    valor_contrato: Optional[Decimal] = None
    recursos_sostenibilidad: Optional[Decimal] = None

    model_config = ConfigDict(from_attributes=True)

class ContratoResponse(ContratoBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)

class LogEntityRead(BaseModel):
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
    id_persona: Optional[int]
    activo: bool
    created_at: datetime
    updated_at: Optional[datetime]
    deleted_at: Optional[datetime]

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
