from dataclasses import dataclass, field
from seedwork.dominio.entidades import AgregacionRaiz, Entidad
from datetime import datetime
from typing import List, Literal
import uuid
from seedwork.dominio.eventos import despachador_eventos
from modulos.ventas.dominio.eventos import PedidoCreado
from modulos.ventas.dominio.enums import EstadoPedido

@dataclass
class Item:
    producto_id: uuid.UUID
    cantidad: int = 0
    precio: float = 0.0
    total: float = 0.0

@dataclass
class Pedido(AgregacionRaiz):
    cliente_id: uuid.UUID = field(default_factory=uuid.uuid4)
    fecha_pedido: datetime = field(default_factory=datetime.now)
    estado: EstadoPedido = field(default=EstadoPedido.PENDIENTE)
    items: List[Item] = field(default_factory=list)
    total: float = field(default=0.0)

    def __post_init__(self):
        super().__post_init__()
        
    def disparar_evento_creacion(self):
        """Dispara el evento de creación del pedido"""
        # Convertir items a información básica para el evento
        items_info = [
            {
                'producto_id': str(item.producto_id),
                'cantidad': item.cantidad,
                'precio': item.precio,
                'total': item.total
            }
            for item in self.items
        ]
        
        evento = PedidoCreado(
            pedido_id=self.id,
            cliente_id=self.cliente_id,
            fecha_pedido=self.fecha_pedido,
            estado=self.estado,
            items_info=items_info,
            total=self.total)
        despachador_eventos.publicar_evento(evento)