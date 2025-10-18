# src/models/tramo_sector_model.py
from sqlalchemy import Column, Integer, String, DECIMAL, ForeignKey, Boolean, Index
from sqlalchemy.orm import relationship
from src.config.config import Base
from src.models.audit_mixin import AuditMixin

"""
Modelo que representa los tramos o sectores viales.
Cada tramo pertenece a una ruta y contiene información de kilometraje y trazabilidad.
"""
class TramoSector(AuditMixin, Base):
    __tablename__ = "tramos_sectores"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True, comment="Identificador único del tramo o sector")
    id_ruta = Column(Integer, ForeignKey("rutas.id"), nullable=True, comment="Ruta a la que pertenece el tramo")
    nombre = Column(String(255), nullable=False, comment="Nombre del tramo o sector")
    kilometraje_inicial = Column(DECIMAL(10, 3), nullable=True, comment="Kilometraje inicial del tramo")
    kilometraje_final = Column(DECIMAL(10, 3), nullable=True, comment="Kilometraje final del tramo")

    # Relación con Ruta
    ruta = relationship("Ruta", back_populates="tramos_sectores")
    persona = relationship("Persona", back_populates="tramos_sectores")
    proyectos = relationship("Proyecto", back_populates="tramo_sector")

    __table_args__ = (
        Index("idx_tramos_sectores_nombre", "nombre"),
        Index("idx_tramos_sectores_id_ruta", "id_ruta"),
    )

