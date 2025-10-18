from fastapi import HTTPException, Request, status
from sqlalchemy.orm import Session
from src.models.tramo_sector import TramoSector
from src.models.logs_model import TipoOperacionEnum
from src.schemas.tramo_sector_schema import TramoSectorCreate, TramoSectorUpdate, LogEntityRead
from datetime import datetime, timezone
from typing import Optional, Dict, Any
from src.utils.logs_util import registrar_log, LogUtil

# Servicio para listar las unidades de ejecucion
class TramoService:
    def __init__(self, db: Session):
        self.db = db

    #funciones base para consultas
    def _base_query(self):
        return self.db.query(TramoSector).filter(TramoSector.deleted_at.is_(None))

    def get(self, payload: Dict[str, Any], is_active: Optional[bool] = None):
        query = self.db.query(TramoSector)
        for field, value in payload.items():
            if hasattr(TramoSector, field) and value is not None:
                query = query.filter(getattr(TramoSector, field) == value)
        if is_active is not None:
            query = query.filter(TramoSector.activo == is_active)
        return query.first()
    
# servicio para listar  los registros
    def list_tramo(self, skip: int, limit: int):
        return self._base_query().offset(skip).limit(limit).all()
    def count_tramo(self):
        return self._base_query().count()
    
    
    # servicio para crear un registro
    async def create_tramo(self, payload: TramoSectorCreate, request: Request, tokenpayload: dict):

        existing = self.get({"nombre": payload.nombre})
        if existing:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="El tramo ya existe")
        
        #crear el nuevo registro
        entity = TramoSector(**payload.model_dump(), id_persona=tokenpayload.get("sub"))

        # guardar en la base de datos
        try:
            self.db.add(entity)
            self.db.commit()
            self.db.refresh(entity)
        except Exception as e:
            self.db.rollback()
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                                detail=f"Error guardando la Tramo/Sector: {e}")
        
        # Registro de logs
        registrar_log(LogUtil(self.db),
            tabla_afectada="tramos_sectores",
            id_registro_afectado=entity.id,
            tipo_operacion=TipoOperacionEnum.INSERT.value,
            datos_nuevos=LogEntityRead.from_orm(entity).model_dump(mode="json"),
            datos_viejos=None,
            id_persona_operacion=entity.id_persona,
            ip_origen=request.client.host,
            user_agent=1)
        
        return LogEntityRead.from_orm(entity)
    
    # servicio para ver un registro por id
    async def show(self, tramo_id: int):
        entity = self.get({"id": tramo_id, "activo": True})
        if not entity:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="El modo no fue hallada")
        return entity
    
    # servicio para editar logicamente un registro
    async def update_tramo(self, tramo_id: int, 
                            payload: TramoSectorUpdate, 
                            request: Request, tokenpayload: dict):
        if payload.nombre:
            existe = self.get({"nombre": payload.nombre})
            if existe:
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail=f"El nombre '{payload.nombre}' ya está siendo usado por otro ModoTransporte."
                )
        #buscar el registro a actualizar
        data = self.get({"id": tramo_id, "activo": True})
        if not data:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="El tramo no fue hallada")
        
        #log de los datos viejos    
        datos_viejos = LogEntityRead.from_orm(data).model_dump(mode="json")

        #actualizar los datos
        for field, value in payload.model_dump(exclude_unset=True).items():
            setattr(data, field, value)

        data.id_persona = tokenpayload.get("sub")
        data.updated_at = datetime.now(timezone.utc)
            
        # guardar los cambios
        try:
            self.db.add(data)
            self.db.commit()
            self.db.refresh(data)
        except Exception as e:
            self.db.rollback()
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                                detail=f"Error actualizando la Tramo/Sector: {e}")
            
            # Registro de logs
        registrar_log(LogUtil(self.db),
            tabla_afectada="tramos_sectores",
            id_registro_afectado=data.id,
            tipo_operacion=TipoOperacionEnum.UPDATE.value,
            datos_nuevos=LogEntityRead.from_orm(data).model_dump(mode="json"),
            datos_viejos=datos_viejos,
            id_persona_operacion=data.id_persona,
            ip_origen=request.client.host,
            user_agent=1)
        
        return LogEntityRead.from_orm(data)
    
    
    # servicio para eliminar logicamente un registro
    async def delete_tramo(self, tramo_id: int, request: Request, tokenpayload: dict):

        datadelete = self.get({"id": tramo_id, "activo": True}) 
        if not datadelete:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="El tramo no fue hallada")
        
        # log de los datos viejos
        datos_viejos = LogEntityRead.from_orm(datadelete).model_dump(mode="json")

    # le paso un valor false para realizar un sofdelete para un eliminado logico
        datadelete.activo = False
        datadelete.deleted_at = datetime.now(timezone.utc)
        datadelete.id_persona = tokenpayload.get("sub")

        # guardar los cambios
        try:
            self.db.add(datadelete)
            self.db.commit()
            self.db.refresh(datadelete)
        except Exception as e:
            self.db.rollback()
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                                detail=f"Error eliminando la Tramo/Sector: {e}")

        
        registrar_log(LogUtil(self.db),
            tabla_afectada="tramos_sectores",
            id_registro_afectado=datadelete.id,
            tipo_operacion=TipoOperacionEnum.DELETE.value,
            datos_nuevos=LogEntityRead.from_orm(datadelete).model_dump(mode="json"),
            datos_viejos=datos_viejos,
            id_persona_operacion=datadelete.id_persona,
            ip_origen=request.client.host,
            user_agent=1)
        
        return LogEntityRead.from_orm(datadelete)