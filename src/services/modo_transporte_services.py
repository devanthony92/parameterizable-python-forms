from fastapi import HTTPException, Request, status
from sqlalchemy.orm import Session
from src.models.modo_transporte_model import ModoTransporte
from src.models.logs_model import TipoOperacionEnum
from src.schemas.modo_transporte_schema import ModoTransporteCreate, ModoTransporteUpdate, LogEntityRead
from datetime import datetime, timezone
from typing import Dict, Any, Optional
from src.utils.logs_util import registrar_log, LogUtil

# Servicio para listar las unidades de ejecucion
class ModoService:
    def __init__(self, db: Session):
        self.db = db


    def _base_query(self):
        """Base query que excluye eliminados (soft delete)."""
        return self.db.query(ModoTransporte).filter(ModoTransporte.deleted_at.is_(None), ModoTransporte.activo == True)
    
    def get(self, payload: Dict[str, Any], is_active: Optional[bool] = None) -> Optional[ModoTransporte]:
        """
        Busca el primer registro que cumpla filtros del payload.
        payload: dict de campo:valor, e.g. {"id": 1} o {"nombre": "Zona Norte"}
        """
        query = self.db.query(ModoTransporte)
        for field, value in payload.items():
            if hasattr(ModoTransporte, field) and value is not None:
                query = query.filter(getattr(ModoTransporte, field) == value)
        if is_active is not None:
            query = query.filter(ModoTransporte.activo == is_active)
        return query.first()


# servicio para listar  los registros
    def list_modo(self, skip: int, limit: int):
        return self._base_query().offset(skip).limit(limit).all()
    def count_modo(self):
        return self._base_query().count()
    
    
    # servicio para crear un registro
    async def create_modo(self, payload: ModoTransporteCreate, 
                            request: Request, tokenpayload: dict):
        if payload.nombre:
            existing = self.get({"nombre": payload.nombre})
            if existing:
                raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="El modo ya existe")
        
        #crear el nuevo registro
        entity = ModoTransporte(**payload.model_dump(), id_persona=tokenpayload.get("sub"))
        
        # guardar en la base de datos
        try:
            self.db.add(entity)
            self.db.commit()
            self.db.refresh(entity)
        except Exception as e:
            self.db.rollback()
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                                detail=f"Error guardando la Modo de transpote: {e}")

        # Registro de logs
        registrar_log(LogUtil(self.db),
            tabla_afectada="Modo",
            id_registro_afectado=entity.id,
            tipo_operacion=TipoOperacionEnum.INSERT.value,
            datos_nuevos=LogEntityRead.from_orm(entity).model_dump(mode="json"),
            datos_viejos=None,
            id_persona_operacion=entity.id_persona,
            ip_origen=request.client.host,
            user_agent=1)
        
        return LogEntityRead.from_orm(entity)
    
    
    
    async def show(self, modo_id: int):
        entity = self.get({"id": modo_id}, is_active=True)
        if not entity:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="El modo no fue hallada")
        return entity
    
    # servicio para editar logicamente un registro
    async def update_modo(self, modo_id: int, 
                            payload: ModoTransporteUpdate, 
                            request: Request, tokenpayload: dict):
        
        #revisar si el registro existe
        if payload.nombre:
            existe = self.get({"nombre": payload.nombre})
            if existe:
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail=f"El nombre '{payload.nombre}' ya está siendo usado por otro ModoTransporte."
                )
        #buscar el registro que se va a actualizar
        data = self.get({"id": modo_id}, is_active= True)
        if not data:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="El modo no fue hallada")
        
        #log de datos viejos antes de la actualizacion
        datos_viejos = LogEntityRead.from_orm(data).model_dump(mode="json")

        #actualizamos los datos
        for field, value in payload.model_dump(exclude_unset=True).items():
            setattr(data, field, value)

        data.id_persona = tokenpayload.get("sub")
        data.updated_at = datetime.now(timezone.utc)
        
        #guardamos los cambios
        try:
            self.db.add(data)
            self.db.commit()
            self.db.refresh(data)
        except Exception as e:
            self.db.rollback()
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                                detail=f"Error actualizando la Modo de transpote: {e}")
                    
            # Registro de logs
        registrar_log(LogUtil(self.db),
            tabla_afectada="modo",
            id_registro_afectado=data.id,
            tipo_operacion=TipoOperacionEnum.UPDATE.value,
            datos_nuevos=LogEntityRead.from_orm(data).model_dump(mode="json"),
            datos_viejos=datos_viejos,
            id_persona_operacion=data.id_persona,
            ip_origen=request.client.host,
            user_agent=1)
        
        return LogEntityRead.from_orm(data)
    
    
    # servicio para eliminar logicamente un registro
    async def delete_modo(self, modo_id: int, request: Request, tokenpayload: dict):
        #buscar el registro que se va a eliminar
        datadelete = self.get({"id": modo_id, "activo": True})
        if not datadelete:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="El modo no fue hallada")
        
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
                                detail=f"Error actualizando la Modo de transpote: {e}")
        
        
        
        registrar_log(LogUtil(self.db),
            tabla_afectada="modo",
            id_registro_afectado=datadelete.id,
            tipo_operacion=TipoOperacionEnum.DELETE.value,
            datos_nuevos=LogEntityRead.from_orm(datadelete).model_dump(mode="json"),
            datos_viejos=datos_viejos,
            id_persona_operacion=datadelete.id_persona,
            ip_origen=request.client.host,
            user_agent=1)
        
        return LogEntityRead.from_orm(datadelete)