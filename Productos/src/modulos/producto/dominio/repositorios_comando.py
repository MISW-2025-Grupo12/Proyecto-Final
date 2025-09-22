from seedwork.dominio.repositorios import Repositorio
from abc import ABC
from modulos.producto.dominio.entidades import Producto, TipoProducto
from uuid import UUID

class RepositorioProductoComando(Repositorio, ABC):
    """Repositorio específico para operaciones de escritura (comandos) de productos"""
    ...

class RepositorioTipoProductoComando(Repositorio, ABC):
    """Repositorio específico para operaciones de escritura (comandos) de tipos de producto"""
    ...
