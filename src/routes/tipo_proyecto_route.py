from fastapi import APIRouter, Depends, Query, Request
from sqlalchemy.orm import Session
from typing import Dict, Any
from src.config.config import get_session
from src.utils.jwt_validator_util import verify_jwt_token
from src.services.tipo_proyecto_services import TipoProyectoService
from src.schemas.tipo_proyecto_schema import (
    TipoProyectoListResponse,
    TipoProyectoCreate,
    TipoProyectoUpdate,
    TipoProyectoResponse,
    LogEntityRead,
)

router = APIRouter()
    

@router.get("/", response_model=TipoProyectoListResponse, summary="Listar tipos de proyecto con paginación")
def listar_tipos_proyecto(skip: int = Query(0, ge=0), limit: int = Query(50, ge=1, le=200),
                          db: Session = Depends(lambda: next(get_session(0))),
                          tokenpayload: dict = Depends(verify_jwt_token)) -> Dict[str, Any]:
    
    service = TipoProyectoService(db)
    data = service.list_tipos_proyecto(skip, limit)
    total = service.count_tipos_proyecto()
    return {
        "data": data,
        "pagination": {
            "skip": skip,
            "limit": limit,
            "total": total,
            "page": (skip // limit) + 1,
            "pages": (total + limit - 1) // limit,
        },
    }

@router.post("/", response_model=TipoProyectoResponse, summary="Crear tipo de proyecto")
async def create_tipo_proyecto(request: Request, payload: TipoProyectoCreate,
                               dbs: list[Session] = Depends(lambda: next(get_session())), # de esta manera llamo todas las bases de datos existentes
                               tokenpayload: dict = Depends(verify_jwt_token)):
    
    # crear registro con una BD y esta dependencia se agregaria asi => db: Session = Depends(lambda: next(get_session(0)))
    data = []
    for db in dbs:
        result = await TipoProyectoService(db).create_tipo_proyecto(payload, request, tokenpayload)
        data.append(result)

    return data[0]      #{"data": data[0]}

@router.get("/{id}", response_model=TipoProyectoResponse, summary="Obtener tipo de proyecto por ID")
async def read_tipo_proyecto(id: int,
                             dbs: list[Session] = Depends(lambda: next(get_session())), # de esta manera llamo todas las bases de datos existentes
                             tokenpayload: dict = Depends(verify_jwt_token)):
    
    # crear registro con una BD y esta dependencia se agregaria asi => db: Session = Depends(lambda: next(get_session(0)))
    data = []
    for db in dbs:
        result = await TipoProyectoService(db).read_tipo_proyecto(id)
        data.append(result)

    return data[0]      #{"data": data[0]}

@router.put("/{id}", response_model=TipoProyectoResponse, summary="Actualizar tipo de proyecto")
async def update_tipo_proyecto(id: int, request: Request, payload: TipoProyectoUpdate,
                               dbs: list[Session] = Depends(lambda: next(get_session())),
                               tokenpayload: dict = Depends(verify_jwt_token)):
    
    # crear registro con una BD y esta dependencia se agregaria asi => db: Session = Depends(lambda: next(get_session(0)))
    data = []
    for db in dbs:
        result = await TipoProyectoService(db).update_tipo_proyecto(id, payload, request, tokenpayload)
        data.append(result)

    return data[0]

@router.delete("/{id}", response_model=LogEntityRead, summary="Eliminar (soft delete) tipo de proyecto")
async def delete_tipo_proyecto(id: int, request: Request,
                               dbs: list[Session] = Depends(lambda: next(get_session())),
                               tokenpayload: dict = Depends(verify_jwt_token)):
    
    data = []
    for db in dbs:
        result = await TipoProyectoService(db).delete_tipo_proyecto(id, request, tokenpayload)
        data.append(result)

    return data[0]