from dataclasses import dataclass, field
from seedwork.dominio.entidades import AgregacionRaiz, Entidad
from datetime import datetime
from typing import List, Literal
import uuid
from enum import Enum

@dataclass
class Item(Entidad):
    producto_id: uuid.UUID = field(default_factory=uuid.uuid4)
    cantidad: int = field(default=0)
    precio: float = field(default=0.0)
    total: float = field(default=0.0)

class EstadoPedido(Enum):
    PENDIENTE = "PENDIENTE"
    APROBADO = "APROBADO"
    RECHAZADO = "RECHAZADO"

@dataclass
class Pedido(AgregacionRaiz):
    cliente_id: uuid.UUID = field(default_factory=uuid.uuid4)
    fecha_pedido: datetime = field(default_factory=datetime.now)
    estado: EstadoPedido = field(default=EstadoPedido.PENDIENTE)
    items: List[Item] = field(default_factory=list)
    total: float = field(default=0.0)
