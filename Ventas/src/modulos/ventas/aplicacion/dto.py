from dataclasses import dataclass, field
import uuid
from typing import Optional
from seedwork.aplicacion.dto import DTO
from datetime import datetime
from typing import List
from modulos.ventas.dominio.enums import EstadoPedido

@dataclass(frozen=True)
class ItemDTO(DTO):
    producto_id: uuid.UUID
    cantidad: int
    precio: float
    total: float
    id: uuid.UUID = field(default_factory=uuid.uuid4)

@dataclass(frozen=True)
class PedidoDTO(DTO):
    cliente_id: uuid.UUID
    fecha_pedido: datetime
    estado: EstadoPedido
    items: List[ItemDTO]
    total: float
    id: Optional[uuid.UUID] = None