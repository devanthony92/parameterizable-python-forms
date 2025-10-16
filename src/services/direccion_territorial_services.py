from fastapi import HTTPException, Request, status
from sqlalchemy.orm import Session
from datetime import datetime, timezone
from src.models.direccion_territorial_model import DireccionTerritorial
from src.schemas.direccion_territorial_schema import DireccionTerritorialCreate, LogEntityRead, DireccionTerritorialUpdate
from src.utils.logs_util import registrar_log, LogUtil
from src.models.logs_model import TipoOperacionEnum
from typing import Optional, Dict, Any

# Servicis CRUD para la direccion territorial
class DireccionTerritorialService:

    def __init__(self, db: Session):
        self.db = db

    def _base_query(self):
        """Base query que excluye eliminados (soft delete)."""
        return self.db.query(DireccionTerritorial).filter(DireccionTerritorial.deleted_at.is_(None))
    
    def get(self, payload: Dict[str, Any], is_active: Optional[bool] = None) -> Optional[DireccionTerritorial]:
        """
        Busca el primer registro que cumpla filtros del payload.
        payload: dict de campo:valor, e.g. {"id": 1} o {"nombre": "Zona Norte"}
        """
        query = self._base_query()
        for field, value in payload.items():
            if hasattr(DireccionTerritorial, field) and value is not None:
                query = query.filter(getattr(DireccionTerritorial, field) == value)
        if is_active is not None:
            query = query.filter(DireccionTerritorial.activo == is_active)
        return query.first()

    def list_direccion_territorial(self, skip: int, limit: int):
        return self._base_query().filter(DireccionTerritorial.activo == True).offset(skip).limit(limit).all()
    
    def count_direccion_territorial(self):
        return self._base_query().filter(DireccionTerritorial.activo == True).count()

    async def create_direccion_territorial(self, payload: DireccionTerritorialCreate,
                                           request: Request, tokenpayload: dict):

        #validamos que no exista un registro con el misno nombre
        existing = self.get({"nombre" : payload.nombre})
        if existing:
            raise HTTPException(status_code=status.HTTP_304_NOT_MODIFIED, detail="La unidad ejecutora ya existe")

        entity = DireccionTerritorial(nombre = payload.nombre.strip(),
                                      region = payload.region,
                                      id_persona = tokenpayload.get("sub"),
                                      activo = True,
                                      created_at = datetime.now(timezone.utc)) 

        try:
            self.db.add(entity)
            self.db.commit()
            self.db.refresh(entity)
        except Exception as e:
            self.db.rollback()
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                                detail=f"Error guardando la Direccion Territorial: {e}")

        try:
            registrar_log(LogUtil(self.db),
                tabla_afectada="direcciones_territoriales",
                id_registro_afectado=entity.id,
                tipo_operacion=TipoOperacionEnum.INSERT.value,
                datos_nuevos=LogEntityRead.from_orm(entity).model_dump(mode="json"),
                datos_viejos=None,
                id_persona_operacion=entity.id_persona,
                ip_origen=request.client.host, 
                user_agent=1)   #user_agent=request.headers.get("user-agent", "unknown"))
        
        except Exception:
            pass
            
        return LogEntityRead.from_orm(entity)
                    
    async def read_direccion_territorial(self, id: int):
        if id is None:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail="El campo id de la unidad ejecutora se encuentra vacío; ingresa un dato válido")

        entity = self.get({"id": id}, is_active=True)
        if not entity:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="La unidad ejecutora no fue hallada")
        return entity

    async def update_direccion_territorial(self, id: int, payload: DireccionTerritorialUpdate, 
                                           request: Request, tokenpayload: dict): 
        
        #validamos que el nombre no este previamente registrado en el sistema
        existe = self.db.query(DireccionTerritorial).filter(
            DireccionTerritorial.nombre == payload.nombre,
            DireccionTerritorial.id != id,
            DireccionTerritorial.deleted_at.is_(None)
        ).first()
        if existe:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail=f"El nombre '{payload.nombre}' ya está siendo usado en otra Direccion Territorial.")

        dataUpdate = self.get({"id": id}, is_active = True)
        if not dataUpdate:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="La Direccion Territorial no fue hallada")
        
        dataOld = LogEntityRead.from_orm(dataUpdate).model_dump(mode="json")

        for field, value in payload.model_dump(exclude_unset=True).items():
            setattr(dataUpdate, field, value)

        dataUpdate.id_persona = tokenpayload.get("sub")
        print(dataUpdate)
        try:
            self.db.add(dataUpdate)
            self.db.commit()
            self.db.refresh(dataUpdate)
        except Exception as e:
            self.db.rollback()
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                                detail=f"Error actualizando la Direccion Territorial: {e}")
        
        # Registro de logs
        try:
            registrar_log(LogUtil(self.db),
                tabla_afectada="direcciones_territoriales",
                id_registro_afectado=dataUpdate.id,
                tipo_operacion=TipoOperacionEnum.UPDATE.value,
                datos_nuevos=LogEntityRead.from_orm(dataUpdate).model_dump(mode="json"),
                datos_viejos=dataOld,
                id_persona_operacion=dataUpdate.id_persona,
                ip_origen=request.client.host,
                user_agent=1)   #user_agent=request.headers.get("user-agent", "unknown"))
        
        except Exception:
            pass

        return LogEntityRead.from_orm(dataUpdate)    
    
    async def delete_direccion_territorial(self, id: int, request: Request, tokenpayload: dict):
        dataDelete = self.get({"id": id}, is_active = True)

        if not dataDelete:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail="La Direccion Territorial no fue hallada")
        
        dataOld = LogEntityRead.from_orm(dataDelete).model_dump(mode="json")

        # le paso un valor false para realizar un sofdelete para un eliminado logico
        dataDelete.activo = False
        dataDelete.deleted_at = datetime.now(timezone.utc)
        dataDelete.id_persona = tokenpayload.get("sub")

        # guardar los cambios
        try:
            self.db.add(dataDelete)
            self.db.commit()
            self.db.refresh(dataDelete)
        except Exception as e:
            self.db.rollback()
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                                detail=f"Error eliminando la Direccion Territorial: {e}")
        # registrar los Logs
        try:
            registrar_log(LogUtil(self.db),
                tabla_afectada="direcciones_territoriales",
                id_registro_afectado=dataDelete.id,
                tipo_operacion=TipoOperacionEnum.DELETE.value,
                datos_nuevos=LogEntityRead.from_orm(dataDelete).model_dump(mode="json"),
                datos_viejos=dataOld,
                id_persona_operacion=dataDelete.id_persona,
                ip_origen=request.client.host,
                user_agent=1)   #user_agent=request.headers.get("user-agent", "unknown"))
        except Exception:
            pass

        return LogEntityRead.from_orm(dataDelete)
    