# src/models/clasificacion_proyecto_model.py
from sqlalchemy import Column, Integer, String, Index
from sqlalchemy.orm import relationship
from src.config.config import Base
from src.models.audit_mixin import AuditMixin

"""
Modelo que representa las clasificaciones de proyecto.
Ejemplo: Suelo Urbano, Suelo Suburbano, Suelo Rural.
"""
class ClasificacionProyecto(AuditMixin, Base):
    __tablename__ = "clasificaciones_proyecto"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True, comment="Identificador único de la clasificación")
    nombre = Column(String(50), nullable=False, unique=True, comment="Clasificación: Suelo Urbano, Suelo Suburbano, Suelo Rural")

    #relaciones
    persona = relationship("Persona", back_populates="clasificaciones_proyecto")
    proyectos = relationship("Proyecto", back_populates="clasificacion")
    
    __table_args__ = (
        Index("idx_clasificaciones_proyecto_nombre", "nombre"),
    )

