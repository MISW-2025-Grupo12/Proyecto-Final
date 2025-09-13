from config.config.db_postgres import db
import uuid

# =============================================================================
# MODELOS PARA COMANDOS (Base de datos normalizada - productos_commands)
# =============================================================================

class TipoProductoComando(db.Model):
    """Modelo de tipo de producto para comandos (normalizado)"""
    __tablename__ = 'tipos_productos'
    __bind_key__ = 'commands'
    
    id = db.Column(db.UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    nombre = db.Column(db.String(255), nullable=False)
    descripcion = db.Column(db.String(500), nullable=False)
    created_at = db.Column(db.DateTime, default=db.func.now())
    updated_at = db.Column(db.DateTime, default=db.func.now(), onupdate=db.func.now())
    
    # Relación con productos
    productos = db.relationship('ProductoComando', back_populates='tipo_producto')

class ProductoComando(db.Model):
    """Modelo de producto para comandos (normalizado)"""
    __tablename__ = 'productos'
    __bind_key__ = 'commands'
    
    id = db.Column(db.UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    nombre = db.Column(db.String(255), nullable=False)
    descripcion = db.Column(db.String(500), nullable=False)
    precio = db.Column(db.Numeric(10, 2), nullable=False)
    stock = db.Column(db.Integer, nullable=False)
    marca = db.Column(db.String(255), nullable=False)
    lote = db.Column(db.String(100), nullable=False)
    tipo_producto_id = db.Column(db.UUID(as_uuid=True), db.ForeignKey('tipos_productos.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=db.func.now())
    updated_at = db.Column(db.DateTime, default=db.func.now(), onupdate=db.func.now())
    
    # Relación con tipo de producto
    tipo_producto = db.relationship('TipoProductoComando', back_populates='productos')

# =============================================================================
# MODELOS PARA CONSULTAS (Base de datos denormalizada - productos_queries)
# =============================================================================

class ProductoConsulta(db.Model):
    """Modelo denormalizado de producto para consultas (optimizado para lectura)"""
    __tablename__ = 'productos_view'
    __bind_key__ = 'queries'
    
    id = db.Column(db.UUID(as_uuid=True), primary_key=True)
    nombre = db.Column(db.String(255), nullable=False)
    descripcion = db.Column(db.String(500), nullable=False)
    precio = db.Column(db.Numeric(10, 2), nullable=False)
    stock = db.Column(db.Integer, nullable=False)
    marca = db.Column(db.String(255), nullable=False)
    lote = db.Column(db.String(100), nullable=False)
    
    # Campos denormalizados del tipo de producto
    tipo_producto_id = db.Column(db.UUID(as_uuid=True), nullable=False)
    tipo_producto_nombre = db.Column(db.String(255), nullable=False)
    tipo_producto_descripcion = db.Column(db.String(500), nullable=False)
    
    # Campos adicionales para consultas
    created_at = db.Column(db.DateTime)
    updated_at = db.Column(db.DateTime)
    
    # Índices para optimizar consultas
    __table_args__ = (
        db.Index('idx_producto_tipo', 'tipo_producto_id'),
        db.Index('idx_producto_stock', 'stock'),
        db.Index('idx_producto_nombre', 'nombre'),
        db.Index('idx_producto_marca', 'marca'),
    )

class TipoProductoConsulta(db.Model):
    """Modelo de tipo de producto para consultas"""
    __tablename__ = 'tipos_productos_view'
    __bind_key__ = 'queries'
    
    id = db.Column(db.UUID(as_uuid=True), primary_key=True)
    nombre = db.Column(db.String(255), nullable=False)
    descripcion = db.Column(db.String(500), nullable=False)
    created_at = db.Column(db.DateTime)
    updated_at = db.Column(db.DateTime)
    
    # Campo calculado: cantidad de productos de este tipo
    cantidad_productos = db.Column(db.Integer, default=0)