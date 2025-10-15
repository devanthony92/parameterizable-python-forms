from fastapi import APIRouter, Depends, Query, Request
from sqlalchemy.orm import Session
from typing import Dict, Any
from src.config.config import get_session
from src.utils.jwt_validator_util import verify_jwt_token
from src.services.direccion_territorial_services import DireccionTerritorialService
from src.schemas.direccion_territorial_schema import DireccionTerritorialListResponse, DireccionTerritorialCreate, DireccionTerritorialUpdate, DireccionTerritorialResponse

# inicializacion del roter
router = APIRouter()

# endpoint para listar los registros con paginacion
@router.get("/", response_model = DireccionTerritorialListResponse)
def listar_direcciones_territoriales(skip: int = Query(0, ge=0),limit: int = Query(50, ge=1, le=200),
                                     db: Session = Depends(lambda: next(get_session(0))),
                                     tokenpayload: dict = Depends(verify_jwt_token)) -> Dict[str, Any]:
    
    data = DireccionTerritorialService(db).list_direccion_territorial(skip,limit)
    total = DireccionTerritorialService(db).count_direccion_territorial()    # Método adicional para contar todos los datos
    return {
        "data": data,
        "pagination": {
            "skip": skip,
            "limit": limit,
            "total": total,
            "page": (skip // limit) + 1,
            "pages": (total + limit - 1) // limit  # Redondeo hacia arriba
        }
    }

# endpoint para crear nuevo registro
@router.post("/")
async def create_direcciones_territoriales(request: Request, payload: DireccionTerritorialCreate,
                          dbs: list[Session] = Depends(lambda: next(get_session())), # de esta manera llamo todas las bases de datos existentes
                          tokenpayload: dict = Depends(verify_jwt_token)):
    
    # crear registro con una BD y esta dependencia se agregaria asi => db: Session = Depends(lambda: next(get_session(0)))
    # return await UnidadEjecutoraService(db).create_unidad(payload, request, tokenpayload)
    data = []
    for db in dbs:
        result = await DireccionTerritorialService(db).create_direccion_territorial(payload, request, tokenpayload)
        data.append(result)

    return {"data": data[0]}

# endpoint para buscar registro por ID
@router.post("/{id}", response_model = DireccionTerritorialResponse)
async def read_direcciones_territoriales(id: int, tokenpayload: dict = Depends(verify_jwt_token),
                                         db: Session = Depends(lambda: next(get_session(0)))):
    return await DireccionTerritorialService(db).read_direccion_territorial(id)

# endpoint para actualizar los datos de un registro
@router.put("/{id}")
async def update_direcciones_territoriales(id: int, request: Request, payload: DireccionTerritorialUpdate,
                                           dbs: list[Session] = Depends(lambda: next(get_session())), # de esta manera llamo todas las bases de datos existentes
                                           tokenpayload: dict = Depends(verify_jwt_token)):

    # crear registrro con uan BD y esta dependencia se agregaria asi => db: Session = Depends(lambda: next(get_session(0)))
    # return await UnidadEjecutoraService(db).create_unidad(payload, request, tokenpayload) 
    data = []
    for db in dbs:
        result = await DireccionTerritorialService(db).update_direccion_territorial(id, payload, request, tokenpayload)
        data.append(result)

    return {"data": data[0]}

# endpoint para eliminar un registro SoftDelete
@router.delete("/{id}")
async def delete_direcciones_territoriales(id: int, request: Request, 
                                           dbs: list[Session] = Depends(lambda: next(get_session())),
                                           tokenpayload: dict = Depends(verify_jwt_token)):

    data = []
    for db in dbs:
        result = await DireccionTerritorialService(db).delete_direccion_territorial(id, request, tokenpayload)
        data.append(result)
    
    return {"data": data[0]}    