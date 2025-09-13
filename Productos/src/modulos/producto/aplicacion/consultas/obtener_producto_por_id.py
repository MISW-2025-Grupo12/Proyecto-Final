
from dataclasses import dataclass
from seedwork.aplicacion.consultas import Consulta, QueryResultado, ejecutar_consulta
from modulos.producto.aplicacion.consultas.base import ProductoConsultaBaseHandler
from modulos.producto.dominio.repositorios_consulta import RepositorioProductoConsulta
import uuid

@dataclass
class ObtenerProductoPorIdConsulta(Consulta):
    id: uuid.UUID

class ObtenerProductoPorIdHandler(ProductoConsultaBaseHandler):
    def handle(self, consulta: ObtenerProductoPorIdConsulta) -> QueryResultado:
        repositorio_consulta = self.fabrica_repositorio.crear_objeto(RepositorioProductoConsulta)
        producto = repositorio_consulta.obtener_por_id(consulta.id)
        return QueryResultado(resultado=producto)

@ejecutar_consulta.register
def _(consulta: ObtenerProductoPorIdConsulta):
    handler = ObtenerProductoPorIdHandler()
    return handler.handle(consulta)