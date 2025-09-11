# src/medisupply/seedwork/aplicacion/consultas.py
from dataclasses import dataclass
from abc import ABC, abstractmethod
from functools import singledispatch
from datetime import datetime
import uuid

@dataclass
class Consulta:
    ...

@dataclass
class QueryResultado:
    resultado: any = None

class ConsultaHandler(ABC):
    @abstractmethod
    def handle(self, consulta: Consulta) -> QueryResultado:
        raise NotImplementedError()

@singledispatch
def ejecutar_consulta(consulta: Consulta) -> QueryResultado:
    raise NotImplementedError(f"No existe implementacion para la consulta de tipo: {type(consulta).__name__}")
