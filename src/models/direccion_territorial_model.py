# src/models/direccion_territorial.py
from sqlalchemy import Column, Integer, String, Boolean, TIMESTAMP, ForeignKey
from sqlalchemy.sql import func
from src.config.config import Base

class DireccionTerritorial(Base):
    __tablename__ = "direcciones_territoriales"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True, comment="Identificador único de la dirección territorial")
    nombre = Column(String(255), unique=True, nullable=False, comment="Nombre de la dirección territorial")
    region = Column(String(100), nullable=True, comment="Región geográfica a la que pertenece")
    id_persona = Column(Integer, ForeignKey("personas.id"), nullable=True, comment="ID de la persona que creó o modificó el registro")
    activo = Column(Boolean, nullable=False, default=True, comment="Indica si el registro está activo (true) o inactivo (false)")
    
    # Campos de auditoria
    created_at = Column(TIMESTAMP(timezone=True), server_default=func.now(), nullable=False, comment="Fecha y hora de creación del registro")
    updated_at = Column(TIMESTAMP(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False, comment="Fecha y hora de última actualización del registro")
    deleted_at = Column(TIMESTAMP(timezone=True), nullable=True, comment="Fecha y hora de eliminación lógica del registro (soft delete)")
    