from fastapi import APIRouter, Depends, Query, Request
from sqlalchemy.orm import Session
from typing import Dict, Any

from src.config.config import get_session
from src.services.categorizacion_carretera_services import CategorizacionService
from src.schemas.categorizacion_carretera_schema import (CategorizacionCarreteraListResponse,
                                                         CategorizacionCarreteraCreate,
                                                         CategorizacionCarreteraUpdate,
                                                         CategorizacionCarreteraResponse,
                                                         LogEntityRead)
from src.utils.jwt_validator_util import verify_jwt_token

# inicializacion del roter
router = APIRouter()

# endpoint de listar data con paginacion incluida
@router.get("/", response_model=CategorizacionCarreteraListResponse, summary="Listar categorizaciones de carretera")
def lista(
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=200),
    # de esta manera llamo solamente la primera base de datos
    db: Session = Depends(lambda: next(get_session(0))),
    tokenpayload: dict = Depends(verify_jwt_token)
) -> Dict[str, Any]:
    data = CategorizacionService(db).list_categorizacion(skip=skip, limit=limit)
    total = CategorizacionService(db).count_categorizacion()  
    # Método adicional para contar todos los datos
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
    
    # endpoin de crear registro

@router.post("/", response_model=CategorizacionCarreteraResponse, summary="Crear una nueva categorización de carretera")
async def creates(request: Request, 
                        payload: CategorizacionCarreteraCreate, 
                        # de esta manera llamo todas las bases de datos existentes
                        dbs: list[Session] = Depends(lambda: next(get_session())),
                        tokenpayload: dict = Depends(verify_jwt_token)):
    
    # crear registrro con uan BD y esta dependencia se agregaria asi 
    # => db: Session = Depends(lambda: next(get_session(0)))
    # return await UnidadEjecutoraService(db).create_unidad(payload, request, tokenpayload)
    
    data = []
    
    for db in dbs:
        result = await CategorizacionService(db).create_categorizacion(payload, request, tokenpayload)
        data.append(result)

    return data[0]


# endpoint de show o ver registro
@router.get("/{categorizacion_id}", response_model=CategorizacionCarreteraResponse, summary="Ver una categorización de carretera por ID")
async def get_show(categorizacion_id: int, db: Session = Depends(lambda: next(get_session(0)))):
    return await CategorizacionService(db).show(categorizacion_id)


# endpoin para actualizar un registro x
@router.put("/{categorizacion_id}", response_model=CategorizacionCarreteraResponse, summary="Actualizar una categorización de carretera por ID")
async def update(request: Request, 
                        categorizacion_id: int,
                        payload: CategorizacionCarreteraUpdate,
                        # de esta manera llamo todas las bases de datos existentes
                        dbs: list[Session] = Depends(lambda: next(get_session())),
                        tokenpayload: dict = Depends(verify_jwt_token)):

# crear registrro con uan BD y esta dependencia se agregaria asi 
# => db: Session = Depends(lambda: next(get_session(0)))
    # return await UnidadEjecutoraService(db).create_unidad(payload, request, tokenpayload)
    
    
    data = []
    
    for db in dbs:
        result = await CategorizacionService(db).update_categorizacion(categorizacion_id, payload, request, tokenpayload)
        data.append(result)
    
    return data[0]


# endpoint para eliminar un registro logicamente
@router.delete("/{categorizacion_id}", response_model=LogEntityRead, summary="Eliminar una categorización de carretera por ID")
async def delete(request: Request, 
                        categorizacion_id: int, 
                        # de esta manera llamo todas las bases de datos existentes
                        dbs: list[Session] = Depends(lambda: next(get_session())),
                        tokenpayload: dict = Depends(verify_jwt_token)):
    
    data = []
    for db in dbs:
        result = await CategorizacionService(db).delete_categorizacion(categorizacion_id, request, tokenpayload)
        data.append(result)
    
    return data[0]
