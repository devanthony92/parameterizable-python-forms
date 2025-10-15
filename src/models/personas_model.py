from sqlalchemy import Column, Integer, String, Text, TIMESTAMP, Boolean, DateTime, func,  ForeignKey, Index
from src.config.config import Base

class Persona(Base):
    __tablename__ = "personas"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True, comment="Identificador único de la unidad ejecutora")
    nombre_completo = Column(String(255), nullable=False, comment="Nombre completo de la persona")
    cedula = Column(String(20), unique=True, index=True, comment="Número de cédula de ciudadanía")
    email = Column(String(255), unique=True, index=True, comment="Correo electrónico válido con formato @dominio")
    telefono = Column(String(20), nullable=True, comment="Número de teléfono celular (10 dígitos)")
    id_persona = Column(Integer, ForeignKey("personas.id"), nullable=True, comment="ID de la persona que creó o modificó el registro")
    activo = Column(Boolean, nullable=False, default=True, comment="Indica si el registro está activo (true) o inactivo (false)")
    
    # Campos de auditoria
    created_at = Column(TIMESTAMP(timezone=True), server_default=func.now(), nullable=False, comment="Fecha y hora de creación del registro")
    updated_at = Column(TIMESTAMP(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False, comment="Fecha y hora de última actualización del registro")
    deleted_at = Column(TIMESTAMP(timezone=True), nullable=True, comment="Fecha y hora de eliminación lógica del registro (soft delete)")
    
    __table_args__ = (
        Index("idx_personas_cedula", "cedula"),
        Index("idx_personas_email", "email"),
    )
