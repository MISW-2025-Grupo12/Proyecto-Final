
from dataclasses import dataclass
from seedwork.aplicacion.consultas import Consulta
from modulos.producto.aplicacion.consultas.base import ProductoConsultaBaseHandler
from modulos.producto.dominio.repositorios_consulta import RepositorioProductoConsulta
from seedwork.aplicacion.consultas import QueryResultado, ejecutar_consulta

@dataclass
class ObtenerTodosLosProductosConsulta(Consulta):
    pass

class ObtenerTodosLosProductosHandler(ProductoConsultaBaseHandler):
    def handle(self, consulta: ObtenerTodosLosProductosConsulta) -> QueryResultado:
        repositorio_consulta = self.fabrica_repositorio.crear_objeto(RepositorioProductoConsulta)
        productos = repositorio_consulta.obtener_todos()
        return QueryResultado(resultado=productos)

@ejecutar_consulta.register
def _(consulta: ObtenerTodosLosProductosConsulta):
    handler = ObtenerTodosLosProductosHandler()
    return handler.handle(consulta)