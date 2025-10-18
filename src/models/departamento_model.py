from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from src.config.config import Base
from src.models.audit_mixin import AuditMixin

class Departamento(AuditMixin, Base):
    __tablename__ = "departamentos"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True, comment="Identificador único del departamento")
    nombre = Column(String(100), nullable=False, unique=True, comment="Nombre del departamento")
    codigo_dane = Column(String(5), nullable=True, comment="Código DANE del departamento")
    
    #relaciones
    municipios = relationship("Municipio", back_populates="departamento")
    persona = relationship("Persona", back_populates="departamento")
