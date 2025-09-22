from seedwork.aplicacion.comandos import ComandoHandler
from modulos.producto.infraestructura.fabrica import FabricaRepositorio
from modulos.producto.dominio.fabricas import FabricaProducto, FabricaTipoProducto

class ProductoComandoBaseHandler(ComandoHandler):
    """Handler base para comandos de productos con CQRS"""
    
    def __init__(self):
        self._fabrica_repositorio = FabricaRepositorio()
        self._fabrica_producto = FabricaProducto()
        self._fabrica_tipo_producto = FabricaTipoProducto()

    @property
    def fabrica_repositorio(self):
        return self._fabrica_repositorio
    
    @property
    def repositorio_comando(self):
        """Acceso directo al repositorio de comandos"""
        from modulos.producto.dominio.repositorios_comando import RepositorioProductoComando
        return self._fabrica_repositorio.crear_objeto(RepositorioProductoComando)

    @property
    def fabrica_producto(self):
        return self._fabrica_producto

    @property
    def fabrica_tipo_producto(self):
        return self._fabrica_tipo_producto
