from fastapi import HTTPException, Request, status
from sqlalchemy.orm import Session
from datetime import datetime
from src.models.direccion_territorial_model import DireccionTerritorial
from src.schemas.direccion_territorial_schema import DireccionTerritorialCreate, LogEntityRead
from src.utils.logs_util import registrar_log, LogUtil
from src.models.logs_model import TipoOperacionEnum

# Servicis CRUD para la direccion territorial
class DireccionTerritorialService:
    def __init__(self, db: Session):
        self.db = db

    async def create_direccion_territorial(self, payload: DireccionTerritorialCreate,
                                           request: Request, tokenpayload: dict ):
        checkDirection = self.db.query(DireccionTerritorial).filter(
            DireccionTerritorial.nombre == payload.nombre,
                DireccionTerritorial.activo == True).first()
        if checkDirection:
            return HTTPException(status_code=status.HTTP_304_NOT_MODIFIED, detail="La unidad ejecutora ya existe")
        if payload.nombre =="":
            return HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="El campo nombre de la unidad ejecutora se encuentra vacia ingresa un dato valido")
        if len(payload.nombre) > 255:
            return HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="El campo nombre no puede tener un rango mayor a 255 caracteres")

        entity = DireccionTerritorial(nombre = payload.nombre, region = payload.region,
                                id_persona = tokenpayload.get("sub"), activo=True, created_at=datetime.utcnow()) #
        self.db.add(entity)
        self.db.commit()
        self.db.refresh(entity)

        registrar_log(LogUtil(self.db),
            tabla_afectada="direccion_territorial",
            id_registro_afectado=entity.id,
            tipo_operacion=TipoOperacionEnum.INSERT.value,
            datos_nuevos=LogEntityRead.from_orm(entity).model_dump(mode="json"),
            datos_viejos=None,
            id_persona_operacion=entity.id_persona,
            ip_origen=request.client.host,
            user_agent=1)
        
        return LogEntityRead.from_orm(entity)
        
         