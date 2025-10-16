# src/models/funcionalidad_carretera_model.py
from sqlalchemy import Column, Integer, String, Index
from sqlalchemy.orm import relationship
from src.config.config import Base
from src.models.audit_mixin import AuditMixin

"""
Modelo que representa las funcionalidades de las carreteras.
Ejemplo: Primaria, Secundaria, Terciaria, Muelle, Puerto, etc.
"""
class FuncionalidadCarretera(AuditMixin, Base):
    __tablename__ = "funcionalidades_carreteras"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True, comment="Identificador único de la funcionalidad")
    nombre = Column(String(50), nullable=False, unique=True, comment="Funcionalidad: Primaria, Secundaria, Terciaria, Muelle, Puerto, etc.")

    # Relación inversa con Proyecto
    persona = relationship("Persona", back_populates="funcionalidades_carreteras")
    proyectos = relationship("Proyecto", back_populates="funcionalidad")

    __table_args__ = (
        Index("idx_funcionalidades_carreteras_nombre", "nombre"),
    )

    def __repr__(self):
        return f"<FuncionalidadCarretera(id={self.id}, nombre='{self.nombre}', activo={self.activo})>"
