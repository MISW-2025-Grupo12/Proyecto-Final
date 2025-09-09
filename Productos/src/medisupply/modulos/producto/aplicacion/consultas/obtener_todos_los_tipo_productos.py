from dataclasses import dataclass
from medisupply.seedwork.aplicacion.consultas import Consulta
from medisupply.modulos.producto.aplicacion.consultas.base import TipoProductoConsultaBaseHandler
from medisupply.modulos.producto.dominio.repositorios import RepositorioTipoProducto
from medisupply.seedwork.aplicacion.consultas import QueryResultado, ejecutar_consulta

@dataclass
class ObtenerTodosLosTiposDeProductoConsulta(Consulta):
    pass

class ObtenerTodosLosTiposDeProductoHandler(TipoProductoConsultaBaseHandler):
    def handle(self, consulta: ObtenerTodosLosTiposDeProductoConsulta) -> QueryResultado:
        repositorio = self.fabrica_repositorio.crear_objeto(RepositorioTipoProducto)
        tipos_productos = repositorio.obtener_todos()
        return QueryResultado(resultado=tipos_productos)
        
@ejecutar_consulta.register
def _(consulta: ObtenerTodosLosTiposDeProductoConsulta):
    handler = ObtenerTodosLosTiposDeProductoHandler()
    return handler.handle(consulta)