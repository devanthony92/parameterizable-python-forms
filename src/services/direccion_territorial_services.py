from fastapi import HTTPException, Request, status
from sqlalchemy.orm import Session
from datetime import datetime
from src.models.direccion_territorial_model import DireccionTerritorial
from src.schemas.direccion_territorial_schema import DireccionTerritorialCreate, LogEntityRead, DireccionTerritorialUpdate
from src.utils.logs_util import registrar_log, LogUtil
from src.models.logs_model import TipoOperacionEnum

# Servicis CRUD para la direccion territorial
class DireccionTerritorialService:

    def __init__(self, db: Session):
        self.db = db

    #metodo auxiliar get para encontrar registro un campo
    #Ejemplo de uso 
    # # Buscar por nombre: get({"nombre": "Zona Norte"})
    # Buscar por id: get({"id": 3})
    def get(self, payload: dict, is_active: bool = None):      
        query = self.db.query(DireccionTerritorial)
        # Construye filtros dinámicos
        for field, value in payload.items():
            if hasattr(DireccionTerritorial, field) and value is not None:
                query = query.filter(getattr(DireccionTerritorial, field) == value)
        # Siempre filtra por activo
        if is_active is not None:
            query = query.filter(DireccionTerritorial.activo == is_active)

        return query.first()

    def list_direccion_territorial(self, skipt: int, limit: int):
        return self.db.query(DireccionTerritorial).filter(DireccionTerritorial.activo == True).offset(skipt).limit(limit).all()
    
    def count_direccion_territorial(self):
        return self.db.query(DireccionTerritorial).filter(DireccionTerritorial.activo == True).count()

    async def create_direccion_territorial(self, payload: DireccionTerritorialCreate,
                                           request: Request, tokenpayload: dict ):
        checkDirection = self.get({"nombre" : payload.nombre})

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
            tabla_afectada="direcciones_territoriales",
            id_registro_afectado=entity.id,
            tipo_operacion=TipoOperacionEnum.INSERT.value,
            datos_nuevos=LogEntityRead.from_orm(entity).model_dump(mode="json"),
            datos_viejos=None,
            id_persona_operacion=entity.id_persona,
            ip_origen=request.client.host,
            user_agent=1)
        
        return LogEntityRead.from_orm(entity)
                
    async def read_direccion_territorial(self, id: int):
        entity = self.get({"id": id}, is_active=True)
        if not entity:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="La unidad ejecutora no fue hallada")
        if id =="":
            return HTTPException(status_code=status.HTTP_400_BAD_REQUEST, 
                                detail="El campo unidad_id de la unidad ejecutora se encuentra vacia ingresa un dato valido")
        return entity

    async def update_direccion_territorial(self, id: int, payload: DireccionTerritorialUpdate, 
                                           request: Request, tokenpayload: dict): 
        if payload.nombre:
            existe = (
                self.db.query(DireccionTerritorial)
                .filter(DireccionTerritorial.nombre == payload.nombre, DireccionTerritorial.id != id)
                .first()
            )
            if existe:
                return HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"El nombre '{payload.nombre}' ya está siendo usado en otra Direccion Territorial."
                )
        dataUpdate = self.get({"id": id}, is_active = True)
        
        if not dataUpdate:
            return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="La Direccion Territorial no fue hallada")
        if payload.nombre =="":
            return HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="El campo nombre de la Direccion Territorial se encuentra vacia ingresa un dato valido")
        if len(payload.nombre) > 255:
            return HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="El campo nombre no puede tener un rango mayor a 255 caracteres")
        
        dataOld = LogEntityRead.from_orm(dataUpdate).model_dump(mode="json")

        if dataUpdate:
            dataUpdate.nombre = payload.nombre
            dataUpdate.region = payload.region
            dataUpdate.id_persona = tokenpayload.get("sub")
            self.db.commit()
            self.db.refresh(dataUpdate)
        
        # Registro de logs
        registrar_log(LogUtil(self.db),
            tabla_afectada="direcciones_territoriales",
            id_registro_afectado=dataUpdate.id,
            tipo_operacion=TipoOperacionEnum.UPDATE.value,
            datos_nuevos=LogEntityRead.from_orm(dataUpdate).model_dump(mode="json"),
            datos_viejos=dataOld,
            id_persona_operacion=dataUpdate.id_persona,
            ip_origen=request.client.host,
            user_agent=1)
        
        return LogEntityRead.from_orm(dataUpdate)
    
    async def delete_direccion_territorial(self, id: int, request: Request, tokenpayload: dict):
        dataDelete = self.get({"id": id}, is_active = True)

        if not dataDelete:
            return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="La Direccion Territorial no fue hallada")
        
        dataOld = LogEntityRead.from_orm(dataDelete).model_dump(mode="json")
        # le paso un valor false para realizar un sofdelete para un eliminado logico
        dataDelete.activo = False
        dataDelete.deleted_at = datetime.utcnow()
        dataDelete.id_persona = tokenpayload.get("sub")
        # guardar los cambios
        self.db.commit()
        self.db.refresh(dataDelete)

        registrar_log(LogUtil(self.db),
            tabla_afectada="direcciones_territoriales",
            id_registro_afectado=dataDelete.id,
            tipo_operacion=TipoOperacionEnum.DELETE.value,
            datos_nuevos=LogEntityRead.from_orm(dataDelete).model_dump(mode="json"),
            datos_viejos=dataOld,
            id_persona_operacion=dataDelete.id_persona,
            ip_origen=request.client.host,
            user_agent=1)
        
        return LogEntityRead.from_orm(dataDelete)
    