from fastapi import HTTPException, Request, status
from sqlalchemy.orm import Session
from src.models.funcionalidad_carretera_model import FuncionalidadCarretera
from src.models.logs_model import TipoOperacionEnum
from src.schemas.funcionalidad_carretera_schema import FuncionalidadCarreteraCreate, LogEntityRead, FuncionalidadCarreteraUpdate
from datetime import datetime, timezone
from typing import Optional, Dict, Any
from src.utils.logs_util import registrar_log, LogUtil

# Servicio para listar las unidades de ejecucion
class FuncionalidadesCarreterService:
    def __init__(self, db: Session):
        self.db = db


    def _base_query(self):
        """Base query que excluye eliminados (soft delete)."""
        return self.db.query(FuncionalidadCarretera).filter(FuncionalidadCarretera.deleted_at.is_(None), FuncionalidadCarretera.activo == True)
    
    def get(self, payload: Dict[str, Any], is_active: Optional[bool] = None) -> Optional[FuncionalidadCarretera]:
        """
        Busca el primer registro que cumpla filtros del payload.
        payload: dict de campo:valor, e.g. {"id": 1} o {"nombre": "Zona Norte"}
        """
        query = self.db.query(FuncionalidadCarretera)
        for field, value in payload.items():
            if hasattr(FuncionalidadCarretera, field) and value is not None:
                query = query.filter(getattr(FuncionalidadCarretera, field) == value)
        if is_active is not None:
            query = query.filter(FuncionalidadCarretera.activo == is_active)
        return query.first()

# servicio para listar  los registros
    def list_funcionalidades_carretera(self, skip: int, limit: int):
        return self._base_query().offset(skip).limit(limit).all()
    def count_funcionalidades_carretera(self):
        return self._base_query().count()
    
    
    # servicio para crear un registro
    async def create_funcionalidades_carretera(self, payload: FuncionalidadCarreteraCreate, 
                            request: Request, tokenpayload: dict):
        if payload.nombre:
            existing = self.get({"nombre": payload.nombre})
            if existing:
                raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="La funcionalidad ya existe")
        
        entity = FuncionalidadCarretera(nombre=payload.nombre, id_persona=tokenpayload.get("sub"), 
                                        activo=True, created_at=datetime.utcnow())
        self.db.add(entity)
        self.db.commit()
        self.db.refresh(entity)
        
        # Registro de logs
        registrar_log(LogUtil(self.db),
            tabla_afectada="funcionalidad_carretera",
            id_registro_afectado=entity.id,
            tipo_operacion=TipoOperacionEnum.INSERT.value,
            datos_nuevos=LogEntityRead.from_orm(entity).model_dump(mode="json"),
            datos_viejos=None,
            id_persona_operacion=entity.id_persona,
            ip_origen=request.client.host,
            user_agent=1)
        
        return LogEntityRead.from_orm(entity)
    
    
    
    async def show(self, funcionalidad_id: int):
        entity = self.get({"id": funcionalidad_id}, is_active=True)
        if not entity:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="La funcionalidad no fue hallada")
        return entity
    
    # servicio para editar logicamente un registro
    async def update_funcionalidades(self, funcionalidad_id: int, 
                            payload: FuncionalidadCarreteraUpdate, 
                            request: Request, tokenpayload: dict):
        
        # revisar si el registro existe
        if payload.nombre:
            existe = self.get({"nombre": payload.nombre})
            if existe:
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail=f"El nombre '{payload.nombre}' ya está siendo usado por otra clasificación."
                )
        
        #buscar el registro a actualizar
        data = self.get({"id": funcionalidad_id}, is_active=True)
        if not data:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="La clasificación no fue hallada")
        
        #log de datos viejos    
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
                                detail=f"Error actualizando la Funcionalidad de carretera: {e}")
        
        # Registro de logs
        registrar_log(LogUtil(self.db),
            tabla_afectada="funcionalidad_carretera",
            id_registro_afectado=data.id,
            tipo_operacion=TipoOperacionEnum.UPDATE.value,
            datos_nuevos=LogEntityRead.from_orm(data).model_dump(mode="json"),
            datos_viejos=datos_viejos,
            id_persona_operacion=data.id_persona,
            ip_origen=request.client.host,
            user_agent=1)
        
        return LogEntityRead.from_orm(data)
    
    
    # servicio para eliminar logicamente un registro
    async def delete_funcionalidad(self,id: int, request: Request, tokenpayload: dict):
        datadelete = self.get({"id":id}, is_active=True)
        if not datadelete:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="La funcionalidad de carretera no fue hallada")
        
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
                                detail=f"Error eliminando la Direccion Territorial: {e}")
        
        
        registrar_log(LogUtil(self.db),
            tabla_afectada="funcionalidad_carretera",
            id_registro_afectado=datadelete.id,
            tipo_operacion=TipoOperacionEnum.DELETE.value,
            datos_nuevos=LogEntityRead.from_orm(datadelete).model_dump(mode="json"),
            datos_viejos=datos_viejos,
            id_persona_operacion=datadelete.id_persona,
            ip_origen=request.client.host,
            user_agent=1)
        
        return LogEntityRead.from_orm(datadelete)