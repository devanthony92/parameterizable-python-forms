from fastapi import APIRouter, Depends, Query, Request
from sqlalchemy.orm import Session
from typing import Dict, Any, Optional
from src.config.config import get_session
from src.utils.jwt_validator_util import verify_jwt_token
from src.services.proyecto_services import ProyectoService
from src.schemas.proyecto_schema import (
    ProyectoListResponse,
    ProyectoCreate,
    ProyectoUpdate,
    ProyectoResponse,
    LogEntityRead,
)

router = APIRouter(prefix="/proyectos", tags=["proyectos"])


# Listar proyectos con paginación
@router.get("/", response_model=ProyectoListResponse, summary="Listar proyectos con paginación")
def listar_proyectos(skip: int = Query(0, ge=0), limit: int = Query(50, ge=1, le=500), 
                     db: Session = Depends(lambda: next(get_session(0))),
                     tokenpayload: dict = Depends(verify_jwt_token)) -> Dict[str, Any]:
    service = ProyectoService(db)
    data = service.list_proyectos(skip, limit)
    total = service.count_proyectos()
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

# Crear nuevo proyecto
@router.post("/", response_model=LogEntityRead, summary="Crear un nuevo proyecto")
async def create_proyecto(request: Request, payload: ProyectoCreate,
    dbs: list[Session] = Depends(lambda: next(get_session())), # de esta manera llamo todas las bases de datos existentes
    tokenpayload: dict = Depends(verify_jwt_token)):
    
    # crear registro con una BD y esta dependencia se agregaria asi => db: Session = Depends(lambda: next(get_session(0)))
    # return await UnidadEjecutoraService(db).create_unidad(payload, request, tokenpayload)
    data = []
    for db in dbs:
        result = await ProyectoService(db).create_proyecto(payload, request, tokenpayload)
        data.append(result)

    return data[0]

# Obtener un proyecto por su ID
@router.get("/{id}", response_model=ProyectoResponse, summary="Obtener un proyecto por ID")
async def read_proyecto(id: int, db: Session = Depends(lambda: next(get_session(0))),
                        tokenpayload: dict = Depends(verify_jwt_token)):
    return await ProyectoService(db).read_proyecto(id)


# Actualizar proyecto existente
@router.put("/{id}", response_model=LogEntityRead, summary="Actualizar un proyecto existente")
async def update_proyecto(id: int, request: Request, payload: ProyectoUpdate,
    dbs: list[Session] = Depends(lambda: next(get_session())), # de esta manera llamo todas las bases de datos existentes
    tokenpayload: dict = Depends(verify_jwt_token)):
    data = []
    for db in dbs:
        result = await ProyectoService(db).update_proyecto(id, payload, request, tokenpayload)
        data.append(result)

    return data[0]

# Eliminar proyecto (soft delete)
@router.delete("/{id}", response_model=LogEntityRead, summary="Eliminar (soft delete) un proyecto")
async def delete_proyecto(id: int, request: Request,
                          dbs: list[Session] = Depends(lambda: next(get_session())), # de esta manera llamo todas las bases de datos existentes
                          tokenpayload: dict = Depends(verify_jwt_token)):
    data = []
    for db in dbs:
        result = await ProyectoService(db).delete_proyecto(id, request, tokenpayload)
        data.append(result)
    return data[0]

