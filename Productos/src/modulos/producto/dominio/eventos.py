from seedwork.dominio.eventos import EventoDominio
from dataclasses import dataclass, field
from typing import Dict, Any
import uuid


@dataclass
class ProductoCreado(EventoDominio):
    """Evento que se dispara cuando se crea un producto"""
    producto_id: uuid.UUID = field(default_factory=uuid.uuid4)
    nombre: str = field(default="")
    descripcion: str = field(default="")
    precio: float = field(default=0.0)
    stock: int = field(default=0)
    marca: str = field(default="")
    lote: str = field(default="")
    tipo_producto_id: uuid.UUID = field(default_factory=uuid.uuid4)
    
    def _get_datos_evento(self) -> Dict[str, Any]:
        return {
            'producto_id': str(self.producto_id),
            'nombre': self.nombre,
            'descripcion': self.descripcion,
            'precio': self.precio,
            'stock': self.stock,
            'marca': self.marca,
            'lote': self.lote,
            'tipo_producto_id': str(self.tipo_producto_id)
        }


@dataclass
class ProductoStockActualizado(EventoDominio):
    """Evento que se dispara cuando se actualiza el stock de un producto"""
    producto_id: uuid.UUID = field(default_factory=uuid.uuid4)
    stock_anterior: int = field(default=0)
    stock_nuevo: int = field(default=0)
    motivo: str = field(default="")
    
    def _get_datos_evento(self) -> Dict[str, Any]:
        return {
            'producto_id': str(self.producto_id),
            'stock_anterior': self.stock_anterior,
            'stock_nuevo': self.stock_nuevo,
            'motivo': self.motivo
        }


@dataclass
class TipoProductoCreado(EventoDominio):
    """Evento que se dispara cuando se crea un tipo de producto"""
    tipo_producto_id: uuid.UUID = field(default_factory=uuid.uuid4)
    nombre: str = field(default="")
    descripcion: str = field(default="")
    
    def _get_datos_evento(self) -> Dict[str, Any]:
        return {
            'tipo_producto_id': str(self.tipo_producto_id),
            'nombre': self.nombre,
            'descripcion': self.descripcion
        }