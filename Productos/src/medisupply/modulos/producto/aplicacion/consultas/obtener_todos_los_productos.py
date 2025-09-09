
from dataclasses import dataclass
from medisupply.seedwork.aplicacion.consultas import Consulta
from medisupply.modulos.producto.aplicacion.consultas.base import ProductoConsultaBaseHandler
from medisupply.modulos.producto.dominio.repositorios import RepositorioProducto
from medisupply.seedwork.aplicacion.consultas import QueryResultado, ejecutar_consulta

@dataclass
class ObtenerTodosLosProductosConsulta(Consulta):
    pass

class ObtenerTodosLosProductosHandler(ProductoConsultaBaseHandler):
    def handle(self, consulta: ObtenerTodosLosProductosConsulta) -> QueryResultado:
        repositorio = self.fabrica_repositorio.crear_objeto(RepositorioProducto)
        productos = repositorio.obtener_todos()
        return QueryResultado(resultado=productos)

@ejecutar_consulta.register
def _(consulta: ObtenerTodosLosProductosConsulta):
    handler = ObtenerTodosLosProductosHandler()
    return handler.handle(consulta)