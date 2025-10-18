from pydantic import BaseModel

class Paginacion(BaseModel):
    skip: int
    limit: int
    total: int
    page: int
    pages: int