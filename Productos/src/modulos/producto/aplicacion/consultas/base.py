from seedwork.aplicacion.consultas import ConsultaHandler
from modulos.producto.infraestructura.fabrica import FabricaRepositorio
from modulos.producto.dominio.fabricas import FabricaTipoProducto

class ProductoConsultaBaseHandler(ConsultaHandler):
    """Handler base para consultas de productos con CQRS"""
    
    def __init__(self):
        self._fabrica_repositorio = FabricaRepositorio()

    @property
    def fabrica_repositorio(self):
        return self._fabrica_repositorio

class TipoProductoConsultaBaseHandler(ConsultaHandler):
    def __init__(self):
        self._fabrica_repositorio = FabricaRepositorio()
        self._fabrica_tipo_producto = FabricaTipoProducto()
    
    @property
    def fabrica_repositorio(self):
        return self._fabrica_repositorio

    @property
    def fabrica_tipo_producto(self):
        return self._fabrica_tipo_producto
