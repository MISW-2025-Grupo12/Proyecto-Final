from medisupply.config.config.db import db
import uuid

class TipoProducto(db.Model):
    __tablename__ = 'tipos_productos'
    id = db.Column(db.UUID, primary_key=True, default=uuid.uuid4)
    nombre = db.Column(db.String(255), nullable=False)
    descripcion = db.Column(db.String(255), nullable=False)
    productos = db.relationship('Producto', backref='tipo_producto')

class Producto(db.Model):
    __tablename__ = 'productos'
    id = db.Column(db.UUID, primary_key=True, default=uuid.uuid4)
    nombre = db.Column(db.String(255), nullable=False)
    descripcion = db.Column(db.String(255), nullable=False)
    precio = db.Column(db.Float, nullable=False)
    stock = db.Column(db.Integer, nullable=False)
    marca = db.Column(db.String(255), nullable=False)
    lote = db.Column(db.String(255), nullable=False)
    tipo_producto_id = db.Column(db.UUID, db.ForeignKey('tipos_productos.id'), nullable=False)