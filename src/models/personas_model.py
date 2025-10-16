from sqlalchemy import Column, Integer, String, Index
from sqlalchemy.orm import relationship
from src.config.config import Base
from src.models.audit_mixin import AuditMixin
"""
Modelo que representa las personas registradas en el sistema.
Contiene información personal como nombre completo, cedula, email y telefono.
"""
class Persona(AuditMixin, Base):
    __tablename__ = "personas"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True, comment="Identificador único de la unidad ejecutora")
    nombre_completo = Column(String(255), nullable=False, comment="Nombre completo de la persona")
    cedula = Column(String(20), unique=True, nullable=False, comment="Número de cédula de ciudadanía")
    email = Column(String(255), unique=True, nullable=False, comment="Correo electrónico válido con formato @dominio")
    telefono = Column(String(20), nullable=True, comment="Número de teléfono celular (20 dígitos)")
 
    def __repr__(self):
        return f"<Persona(id={self.id}, nombre='{self.nombre_completo}', cedula='{self.cedula}', email='{self.email}', activo={self.activo})>"
        
    #relaciones
    creado_por = relationship("Persona", remote_side=[id], backref="personas_creadas")
    direcciones_territoriales = relationship("DireccionTerritorial", back_populates="persona")

    __table_args__ = (
        Index("idx_personas_cedula", "cedula",unique=True),
        Index("idx_personas_email", "email",unique=True),
    )
