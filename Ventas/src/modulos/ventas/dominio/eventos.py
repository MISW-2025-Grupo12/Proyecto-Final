from seedwork.dominio.eventos import EventoDominio
from dataclasses import dataclass, field
from typing import Dict, Any, List
import uuid
from datetime import datetime
from modulos.ventas.dominio.enums import EstadoPedido

@dataclass
class PedidoCreado(EventoDominio):
    pedido_id: uuid.UUID = field(default_factory=uuid.uuid4)
    cliente_id: uuid.UUID = field(default_factory=uuid.uuid4)
    fecha_pedido: datetime = field(default_factory=datetime.now)
    estado: EstadoPedido = field(default=EstadoPedido.PENDIENTE)
    items_info: List[Dict[str, Any]] = field(default_factory=list)  # Información básica de items
    total: float = field(default=0.0)

    def _get_datos_evento(self) -> Dict[str, Any]:
        return {
            'pedido_id': str(self.pedido_id),
            'cliente_id': str(self.cliente_id),
            'fecha_pedido': self.fecha_pedido.isoformat() if self.fecha_pedido else None,
            'estado': self.estado.value if hasattr(self.estado, 'value') else str(self.estado),
            'items_info': self.items_info,
            'total': self.total
        }