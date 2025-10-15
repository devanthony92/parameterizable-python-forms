from fastapi import APIRouter, Depends, Query, Request
from sqlalchemy.orm import Session
from typing import Dict, Any
from src.config.config import get_session
from src.utils.jwt_validator_util import verify_jwt_token
from src.services.direccion_territorial_services import DireccionTerritorialService
from src.schemas.direccion_territorial_schema import DireccionTerritorialCreate

# inicializacion del roter
router = APIRouter()

# endpoint para crear nuevo registro
@router.post("/")
async def create_unidades(request: Request, payload: DireccionTerritorialCreate,
                          dbs: list[Session] = Depends(lambda: next(get_session())), # de esta manera llamo todas las bases de datos existentes
                          tokenpayload: dict = Depends(verify_jwt_token)):
    
    # crear registro con una BD y esta dependencia se agregaria asi => db: Session = Depends(lambda: next(get_session(0)))
    # return await UnidadEjecutoraService(db).create_unidad(payload, request, tokenpayload)
    data = []
    for db in dbs:
        result = await DireccionTerritorialService(db).create_direccion_territorial(payload, request, tokenpayload)
        data.append(result)

    return {"data": data[0]}
