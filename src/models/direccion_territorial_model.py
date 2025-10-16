from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from src.config.config import Base
from src.models.audit_mixin import AuditMixin
"""
Modelo que representa las direcciones territoriales del sistema.
Contiene información sobre la región, estado y trazabilidad del registro.
Incluye campos de auditoría, el registro del creador (id_persona) y relación con Persona.
"""
class DireccionTerritorial(AuditMixin, Base):
    __tablename__ = "direcciones_territoriales"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True, comment="Identificador único de la dirección territorial")
    nombre = Column(String(255), unique=True, nullable=False, comment="Nombre de la dirección territorial")
    region = Column(String(100), nullable=True, comment="Región geográfica a la que pertenece")
        
    # Relaciones ORM
    persona = relationship("Persona", back_populates="direcciones_territoriales")
    proyectos = relationship("Proyecto", back_populates="direccion_territorial")

    def __repr__(self):
        return f"<DireccionTerritorial(id={self.id}, nombre='{self.nombre}', activo={self.activo})>"
