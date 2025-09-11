from dataclasses import dataclass
from seedwork.aplicacion.consultas import Consulta
from modulos.ventas.aplicacion.consultas.base import ConsultaPedidoBaseHandler
from modulos.ventas.dominio.repositorios import RepositorioPedido
from seedwork.aplicacion.consultas import QueryResultado, ejecutar_consulta

@dataclass
class ObtenerTodosLosPedidosConsulta(Consulta):
    pass

class ObtenerTodosLosPedidosHandler(ConsultaPedidoBaseHandler):
    def handle(self, consulta: ObtenerTodosLosPedidosConsulta) -> QueryResultado:
        repositorio = self.fabrica_repositorio.crear_objeto(RepositorioPedido)
        pedidos = repositorio.obtener_todos()
        return QueryResultado(resultado=pedidos)

@ejecutar_consulta.register
def _(consulta: ObtenerTodosLosPedidosConsulta):
    handler = ObtenerTodosLosPedidosHandler()
    return handler.handle(consulta)