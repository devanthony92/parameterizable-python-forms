from pydantic import BaseModel, ConfigDict, field_validator
from typing import Optional, List
from datetime import date, datetime
from src.models.audit_mixin import AuditLogs
from src.models.paginacion_model import Paginacion

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

    @field_validator(
        "id_unidad_ejecutora", "id_direccion_territorial", "id_tipo_proyecto",
        "id_ruta", "id_tramo_sector", "id_clasificacion", "id_modo_transporte",
        "id_funcionalidad", "id_categorizacion"
    )
    def ids_mayores_que_cero(cls, v, info):
        if v is None:
            return v
        if v <= 0:
            raise ValueError(f"El campo '{info.field_name}' debe ser mayor que cero")
        return v

class ProyectoUpdate(ProyectoBase):
    es_convenio_interadministrativo: Optional[bool] = None
    
    @field_validator(
        "id_unidad_ejecutora", "id_direccion_territorial", "id_tipo_proyecto",
        "id_ruta", "id_tramo_sector", "id_clasificacion", "id_modo_transporte",
        "id_funcionalidad", "id_categorizacion"
    )
    def ids_mayores_que_cero(cls, v, info):
        if v is None:
            return v
        if v <= 0:
            raise ValueError(f"El campo '{info.field_name}' debe ser mayor que cero")
        return v
    
class ProyectoResponse(ProyectoBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)

class LogEntityRead(AuditLogs, BaseModel):
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

    model_config = ConfigDict(from_attributes=True)

class ProyectoListResponse(BaseModel):
    data: List[ProyectoResponse]
    pagination: Paginacion
