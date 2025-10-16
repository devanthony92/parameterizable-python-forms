from sqlalchemy import Column, Integer, String, TIMESTAMP, Boolean
from src.config.config import Base
from src.models.audit_mixin import AuditMixin

class Profesion(AuditMixin, Base):
    __tablename__ = "profesiones"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    nombre = Column(String(255), unique=True, nullable=False, comment="Nombre de la profesión o carrera")
    area_conocimiento = Column(String(100), nullable=True, comment="Área de conocimiento de la profesión")
    
