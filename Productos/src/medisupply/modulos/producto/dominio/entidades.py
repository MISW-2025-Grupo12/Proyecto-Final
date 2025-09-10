from dataclasses import dataclass, field
from datetime import datetime
from medisupply.seedwork.dominio.entidades import Entidad, AgregacionRaiz
from .objetos_valor import Nombre, Descripcion, Precio, Stock, Marca, Lote
from .eventos import ProductoCreado, ProductoStockActualizado
from medisupply.seedwork.dominio.eventos import despachador_eventos

@dataclass
class TipoProducto(Entidad):    
    nombre: Nombre = field(default_factory=lambda: Nombre(""))
    descripcion: Descripcion = field(default_factory=lambda: Descripcion(""))


@dataclass
class Producto(AgregacionRaiz):
    nombre: Nombre = field(default_factory=lambda: Nombre(""))
    tipo: TipoProducto = field(default_factory=TipoProducto)
    descripcion: Descripcion = field(default_factory=lambda: Descripcion(""))
    precio: Precio = field(default_factory=lambda: Precio(0.0))
    stock: Stock = field(default_factory=lambda: Stock(0))
    marca: Marca = field(default_factory=lambda: Marca(""))
    lote: Lote = field(default_factory=lambda: Lote("", datetime.now(), datetime.now()))
    
    def __post_init__(self):
        super().__post_init__()
    
    def disparar_evento_creacion(self):
        """Dispara el evento de creación del producto"""
        evento = ProductoCreado(
            producto_id=self.id,
            nombre=self.nombre.nombre,
            descripcion=self.descripcion.descripcion,
            precio=self.precio.precio,
            stock=self.stock.stock,
            marca=self.marca.nombre,
            lote=self.lote.codigo,
            tipo_producto_id=self.tipo.id if self.tipo and self.tipo.id else None
        )
        print(f"Disparando evento de creación del producto: {evento}")
        despachador_eventos.publicar_evento(evento)
    
    def actualizar_stock(self, nuevo_stock: int, motivo: str = "Actualización manual"):
        """Actualiza el stock y dispara evento"""
        stock_anterior = self.stock.stock
        self.stock = Stock(nuevo_stock)
        
        evento = ProductoStockActualizado(
            producto_id=self.id,
            stock_anterior=stock_anterior,
            stock_nuevo=nuevo_stock,
            motivo=motivo
        )
        despachador_eventos.publicar_evento(evento)