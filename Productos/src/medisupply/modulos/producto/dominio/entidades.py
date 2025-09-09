from dataclasses import dataclass, field
from medisupply.seedwork.dominio.entidades import Entidad, AgregacionRaiz
from .objetos_valor import Nombre, Descripcion, Precio, Stock, Marca, Lote

@dataclass
class TipoProducto(Entidad):    
    nombre: Nombre = field (default_factory=Nombre)
    descripcion: Descripcion = field(default_factory=Descripcion)

@dataclass
class Producto(AgregacionRaiz):
    nombre: Nombre = field(default_factory=Nombre)
    tipo: TipoProducto = field(default_factory=TipoProducto)
    descripcion: Descripcion = field(default_factory=Descripcion)
    precio: Precio = field(default_factory=Precio)
    stock: Stock = field(default_factory=Stock)
    marca: Marca = field(default_factory=Marca)
    lote: Lote = field(default_factory=Lote)
