from sqlalchemy import Column, Integer, String, Boolean, Index
from src.config.config import Base
from src.models.audit_mixin import AuditMixin

"""
Modelo que representa los tipos de proyecto.
Ejemplo: Licenciado o No licenciado, e indica si requiere licencia ambiental.
"""
class TipoProyecto(AuditMixin, Base):
    __tablename__ = "tipos_proyecto"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True, comment="Identificador único del tipo de proyecto")
    nombre = Column(String(50), unique=True, nullable=False, comment="Tipo de proyecto: Licenciado o No licenciado")
    requiere_licencia = Column(Boolean, nullable=False, default=False, comment="Indica si el tipo requiere licencia ambiental")

    __table_args__ = (
        Index("idx_tipos_proyecto_nombre", "nombre"),
    )

    def __repr__(self):
        return f"<TipoProyecto(id={self.id}, nombre='{self.nombre}', requiere_licencia={self.requiere_licencia}, activo={self.activo})>"
