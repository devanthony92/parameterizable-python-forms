from fastapi import HTTPException, Request, status
from sqlalchemy.orm import Session
from datetime import datetime, timezone
from typing import Optional, Dict, Any
from src.models.proyecto_model import Proyecto
from src.schemas.proyecto_schema import ProyectoCreate, ProyectoUpdate, LogEntityRead
from src.utils.logs_util import registrar_log, LogUtil
from src.models.logs_model import TipoOperacionEnum

class ProyectoService:
    def __init__(self, db: Session):
        self.db = db

    def _base_query(self):
        """Base query que excluye eliminados (soft delete)."""
        return self.db.query(Proyecto).filter(Proyecto.deleted_at.is_(None))

    def get(self, payload: Dict[str, Any], is_active: Optional[bool] = None):
        """
        Busca el primer registro que cumpla filtros del payload.
        payload: dict de campo:valor, e.g. {"id": 1} o {"nombre": "Zona Norte"}
        """
        query = self._base_query()
        for field, value in payload.items():
            if hasattr(Proyecto, field) and value is not None:
                query = query.filter(getattr(Proyecto, field) == value)
        if is_active is not None:
            query = query.filter(Proyecto.activo == is_active)
        return query.first()

    def list_proyectos(self, skip: int, limit: int):
        return self._base_query().filter(Proyecto.activo == True).offset(skip).limit(limit).all()

    def count_proyectos(self):
        return self._base_query().filter(Proyecto.activo == True).count()

    async def create_proyecto(self, payload: ProyectoCreate, request: Request, tokenpayload: dict):

        entity = Proyecto(**payload.model_dump(), id_persona=tokenpayload.get("sub"),
                          activo=True, created_at=datetime.now(timezone.utc))
        
        #guardamos los datos
        try:
            self.db.add(entity)
            self.db.commit()
            self.db.refresh(entity)
        except Exception as e:
            self.db.rollback()
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                                detail=f"Error creando el proyecto: {e}")

        registrar_log(LogUtil(self.db),
            tabla_afectada="proyectos",
            id_registro_afectado=entity.id,
            tipo_operacion=TipoOperacionEnum.INSERT.value,
            datos_nuevos=LogEntityRead.from_orm(entity).model_dump(mode="json"),
            datos_viejos=None,
            id_persona_operacion=entity.id_persona,
            ip_origen=request.client.host,
            user_agent=1)   #user_agent=request.headers.get("user-agent", "unknown"))

        return LogEntityRead.from_orm(entity)

    async def read_proyecto(self, id: int):
        if id is None:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail="El campo id de la unidad ejecutora se encuentra vacío; ingresa un dato válido")

        entity = self.get({"id": id}, is_active=True)
        print(entity)
        if not entity:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail="El proyecto no fue hallado")
        return entity

    async def update_proyecto(self, id: int, payload: ProyectoUpdate, request: Request, tokenpayload: dict):

        #buscamos el registro que se va a actualizar
        data = self.get({"id": id}, is_active=True)
        if not data:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail="El proyecto no fue hallado")

        data_old = LogEntityRead.from_orm(data).model_dump(mode="json")

        for field, value in payload.model_dump(exclude_unset=True).items():
            setattr(data, field, value)

        data.id_persona = tokenpayload.get("sub")
        data.updated_at = datetime.now(timezone.utc)

        #guardamos los datos
        try:
            self.db.add(data)
            self.db.commit()
            self.db.refresh(data)
        except Exception as e:
            self.db.rollback()
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                                detail=f"Error actualizando el proyecto: {e}")

        #guardamos los logs
        registrar_log(LogUtil(self.db),
            tabla_afectada="proyectos",
            id_registro_afectado=data.id,
            tipo_operacion=TipoOperacionEnum.UPDATE.value,
            datos_nuevos=LogEntityRead.from_orm(data).model_dump(mode="json"),
            datos_viejos=data_old,
            id_persona_operacion=data.id_persona,
            ip_origen=request.client.host,
            user_agent=request.headers.get("user-agent", "unknown"))

        return LogEntityRead.from_orm(data)

    async def delete_proyecto(self, id: int, request: Request, tokenpayload: dict):
        data = self.get({"id": id}, is_active=True)
        if not data:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail="El proyecto no fue hallado")

        data_old = LogEntityRead.from_orm(data).model_dump(mode="json")
        data.activo = False
        data.deleted_at = datetime.now(timezone.utc)
        data.id_persona = tokenpayload.get("sub")

        try:
            self.db.add(data)
            self.db.commit()
            self.db.refresh(data)
        except Exception as e:
            self.db.rollback()
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                                detail=f"Error eliminando el proyecto: {e}")

        registrar_log(LogUtil(self.db),
            tabla_afectada="proyectos",
            id_registro_afectado=data.id,
            tipo_operacion=TipoOperacionEnum.DELETE.value,
            datos_nuevos=LogEntityRead.from_orm(data).model_dump(mode="json"),
            datos_viejos=data_old,
            id_persona_operacion=data.id_persona,
            ip_origen=request.client.host,
            user_agent=request.headers.get("user-agent", "unknown"))

        return LogEntityRead.from_orm(data)
