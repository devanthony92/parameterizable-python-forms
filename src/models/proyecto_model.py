from sqlalchemy import Column, Integer, String, Boolean, Date, Text, ForeignKey, Index
from sqlalchemy.orm import relationship
from src.config.config import Base
from src.models.audit_mixin import AuditMixin

"""
Modelo que representa los proyectos registrados en el sistema.
Incluye información sobre su unidad ejecutora, dirección territorial,
tipo, clasificación, convenios y campos de auditoría.
"""
class Proyecto(AuditMixin, Base):
    __tablename__ = "proyectos"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True, comment="Identificador único del proyecto")
    id_unidad_ejecutora = Column(Integer, ForeignKey("unidades_ejecutoras.id"), nullable=True, comment="Unidad ejecutora responsable del proyecto")
    id_direccion_territorial = Column(Integer, ForeignKey("direcciones_territoriales.id"), nullable=True, comment="Dirección territorial que supervisa el proyecto")
    id_tipo_proyecto = Column(Integer, ForeignKey("tipos_proyecto.id"), nullable=True, comment="Tipo de proyecto (licenciado/no licenciado)")
    id_ruta = Column(Integer, ForeignKey("rutas.id"), nullable=True, comment="Ruta vial principal del proyecto")
    id_tramo_sector = Column(Integer, ForeignKey("tramos_sectores.id"), nullable=True, comment="Tramo o sector específico del proyecto")
    id_clasificacion = Column(Integer, ForeignKey("clasificaciones.id"), nullable=True, comment="Clasificación del proyecto por tipo de suelo")
    id_modo_transporte = Column(Integer, ForeignKey("modos_transporte.id"), nullable=True, comment="Modo de transporte del proyecto")
    id_funcionalidad = Column(Integer, ForeignKey("funcionalidades.id"), nullable=True, comment="Funcionalidad carretera del proyecto")
    id_categorizacion = Column(Integer, ForeignKey("categorizaciones.id"), nullable=True, comment="Categorización del proyecto")

    objeto_proyecto = Column(Text, nullable=True, comment="Descripción detallada del objeto del proyecto")
    resolucion_licencia = Column(String(100), nullable=True, comment="Número de resolución de licencia ambiental (si aplica)")
    fecha_resolucion = Column(Date, nullable=True, comment="Fecha de expedición de la resolución")
    es_convenio_interadministrativo = Column(Boolean, nullable=False, default=False, comment="Indica si el proyecto es un convenio interadministrativo")
    numero_convenio = Column(String(100), nullable=True, comment="Número del convenio interadministrativo (si aplica)")

    # Relaciones
    contratos = relationship("Contrato", back_populates="proyecto", cascade="all, delete-orphan", lazy="select")
    tipo_proyecto = relationship("TipoProyecto", backref="proyectos")
    
    
    __table_args__ = (
        Index("idx_proyectos_id_unidad_ejecutora", "id_unidad_ejecutora"),
        Index("idx_proyectos_id_direccion_territorial", "id_direccion_territorial"),
        Index("idx_proyectos_id_tipo_proyecto", "id_tipo_proyecto"),
    )

    def __repr__(self):
        return f"<Proyecto(id={self.id}, objeto='{(self.objeto_proyecto[:30] + '...') if self.objeto_proyecto else ''}', activo={self.activo})>"
