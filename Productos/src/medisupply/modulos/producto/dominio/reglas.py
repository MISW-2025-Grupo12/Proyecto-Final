from medisupply.seedwork.dominio.reglas import ReglaNegocio
from .objetos_valor import Nombre, Descripcion, Precio


class NombreProductoNoPuedeSerVacio(ReglaNegocio):
    nombre: Nombre
    def __init__(self, nombre, mensaje='El nombre del producto no puede ser vacio'):
        super().__init__(mensaje)
        self.nombre = nombre

    def es_valido(self) -> bool:
        return self.nombre is not None and self.nombre.nombre.strip() != ''


class DescripcionProductoNoPuedeSerVacio(ReglaNegocio):
    descripcion: Descripcion
    def __init__(self, descripcion, mensaje='La descripcion del producto no puede ser vacio'):
        super().__init__(mensaje)
        self.descripcion = descripcion

    def es_valido(self) -> bool:
        return self.descripcion is not None and self.descripcion.descripcion.strip() != ''


class PrecioProductoNoPuedeSerVacio(ReglaNegocio):
    precio: Precio
    def __init__(self, precio, mensaje='El precio del producto no puede ser vacio'):
        super().__init__(mensaje)
        self.precio = precio
    
    def es_valido(self) -> bool:
        return self.precio is not None and self.precio.precio > 0


class PrecioProductoNoPuedeSerMenorACero(ReglaNegocio):
    precio: Precio
    def __init__(self, precio, mensaje='El precio del producto no puede ser menor a cero'):
        super().__init__(mensaje)
        self.precio = precio

    def es_valido(self) -> bool:
        return self.precio is not None and self.precio.precio > 0

class PrecioProductoDebeSerNumerico(ReglaNegocio):
    precio: Precio
    def __init__(self, precio, mensaje='El precio del producto debe ser numerico'):
        super().__init__(mensaje)
        self.precio = precio

    def es_valido(self) -> bool:
        return isinstance(self.precio.precio, float)

class NombreTipoProductoNoPuedeSerVacio(ReglaNegocio):
    nombre: Nombre
    def __init__(self, nombre, mensaje='El nombre del tipo de producto no puede ser vacio'):
        super().__init__(mensaje)
        self.nombre = nombre

    def es_valido(self) -> bool:
        return self.nombre is not None and self.nombre.nombre.strip() != ''

class DescripcionTipoProductoNoPuedeSerVacio(ReglaNegocio):
    descripcion: Descripcion
    def __init__(self, descripcion, mensaje='La descripcion del tipo de producto no puede ser vacio'):
        super().__init__(mensaje)
        self.descripcion = descripcion

    def es_valido(self) -> bool:
        return self.descripcion is not None and self.descripcion.descripcion.strip() != ''