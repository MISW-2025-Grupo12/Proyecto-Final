from dataclasses import dataclass, field
import uuid
from typing import Optional
from medisupply.seedwork.aplicacion.dto import DTO

@dataclass(frozen=True)
class ProductoDTO(DTO):
    nombre: str
    descripcion: str
    precio: float
    stock: int
    marca: str
    lote: str
    tipo_producto_id: uuid.UUID
    id: uuid.UUID = field(default_factory=uuid.uuid4)

@dataclass(frozen=True)
class TipoProductoDTO(DTO):
    nombre: str
    descripcion: str
    id: Optional[uuid.UUID] = None