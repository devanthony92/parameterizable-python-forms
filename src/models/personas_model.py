from sqlalchemy import Column, Integer, String, TIMESTAMP, Boolean, func,  ForeignKey, Index
from sqlalchemy.orm import relationship
from src.config.config import Base
from src.models.audit_mixin import AuditMixin
"""
Modelo que representa las direcciones territoriales del sistema.
Contiene información sobre la región, estado y trazabilidad del registro.
"""
class Persona(AuditMixin, Base):
    __tablename__ = "personas"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True, comment="Identificador único de la unidad ejecutora")
    nombre_completo = Column(String(255), nullable=False, comment="Nombre completo de la persona")
    cedula = Column(String(20), unique=True, index=True, comment="Número de cédula de ciudadanía")
    email = Column(String(255), unique=True, index=True, comment="Correo electrónico válido con formato @dominio")
    telefono = Column(String(20), nullable=True, comment="Número de teléfono celular (10 dígitos)")
    id_persona = Column(Integer, ForeignKey("personas.id"), nullable=True, comment="ID de la persona que creó o modificó el registro")
    activo = Column(Boolean, nullable=False, default=True, comment="Indica si el registro está activo (true) o inactivo (false)")
    
    #relaciones
    direcciones_territoriales = relationship("DireccionTerritorial", back_populates="persona")

    __table_args__ = (
        Index("idx_personas_cedula", "cedula"),
        Index("idx_personas_email", "email"),
    )
