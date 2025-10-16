from sqlalchemy import Column, TIMESTAMP, Integer, ForeignKey, Boolean
from sqlalchemy.sql import func
from sqlalchemy.ext.declarative import declared_attr

class AuditMixin:
    activo = Column(Boolean, nullable=False, default=True, index=True, comment="Indica si el registro está activo (true) o inactivo (false)")
    created_at = Column(TIMESTAMP(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(TIMESTAMP(timezone=True), onupdate=func.now())
    deleted_at = Column(TIMESTAMP(timezone=True))

    @declared_attr
    def id_persona(cls):
        return Column(Integer, ForeignKey("personas.id"), nullable=True, comment="ID de la persona que creó o modificó el registro")