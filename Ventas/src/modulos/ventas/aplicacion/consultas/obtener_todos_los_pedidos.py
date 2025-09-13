from dataclasses import dataclass
from seedwork.aplicacion.consultas import Consulta
from modulos.ventas.aplicacion.consultas.base import PedidoConsultaBaseHandler
from modulos.ventas.dominio.repositorios_consulta import RepositorioPedidoConsulta
from seedwork.aplicacion.consultas import QueryResultado, ejecutar_consulta

@dataclass
class ObtenerTodosLosPedidosConsulta(Consulta):
    pass

class ObtenerTodosLosPedidosHandler(PedidoConsultaBaseHandler):
    def handle(self, consulta: ObtenerTodosLosPedidosConsulta) -> QueryResultado:
        repositorio_consulta = self.repositorio_consulta
        pedidos = repositorio_consulta.obtener_todos()
        return QueryResultado(resultado=pedidos)

@ejecutar_consulta.register
def _(consulta: ObtenerTodosLosPedidosConsulta):
    handler = ObtenerTodosLosPedidosHandler()
    return handler.handle(consulta)