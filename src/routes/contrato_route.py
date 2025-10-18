from fastapi import APIRouter, Depends, Query, Request
from sqlalchemy.orm import Session
from typing import Dict, Any

from src.config.config import get_session
from src.utils.jwt_validator_util import verify_jwt_token
from src.services.contrato_services import ContratoService
from src.schemas.contrato_schema import (
    ContratoListResponse,
    ContratoCreate,
    ContratoUpdate,
    ContratoResponse,
    LogEntityRead,
)

router = APIRouter()

@router.get("/", response_model=ContratoListResponse, summary="Listar contratos con paginación")
def listar_contratos(skip: int = Query(0, ge=0), limit: int = Query(50, ge=1, le=200),
                     db: Session = Depends(lambda: next(get_session(0))),
                     tokenpayload: dict = Depends(verify_jwt_token)) -> Dict[str, Any]:
    service = ContratoService(db)
    data = service.list_contratos(skip, limit)
    total = service.count_contratos()
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

@router.post("/", response_model=ContratoResponse, summary="Crear nuevo contrato")
async def create_contrato(request: Request, payload: ContratoCreate,
                          dbs: list[Session] = Depends(lambda: next(get_session())), # de esta manera llamo todas las bases de datos existentes
                          tokenpayload: dict = Depends(verify_jwt_token)):
        # crear registro con una BD y esta dependencia se agregaria asi => db: Session = Depends(lambda: next(get_session(0)))
    # return await UnidadEjecutoraService(db).create_unidad(payload, request, tokenpayload)
    data = []
    for db in dbs:
        result = await ContratoService(db).create_contrato(payload, request, tokenpayload)
        data.append(result)

    return data[0]

@router.get("/{id}", response_model=ContratoResponse, summary="Obtener contrato por ID")
async def read_contrato(id: int, db: Session = Depends(lambda: next(get_session(0))),
                        tokenpayload: dict = Depends(verify_jwt_token)):
    return await ContratoService(db).read_contrato(id)

@router.put("/{id}", response_model=ContratoResponse, summary="Actualizar contrato")
async def update_contrato(id: int, request: Request, payload: ContratoUpdate,
                          dbs: list[Session] = Depends(lambda: next(get_session())), # de esta manera llamo todas las bases de datos existentes
                          tokenpayload: dict = Depends(verify_jwt_token)):
    data = []
    for db in dbs:
        result = await ContratoService(db).update_contrato(id, payload, request, tokenpayload)
        data.append(result)
    return data[0]

@router.delete("/{id}", response_model=LogEntityRead, summary="Eliminar (soft delete) contrato")
async def delete_contrato(id: int, request: Request,
                          dbs: list[Session] = Depends(lambda: next(get_session())), # de esta manera llamo todas las bases de datos existentes
                          tokenpayload: dict = Depends(verify_jwt_token)):    
    data = []
    for db in dbs:
        result = await ContratoService(db).delete_contrato(id, request, tokenpayload)
        data.append(result)
    return data[0]