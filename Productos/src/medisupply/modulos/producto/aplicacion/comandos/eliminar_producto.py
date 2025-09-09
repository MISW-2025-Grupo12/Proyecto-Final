
from dataclasses import dataclass
from medisupply.seedwork.aplicacion.comandos import Comando
import uuid

@dataclass
class EliminarProductoComando(Comando):
    id: uuid.UUID
