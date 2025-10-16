from fastapi import HTTPException, Request, status
from sqlalchemy.orm import Session
from datetime import datetime, timezone
from typing import Optional, Dict, Any
from src.models.contrato_model import Contrato
from src.schemas.contrato_schema import ContratoCreate, ContratoUpdate, LogEntityRead
from src.utils.logs_util import registrar_log, LogUtil
from src.models.logs_model import TipoOperacionEnum

class ContratoService:
    def __init__(self, db: Session):
        self.db = db

    def _base_query(self):
        return self.db.query(Contrato).filter(Contrato.deleted_at.is_(None))

    def get(self, payload: Dict[str, Any], is_active: Optional[bool] = None):
        query = self._base_query()
        for field, value in payload.items():
            if hasattr(Contrato, field) and value is not None:
                query = query.filter(getattr(Contrato, field) == value)
        if is_active is not None:
            query = query.filter(Contrato.activo == is_active)
        return query.first()

    def list_contratos(self, skip: int, limit: int):
        return self._base_query().filter(Contrato.activo == True).offset(skip).limit(limit).all()

    def count_contratos(self):
        return self._base_query().filter(Contrato.activo == True).count()

    async def create_contrato(self, payload: ContratoCreate, request: Request, tokenpayload: dict):
        if not payload.numero_contrato or payload.numero_contrato.strip() == "":
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="El número de contrato no puede estar vacío")

        existing = self.get({"numero_contrato": payload.numero_contrato})
        if existing:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Ya existe un contrato con ese número")

        entity = Contrato(
            id_proyecto=payload.id_proyecto,
            numero_contrato=payload.numero_contrato.strip(),
            tipo_contrato=payload.tipo_contrato,
            fecha_contrato=payload.fecha_contrato,
            objeto_contrato=payload.objeto_contrato,
            fecha_inicio=payload.fecha_inicio,
            fecha_terminacion=payload.fecha_terminacion,
            valor_contrato=payload.valor_contrato,
            recursos_sostenibilidad=payload.recursos_sostenibilidad,
            id_persona=tokenpayload.get("sub"),
            activo=True,
            created_at=datetime.now(timezone.utc),
        )

        try:
            self.db.add(entity)
            self.db.commit()
            self.db.refresh(entity)
        except Exception as e:
            self.db.rollback()
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Error creando el contrato: {e}")

        registrar_log(LogUtil(self.db),
            tabla_afectada="contratos",
            id_registro_afectado=entity.id,
            tipo_operacion=TipoOperacionEnum.INSERT.value,
            datos_nuevos=LogEntityRead.from_orm(entity).model_dump(mode="json"),
            datos_viejos=None,
            id_persona_operacion=entity.id_persona,
            ip_origen=request.client.host,
            user_agent=1)    #user_agent=request.headers.get("user-agent", "unknown"))

        return LogEntityRead.from_orm(entity)

    async def read_contrato(self, id: int):
        entity = self.get({"id": id}, is_active=True)
        if not entity:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="El contrato no fue hallado")
        return entity

    async def update_contrato(self, id: int, payload: ContratoUpdate, request: Request, tokenpayload: dict):
        if payload.numero_contrato is not None:
            numero_contrato_str = payload.numero_contrato.strip()
            if numero_contrato_str == "":
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                    detail="El campo numero de contrato se encuentra vacío; ingresa un dato válido")
            if len(numero_contrato_str) > 255:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                    detail="El campo numero de contrato no puede tener un rango mayor a 255 caracteres")

            #validamos que el nombre no este previamente registrado en el sistema
            existe = self.db.query(Contrato).filter(
                Contrato.numero_contrato == numero_contrato_str,
                Contrato.id != id,
                Contrato.deleted_at.is_(None)
            ).first()
            if existe:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                    detail=f"El numero de contrato '{numero_contrato_str}' ya está siendo usado")
        
        data = self.get({"id": id}, is_active=True)
        if not data:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="El contrato no fue hallado")

        old_data = LogEntityRead.from_orm(data).model_dump(mode="json")

        for field, value in payload.model_dump(exclude_unset=True).items():
            setattr(data, field, value)

        data.id_persona = tokenpayload.get("sub")
        data.updated_at = datetime.now(timezone.utc)

        try:
            self.db.add(data)
            self.db.commit()
            self.db.refresh(data)
        except Exception as e:
            self.db.rollback()
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Error actualizando el contrato: {e}")

        registrar_log(LogUtil(self.db),
            tabla_afectada="contratos",
            id_registro_afectado=data.id,
            tipo_operacion=TipoOperacionEnum.UPDATE.value,
            datos_nuevos=LogEntityRead.from_orm(data).model_dump(mode="json"),
            datos_viejos=old_data,
            id_persona_operacion=data.id_persona,
            ip_origen=request.client.host,
            user_agent=request.headers.get("user-agent", "unknown"))

        return LogEntityRead.from_orm(data)

    async def delete_contrato(self, id: int, request: Request, tokenpayload: dict):
        data = self.get({"id": id}, is_active=True)
        if not data:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="El contrato no fue hallado")

        old_data = LogEntityRead.from_orm(data).model_dump(mode="json")

        # le paso un valor false para realizar un sofdelete para un eliminado logico
        data.activo = False
        data.deleted_at = datetime.now(timezone.utc)
        data.id_persona = tokenpayload.get("sub")

        # guardar los cambios
        try:
            self.db.add(data)
            self.db.commit()
            self.db.refresh(data)
        except Exception as e:
            self.db.rollback()
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Error eliminando el contrato: {e}")
        
        # registrar los Logs
        registrar_log(LogUtil(self.db),
            tabla_afectada="contratos",
            id_registro_afectado=data.id,
            tipo_operacion=TipoOperacionEnum.DELETE.value,
            datos_nuevos=LogEntityRead.from_orm(data).model_dump(mode="json"),
            datos_viejos=old_data,
            id_persona_operacion=data.id_persona,
            ip_origen=request.client.host,
            user_agent=1)   #user_agent=request.headers.get("user-agent", "unknown"))

        return LogEntityRead.from_orm(data)
