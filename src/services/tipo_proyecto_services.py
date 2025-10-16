# src/services/tipo_proyecto_services.py
from fastapi import HTTPException, Request, status
from sqlalchemy.orm import Session
from datetime import datetime, timezone
from typing import Optional, Dict, Any
from src.models.tipo_proyecto_model import TipoProyecto
from src.schemas.tipo_proyecto_schema import TipoProyectoCreate, TipoProyectoUpdate, LogEntityRead
from src.utils.logs_util import registrar_log, LogUtil
from src.models.logs_model import TipoOperacionEnum

class TipoProyectoService:
    def __init__(self, db: Session):
        self.db = db

    def _base_query(self):
        return self.db.query(TipoProyecto).filter(TipoProyecto.deleted_at.is_(None))

    def get(self, payload: Dict[str, Any], is_active: Optional[bool] = None):
        query = self._base_query()
        for field, value in payload.items():
            if hasattr(TipoProyecto, field) and value is not None:
                query = query.filter(getattr(TipoProyecto, field) == value)
        if is_active is not None:
            query = query.filter(TipoProyecto.activo == is_active)
        return query.first()

    def list_tipos_proyecto(self, skip: int, limit: int):
        return self._base_query().filter(TipoProyecto.activo == True).offset(skip).limit(limit).all()

    def count_tipos_proyecto(self):
        return self._base_query().filter(TipoProyecto.activo == True).count()

    async def create_tipo_proyecto(self, payload: TipoProyectoCreate, request: Request, tokenpayload: dict):
        
        #validamos que los datos ingresados no esten vacios
        if not payload.nombre or payload.nombre.strip() == "":
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="El nombre del tipo de proyecto no puede estar vacío")
        if len(payload.nombre) > 50:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail="El campo nombre no puede tener un rango mayor a 50 caracteres")
        
        #validamos que no exista un registro con el misno nombre
        existing = self.db.query(TipoProyecto).filter(
            TipoProyecto.nombre == payload.nombre.strip(),
            TipoProyecto.deleted_at.is_(None)
        ).first()
        if existing:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Ya existe un tipo de proyecto con ese nombre")

        entity = TipoProyecto(
            nombre=payload.nombre.strip(),
            requiere_licencia=payload.requiere_licencia or False,
            id_persona=tokenpayload.get("sub"),
            activo=True,
        )

        try:
            self.db.add(entity)
            self.db.commit()
            self.db.refresh(entity)
        except Exception as e:
            self.db.rollback()
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Error creando el tipo de proyecto: {e}")

        registrar_log(LogUtil(self.db),
            tabla_afectada="tipos_proyecto",
            id_registro_afectado=entity.id,
            tipo_operacion=TipoOperacionEnum.INSERT.value,
            datos_nuevos=LogEntityRead.from_orm(entity).model_dump(mode="json"),
            datos_viejos=None,
            id_persona_operacion=entity.id_persona,
            ip_origen=request.client.host,
            user_agent=1)   #user_agent=request.headers.get("user-agent", "unknown"))

        return LogEntityRead.from_orm(entity)

    async def read_tipo_proyecto(self, id: int):
        entity = self.get({"id": id}, is_active=True)
        if not entity:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="El tipo de proyecto no fue hallado")
        return entity

    async def update_tipo_proyecto(self, id: int, payload: TipoProyectoUpdate, request: Request, tokenpayload: dict):

        #buscamos el registro que se va a actualizar
        data = self.get({"id": id}, is_active=True)
        if not data:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="El tipo de proyecto no fue hallado")

        #guardamos los datos antiguos
        old_data = LogEntityRead.from_orm(data).model_dump(mode="json")

        #verificamos que el nombre no este siendo utilizado en otro tipo de proyecto
        if payload.nombre and payload.nombre.strip() != data.nombre:
            duplicate = self.db.query(TipoProyecto).filter(
                TipoProyecto.nombre == payload.nombre.strip(),
                TipoProyecto.id != id
            ).first()
            if duplicate:
                raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Ya existe otro tipo de proyecto con ese nombre")

        #actualizamos los datos
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
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Error actualizando el tipo de proyecto: {e}")

        #guardamos los logs
        registrar_log(LogUtil(self.db),
            tabla_afectada="tipos_proyecto",
            id_registro_afectado=data.id,
            tipo_operacion=TipoOperacionEnum.UPDATE.value,
            datos_nuevos=LogEntityRead.from_orm(data).model_dump(mode="json"),
            datos_viejos=old_data,
            id_persona_operacion=data.id_persona,
            ip_origen=request.client.host,
            user_agent=request.headers.get("user-agent", "unknown"))

        return LogEntityRead.from_orm(data)

    async def delete_tipo_proyecto(self, id: int, request: Request, tokenpayload: dict):

        #buscamos el registro que se va a eliminar
        data = self.get({"id": id}, is_active=True)
        if not data:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="El tipo de proyecto no fue hallado")

        #guardamos los datos antiguos
        old_data = LogEntityRead.from_orm(data).model_dump(mode="json")

        #se realiza un soft delete pasando el campo activo a false y agregando la hora actual al campo deleted_at
        data.activo = False
        data.deleted_at = datetime.now(timezone.utc)
        data.id_persona = tokenpayload.get("sub")

        #se desactiva el registro de la base de datos
        try:
            self.db.add(data)
            self.db.commit()
            self.db.refresh(data)
        except Exception as e:
            self.db.rollback()
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Error eliminando el tipo de proyecto: {e}")

        registrar_log(LogUtil(self.db),
            tabla_afectada="tipos_proyecto",
            id_registro_afectado=data.id,
            tipo_operacion=TipoOperacionEnum.DELETE.value,
            datos_nuevos=LogEntityRead.from_orm(data).model_dump(mode="json"),
            datos_viejos=old_data,
            id_persona_operacion=data.id_persona,
            ip_origen=request.client.host,
            user_agent=request.headers.get("user-agent", "unknown"))

        return LogEntityRead.from_orm(data)
