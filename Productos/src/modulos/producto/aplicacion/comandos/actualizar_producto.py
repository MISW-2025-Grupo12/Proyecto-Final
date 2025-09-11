
from dataclasses import dataclass
from seedwork.aplicacion.comandos import Comando
import uuid

@dataclass
class ActualizarProductoComando(Comando):
    id: uuid.UUID
    nombre: str = None
    descripcion: str = None
    precio: float = None
    stock: int = None
    marca: str = None
    lote: str = None
    tipo_producto_id: uuid.UUID = None

