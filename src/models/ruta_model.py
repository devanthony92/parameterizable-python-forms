# src/models/ruta_model.py
from sqlalchemy import Column, Integer, String, Index
from sqlalchemy.orm import relationship
from src.config.config import Base
from src.models.audit_mixin import AuditMixin

"""
Modelo que representa las rutas viales del sistema.
Incluye información básica como el nombre, código y trazabilidad del registro.
"""
class Ruta(AuditMixin, Base):
    __tablename__ = "rutas"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True, comment="Identificador único de la ruta")
    nombre = Column(String(255), nullable=False, comment="Nombre de la ruta vial")
    codigo = Column(String(20), nullable=True, comment="Código identificador de la ruta")

    # Relación 
    persona = relationship("Persona", back_populates="rutas")
    tramos_sectores = relationship("TramoSector", back_populates="ruta")
    proyectos = relationship("Proyecto", back_populates="ruta")

    __table_args__ = (
        Index("idx_rutas_nombre", "nombre"),
        Index("idx_rutas_codigo", "codigo"),
    )
