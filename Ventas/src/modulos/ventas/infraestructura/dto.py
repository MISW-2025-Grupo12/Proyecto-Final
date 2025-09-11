from config.config.db import db
import uuid

class Item(db.Model):
    __tablename__ = 'items'
    id = db.Column(db.UUID, primary_key=True, default=uuid.uuid4)
    pedido_id = db.Column(db.UUID, db.ForeignKey('pedidos.id'), nullable=False)
    producto_id = db.Column(db.UUID, nullable=False)
    cantidad = db.Column(db.Integer, nullable=False)
    precio = db.Column(db.Float, nullable=False)
    total = db.Column(db.Float, nullable=False)

    pedido = db.relationship('Pedido', back_populates='items')

class Pedido(db.Model):
    __tablename__ = 'pedidos'
    id = db.Column(db.UUID, primary_key=True, default=uuid.uuid4)
    cliente_id = db.Column(db.UUID, nullable=False)
    fecha_pedido = db.Column(db.DateTime, nullable=False)
    estado = db.Column(db.String(255), nullable=False)
    items = db.relationship('Item', back_populates='pedido', cascade='all, delete-orphan')
    total = db.Column(db.Float, nullable=False)

