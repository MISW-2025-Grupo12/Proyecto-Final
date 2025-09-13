from seedwork.dominio.repositorios import Repositorio
from abc import ABC
from modulos.ventas.dominio.entidades import Pedido

class RepositorioPedidoComando(Repositorio, ABC):
    """Interfaz para repositorio de comandos de pedidos"""
    pass
