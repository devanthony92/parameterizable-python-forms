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

    # Relaciones con catalogos / entidades
    id = Column(Integer, primary_key=True, index=True, autoincrement=True, comment="Identificador único del proyecto")
    id_unidad_ejecutora = Column(Integer, ForeignKey("unidades_ejecutoras.id"), nullable=True, comment="Unidad ejecutora responsable del proyecto")
    id_direccion_territorial = Column(Integer, ForeignKey("direcciones_territoriales.id"), nullable=True, comment="Dirección territorial que supervisa el proyecto")
    id_tipo_proyecto = Column(Integer, ForeignKey("tipos_proyecto.id"), nullable=True, comment="Tipo de proyecto (licenciado/no licenciado)")
    id_ruta = Column(Integer, ForeignKey("rutas.id"), nullable=True, comment="Ruta vial principal del proyecto")
    id_tramo_sector = Column(Integer, ForeignKey("tramos_sectores.id"), nullable=True, comment="Tramo o sector específico del proyecto")
    id_clasificacion = Column(Integer, ForeignKey("clasificaciones_proyecto.id"), nullable=True, comment="Clasificación del proyecto por tipo de suelo")
    id_modo_transporte = Column(Integer, ForeignKey("modos_transporte.id"), nullable=True, comment="Modo de transporte del proyecto")
    id_funcionalidad = Column(Integer, ForeignKey("funcionalidades_carreteras.id"), nullable=True, comment="Funcionalidad carretera del proyecto")
    id_categorizacion = Column(Integer, ForeignKey("categorizaciones_carreteras.id"), nullable=True, comment="Categorización del proyecto")

    # Atributos propios del proyecto
    objeto_proyecto = Column(Text, nullable=True, comment="Descripción detallada del objeto del proyecto")
    resolucion_licencia = Column(String(100), nullable=True, comment="Número de resolución de licencia ambiental (si aplica)")
    fecha_resolucion = Column(Date, nullable=True, comment="Fecha de expedición de la resolución")
    es_convenio_interadministrativo = Column(Boolean, nullable=False, default=False, comment="Indica si el proyecto es un convenio interadministrativo")
    numero_convenio = Column(String(100), nullable=True, comment="Número del convenio interadministrativo (si aplica)")

# Relaciones ORM
    unidad_ejecutora = relationship("UnidadEjecutora", back_populates="proyectos")
    direccion_territorial = relationship("DireccionTerritorial", back_populates="proyectos")
    tipo_proyecto = relationship("TipoProyecto", back_populates="proyectos")
    ruta = relationship("Ruta", back_populates="proyectos")
    tramo_sector = relationship("TramoSector", back_populates="proyectos")
    clasificacion = relationship("ClasificacionProyecto", back_populates="proyectos")
    modo_transporte = relationship("ModoTransporte", back_populates="proyectos")
    funcionalidad = relationship("FuncionalidadCarretera", back_populates="proyectos")
    categorizacion = relationship("CategorizacionCarretera", back_populates="proyectos")
    persona = relationship("Persona", back_populates="proyectos")

    contratos = relationship("Contrato", back_populates="proyecto")
    # indices
    __table_args__ = (
        Index("idx_proyectos_id_unidad_ejecutora", "id_unidad_ejecutora"),
        Index("idx_proyectos_id_direccion_territorial", "id_direccion_territorial"),
        Index("idx_proyectos_id_tipo_proyecto", "id_tipo_proyecto"),
        Index("idx_proyectos_id_ruta", "id_ruta"),
        Index("idx_proyectos_id_tramo_sector", "id_tramo_sector"),
        Index("idx_proyectos_id_clasificacion", "id_clasificacion"),
        Index("idx_proyectos_id_modo_transporte", "id_modo_transporte"),
        Index("idx_proyectos_id_funcionalidad", "id_funcionalidad"),
        Index("idx_proyectos_id_categorizacion", "id_categorizacion"),
        Index("idx_proyectos_id_persona", "id_persona"),
    )
    def __repr__(self):
        return f"<Proyecto(id={self.id}, objeto='{(self.objeto_proyecto[:30] + '...') if self.objeto_proyecto else ''}', activo={self.activo})>"
