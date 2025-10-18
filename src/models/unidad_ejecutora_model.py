from sqlalchemy import Column, Integer, String, Text
from sqlalchemy.orm import relationship

from src.config.config import Base
from src.models.audit_mixin import AuditMixin
"""
Modelo que representa las unidades ejecutoras relacionadas al proyecto.
"""

class UnidadEjecutora(AuditMixin, Base):
    __tablename__ = "unidades_ejecutoras"

    id = Column(
        Integer,
        primary_key=True,
        index=True,
        autoincrement=True,
        comment="Identificador único de la unidad ejecutora",
    )
    nombre = Column(
        String(255),
        unique=True,
        nullable=False,
        comment="Nombre de la unidad ejecutora",
    )
    descripcion = Column(
        Text, nullable=True, comment="Descripción detallada de la unidad ejecutora"
    )    

    persona = relationship("Persona", back_populates="unidades_ejecutoras")
    proyectos = relationship("Proyecto", back_populates="unidad_ejecutora")

