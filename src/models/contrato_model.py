from sqlalchemy import Column, Integer, String, ForeignKey, Date, DECIMAL, Enum, Index
from sqlalchemy.orm import relationship
from src.config.config import Base
from src.models.audit_mixin import AuditMixin
import enum

class TipoContratoEnum(enum.Enum):
    obra = "obra"
    interventoria = "interventoria"
    convenio = "convenio"

"""
Modelo que representa los contratos asociados a proyectos.
Incluye información de valor, fechas, tipo y trazabilidad (auditoría y soft delete).
"""
class Contrato(AuditMixin, Base):
    __tablename__ = "contratos"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True, comment="Identificador único del contrato")
    id_proyecto = Column(Integer, ForeignKey("proyectos.id"), nullable=True, comment="Proyecto al que pertenece el contrato")
    numero_contrato = Column(String(100), nullable=False, unique=True, comment="Número oficial del contrato")
    tipo_contrato = Column(Enum(TipoContratoEnum), nullable=False, comment="Tipo de contrato: obra, interventoría o convenio")
    fecha_contrato = Column(Date, nullable=True, comment="Fecha de firma del contrato")
    objeto_contrato = Column(String, nullable=True, comment="Descripción del objeto del contrato")
    fecha_inicio = Column(Date, nullable=True, comment="Fecha de inicio de ejecución del contrato")
    fecha_terminacion = Column(Date, nullable=True, comment="Fecha de terminación del contrato")
    valor_contrato = Column(DECIMAL(18, 2), nullable=True, comment="Valor total del contrato en pesos colombianos")
    recursos_sostenibilidad = Column(DECIMAL(18, 2), nullable=True, comment="Recursos asignados para sostenibilidad")

    # Relación con proyecto (si existe el modelo Proyecto)
    proyecto = relationship("Proyecto", back_populates="contratos")
    persona = relationship("Persona", back_populates="contratos")
    
    __table_args__ = (
        Index("idx_contratos_id_proyecto", "id_proyecto"),
        Index("idx_contratos_numero_contrato", "numero_contrato"),
        Index("idx_contratos_tipo_contrato", "tipo_contrato"),
    )
    def __repr__(self):
        return f"<Contrato(id={self.id}, numero='{self.numero_contrato}', tipo='{self.tipo_contrato.value}', activo={self.activo})>"
