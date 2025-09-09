from dataclasses import dataclass
from datetime import datetime
from medisupply.seedwork.dominio.objetos_valor import ObjetoValor

@dataclass(frozen=True)
class Nombre(ObjetoValor):
    nombre: str

@dataclass(frozen=True)
class Descripcion(ObjetoValor):
    descripcion: str

@dataclass(frozen=True)
class Precio(ObjetoValor):
    precio: float

@dataclass(frozen=True)
class Stock(ObjetoValor):
    stock: int

@dataclass(frozen=True)
class Categoria(ObjetoValor):
    nombre: str

@dataclass(frozen=True)
class Marca(ObjetoValor):
    nombre: str

@dataclass(frozen=True)
class Lote(ObjetoValor):
    codigo: str
    fecha_vencimiento: datetime
    fecha_fabricacion: datetime
