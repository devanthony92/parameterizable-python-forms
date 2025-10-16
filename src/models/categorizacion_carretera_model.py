# src/models/categorizacion_carretera_model.py
from sqlalchemy import Column, Integer, String, Index
from sqlalchemy.orm import relationship
from src.config.config import Base
from src.models.audit_mixin import AuditMixin

"""
Modelo que representa las categorizaciones de carreteras.
Ejemplo: Construcción, Rehabilitación, Mejoramiento, Mantenimiento, etc.
"""
class CategorizacionCarretera(AuditMixin, Base):
    __tablename__ = "categorizaciones_carreteras"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True, comment="Identificador único de la categorización")
    nombre = Column(String(100), nullable=False, unique=True, comment="Categorización: Construcción, Rehabilitación, Mejoramiento, Mantenimiento, etc.")

    #relaciones 
    persona = relationship("Persona", back_populates="categorizaciones_carreteras")
    proyectos = relationship("Proyecto", back_populates="categorizacion")

    __table_args__ = (
        Index("idx_categorizaciones_carreteras_nombre", "nombre"),
    )

    def __repr__(self):
        return f"<CategorizacionCarretera(id={self.id}, nombre='{self.nombre}', activo={self.activo})>"
