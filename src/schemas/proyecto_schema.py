from pydantic import BaseModel, ConfigDict, constr
from typing import Optional, List
from datetime import date, datetime
from src.schemas.contrato_schema import ContratoResponse

class ProyectoBase(BaseModel):
    id_unidad_ejecutora: Optional[int] = None
    id_direccion_territorial: Optional[int] = None
    id_tipo_proyecto: Optional[int] = None
    id_ruta: Optional[int] = None
    id_tramo_sector: Optional[int] = None
    id_clasificacion: Optional[int] = None
    id_modo_transporte: Optional[int] = None
    id_funcionalidad: Optional[int] = None
    id_categorizacion: Optional[int] = None
    objeto_proyecto: Optional[str] = None
    resolucion_licencia: Optional[str] = None
    fecha_resolucion: Optional[date] = None
    es_convenio_interadministrativo: Optional[bool] = False
    numero_convenio: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)

class ProyectoCreate(ProyectoBase):
    pass

class ProyectoUpdate(ProyectoBase):
    es_convenio_interadministrativo: Optional[bool] = None
    
    
class ProyectoResponse(ProyectoBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None
    contratos: Optional[List[ContratoResponse]] = None

    model_config = ConfigDict(from_attributes=True)

class LogEntityRead(BaseModel):
    id: int
    id_unidad_ejecutora: Optional[int]
    id_direccion_territorial: Optional[int]
    id_tipo_proyecto: Optional[int]
    id_ruta: Optional[int]
    id_tramo_sector: Optional[int]
    id_clasificacion: Optional[int]
    id_modo_transporte: Optional[int]
    id_funcionalidad: Optional[int]
    id_categorizacion: Optional[int]
    objeto_proyecto: Optional[str]
    resolucion_licencia: Optional[str]
    fecha_resolucion: Optional[date]
    es_convenio_interadministrativo: Optional[bool]
    numero_convenio: Optional[str]
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

class ProyectoListResponse(BaseModel):
    data: List[ProyectoResponse]
    pagination: PaginacionSchema
