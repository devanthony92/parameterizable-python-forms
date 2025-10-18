# src/models/modo_transporte_model.py
from sqlalchemy import Column, Integer, String, Index
from sqlalchemy.orm import relationship
from src.config.config import Base
from src.models.audit_mixin import AuditMixin

"""
Modelo que representa los modos de transporte.
Ejemplo: Carretero, Marítimo, Fluvial, Férreo, Intermodal.
"""
class ModoTransporte(AuditMixin, Base):
    __tablename__ = "modos_transporte"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True, comment="Identificador único del modo de transporte")
    nombre = Column(String(50), nullable=False, unique=True, comment="Modo: Carretero, Marítimo, Fluvial, Férreo, Intermodal")

    #relaciones 
    persona = relationship("Persona", back_populates="modos_transporte")
    proyectos = relationship("Proyecto", back_populates="modo_transporte")
    
    __table_args__ = (
        Index("idx_modos_transporte_nombre", "nombre"),
    )

