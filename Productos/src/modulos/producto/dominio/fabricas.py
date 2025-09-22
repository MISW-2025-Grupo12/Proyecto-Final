from dataclasses import dataclass
from seedwork.dominio.fabricas import Fabrica
from seedwork.dominio.entidades import Entidad
from seedwork.dominio.repositorios import Mapeador
from .entidades import Producto, TipoProducto
from .reglas import NombreProductoNoPuedeSerVacio, DescripcionProductoNoPuedeSerVacio, PrecioProductoNoPuedeSerVacio
from .reglas import PrecioProductoNoPuedeSerMenorACero, PrecioProductoDebeSerNumerico, NombreTipoProductoNoPuedeSerVacio 
from .reglas import DescripcionTipoProductoNoPuedeSerVacio

@dataclass
class FabricaProducto(Fabrica):
    def crear_objeto(self, obj: any, mapeador: Mapeador) -> any:
        if isinstance(obj, Entidad):
            return mapeador.entidad_a_dto(obj)
        else:
            print( "Fabricando producto: ", obj)
            
            producto: Producto = mapeador.dto_a_entidad(obj)
            self.validar_regla(NombreProductoNoPuedeSerVacio(producto.nombre))
            self.validar_regla(DescripcionProductoNoPuedeSerVacio(producto.descripcion))
            self.validar_regla(PrecioProductoNoPuedeSerVacio(producto.precio))
            self.validar_regla(PrecioProductoNoPuedeSerMenorACero(producto.precio))
            self.validar_regla(PrecioProductoDebeSerNumerico(producto.precio))
                        
            return producto

@dataclass
class FabricaTipoProducto(Fabrica):
    def crear_objeto(self, obj: any, mapeador: Mapeador) -> any:
        if isinstance(obj, Entidad):
            return mapeador.entidad_a_dto(obj)
        else:
            print( "Fabricando tipo de producto: ", obj)
            tipo_producto: TipoProducto = mapeador.dto_a_entidad(obj)
            self.validar_regla(NombreTipoProductoNoPuedeSerVacio(tipo_producto.nombre))
            self.validar_regla(DescripcionTipoProductoNoPuedeSerVacio(tipo_producto.descripcion))
            return tipo_producto

    