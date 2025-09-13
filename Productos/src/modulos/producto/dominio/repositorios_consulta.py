from seedwork.dominio.repositorios import Repositorio
from abc import ABC
from modulos.producto.dominio.entidades import Producto, TipoProducto
from uuid import UUID

class RepositorioProductoConsulta(Repositorio, ABC):
    """Repositorio específico para operaciones de lectura (consultas) de productos"""
    ...

class RepositorioTipoProductoConsulta(Repositorio, ABC):
    """Repositorio específico para operaciones de lectura (consultas) de tipos de producto"""
    ...
