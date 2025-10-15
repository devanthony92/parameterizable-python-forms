# src/models/direccion_territorial.py
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from src.config.config import Base
from src.models.audit_mixin import AuditMixin

class DireccionTerritorial(AuditMixin, Base):
    __tablename__ = "direcciones_territoriales"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True, comment="Identificador único de la dirección territorial")
    nombre = Column(String(255), unique=True, nullable=False, comment="Nombre de la dirección territorial")
    region = Column(String(100), nullable=True, comment="Región geográfica a la que pertenece")
    id_persona = Column(Integer, ForeignKey("personas.id"), nullable=True, comment="ID de la persona que creó o modificó el registro")
    activo = Column(Boolean, nullable=False, default=True, comment="Indica si el registro está activo (true) o inactivo (false)")
        
    #relacion con la tabla Persona
    persona = relationship("Persona", back_populates="direcciones_territoriales")