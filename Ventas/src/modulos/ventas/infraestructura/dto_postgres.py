# src/modulos/ventas/infraestructura/dto_postgres.py
from config.config.db_postgres import db
import uuid
from datetime import datetime
from decimal import Decimal

# =============================================================================
# MODELOS DE COMANDOS (NORMALIZADOS) - Base de datos de comandos
# =============================================================================

class ItemComando(db.Model):
    """Modelo normalizado para items de pedidos en la base de comandos"""
    __tablename__ = 'items_comando'
    __bind_key__ = 'commands'
    
    id = db.Column(db.UUID, primary_key=True, default=uuid.uuid4)
    pedido_id = db.Column(db.UUID, db.ForeignKey('pedidos_comando.id'), nullable=False)
    producto_id = db.Column(db.UUID, nullable=False)
    cantidad = db.Column(db.Integer, nullable=False)
    precio = db.Column(db.Numeric(10, 2), nullable=False)  # Usar Decimal para precisión
    total = db.Column(db.Numeric(10, 2), nullable=False)
    
    # Relación con pedido
    pedido = db.relationship('PedidoComando', back_populates='items')

class PedidoComando(db.Model):
    """Modelo normalizado para pedidos en la base de comandos"""
    __tablename__ = 'pedidos_comando'
    __bind_key__ = 'commands'
    
    id = db.Column(db.UUID, primary_key=True, default=uuid.uuid4)
    cliente_id = db.Column(db.UUID, nullable=False)
    fecha_pedido = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    estado = db.Column(db.String(255), nullable=False)
    total = db.Column(db.Numeric(10, 2), nullable=False)
    
    # Relación con items
    items = db.relationship('ItemComando', back_populates='pedido', cascade='all, delete-orphan')

# =============================================================================
# MODELOS DE CONSULTAS (DESNORMALIZADOS) - Base de datos de consultas
# =============================================================================

class PedidoConsulta(db.Model):
    """Modelo desnormalizado para pedidos en la base de consultas"""
    __tablename__ = 'pedidos_consulta'
    __bind_key__ = 'queries'
    
    id = db.Column(db.UUID, primary_key=True, default=uuid.uuid4)
    cliente_id = db.Column(db.UUID, nullable=False)
    fecha_pedido = db.Column(db.DateTime, nullable=False)
    estado = db.Column(db.String(255), nullable=False)
    total = db.Column(db.Numeric(10, 2), nullable=False)
    
    # Campos desnormalizados para consultas rápidas
    cantidad_items = db.Column(db.Integer, nullable=False, default=0)
    items_detalle = db.Column(db.Text, nullable=True)  # JSON string con detalles de items
    
    # Campos adicionales para consultas complejas
    cliente_nombre = db.Column(db.String(255), nullable=True)  # Si tenemos datos del cliente
    fecha_ultima_actualizacion = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    
    # Índices para optimizar consultas
    __table_args__ = (
        db.Index('idx_pedidos_consulta_cliente', 'cliente_id'),
        db.Index('idx_pedidos_consulta_estado', 'estado'),
        db.Index('idx_pedidos_consulta_fecha', 'fecha_pedido'),
        db.Index('idx_pedidos_consulta_total', 'total'),
    )

class ItemConsulta(db.Model):
    """Modelo desnormalizado para items en la base de consultas (si necesitamos consultas específicas de items)"""
    __tablename__ = 'items_consulta'
    __bind_key__ = 'queries'
    
    id = db.Column(db.UUID, primary_key=True, default=uuid.uuid4)
    pedido_id = db.Column(db.UUID, nullable=False)
    producto_id = db.Column(db.UUID, nullable=False)
    cantidad = db.Column(db.Integer, nullable=False)
    precio = db.Column(db.Numeric(10, 2), nullable=False)
    total = db.Column(db.Numeric(10, 2), nullable=False)
    
    # Campos desnormalizados
    producto_nombre = db.Column(db.String(255), nullable=True)  # Si tenemos datos del producto
    pedido_cliente_id = db.Column(db.UUID, nullable=False)
    pedido_fecha = db.Column(db.DateTime, nullable=False)
    pedido_estado = db.Column(db.String(255), nullable=False)
    
    # Índices para optimizar consultas
    __table_args__ = (
        db.Index('idx_items_consulta_pedido', 'pedido_id'),
        db.Index('idx_items_consulta_producto', 'producto_id'),
        db.Index('idx_items_consulta_cliente', 'pedido_cliente_id'),
    )
