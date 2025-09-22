# src/seedwork/aplicacion/comandos.py
from dataclasses import dataclass, field
from abc import ABC, abstractmethod
from datetime import datetime
from functools import singledispatch
import uuid

@dataclass
class Comando:
    ...

class ComandoHandler(ABC):
    @abstractmethod
    def handle(self, comando: Comando):
        raise NotImplementedError()

@singledispatch
def ejecutar_comando(comando):
    raise NotImplementedError(f"No existe implementacion para el comando de tipo: {type(comando).__name__}")
