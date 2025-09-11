
from dataclasses import dataclass
from seedwork.aplicacion.comandos import Comando
import uuid

@dataclass
class EliminarProductoComando(Comando):
    id: uuid.UUID
