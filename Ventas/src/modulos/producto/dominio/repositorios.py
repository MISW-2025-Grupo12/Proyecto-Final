from seedwork.dominio.repositorios import Repositorio
from abc import ABC

class RepositorioProducto(Repositorio, ABC):
    ...

class RepositorioTipoProducto(Repositorio, ABC):
    ...