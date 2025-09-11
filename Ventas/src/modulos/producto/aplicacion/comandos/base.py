
from medisupply.seedwork.aplicacion.comandos import ComandoHandler
from medisupply.modulos.producto.infraestructura.fabricas import FabricaRepositorio
from medisupply.modulos.producto.dominio.fabricas import FabricaProducto, FabricaTipoProducto


class CrearProductoBaseHandler(ComandoHandler):
    def __init__(self):
        self._fabrica_repositorio = FabricaRepositorio()
        self._fabrica_producto = FabricaProducto()

    @property
    def fabrica_repositorio(self):
        return self._fabrica_repositorio

    @property
    def fabrica_producto(self):
        return self._fabrica_producto

class CrearTipoProductoBaseHandler(ComandoHandler):
    def __init__(self):
        self._fabrica_repositorio = FabricaRepositorio()
        self._fabrica_tipo_producto = FabricaTipoProducto()

    @property
    def fabrica_repositorio(self):
        return self._fabrica_repositorio

    @property
    def fabrica_tipo_producto(self):
        return self._fabrica_tipo_producto
