from sqlalchemy import Column, Integer, String, TIMESTAMP, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from src.config.config import Base
from src.models.audit_mixin import AuditMixin

class Municipio(AuditMixin, Base):
    __tablename__ = "municipios"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True, comment="Identificador único del municipio")
    id_departamento = Column(Integer, ForeignKey("departamentos.id", onupdate="NO ACTION", ondelete="NO ACTION"), nullable=True, comment="Departamento al que pertenece el municipio")
    nombre = Column(String(100), nullable=False, unique=True, comment="Nombre del municipio")
    codigo_dane = Column(String(8), nullable=True, comment="Código DANE del municipio")
        
    departamento = relationship("Departamento", backref="municipios")
