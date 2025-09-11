from seedwork.aplicacion.consultas import ConsultaHandler
from modulos.ventas.infraestructura.fabricas import FabricaRepositorio
from modulos.ventas.dominio.fabricas import FabricaPedido


class ConsultaPedidoBaseHandler(ConsultaHandler):
    def __init__(self):
        self._fabrica_repositorio = FabricaRepositorio()
        self._fabrica_pedido = FabricaPedido()

    @property
    def fabrica_repositorio(self):
        return self._fabrica_repositorio

    @property
    def fabrica_pedido(self):
        return self._fabrica_pedido