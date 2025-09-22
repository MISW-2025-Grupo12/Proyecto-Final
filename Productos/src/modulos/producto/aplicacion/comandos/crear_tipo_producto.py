from dataclasses import dataclass


from seedwork.aplicacion.comandos import Comando, ejecutar_comando
from modulos.producto.aplicacion.comandos.base import ProductoComandoBaseHandler
from modulos.producto.aplicacion.dto import TipoProductoDTO
from modulos.producto.aplicacion.mapeadores import MapeadorTipoProducto
from modulos.producto.dominio.repositorios_comando import RepositorioTipoProductoComando

@dataclass
class CrearTipoProducto(Comando):
    nombre: str
    descripcion: str

class CrearTipoProductoHandler(ProductoComandoBaseHandler):
    def __init__(self):
        super().__init__()
        self._mapeador = MapeadorTipoProducto()

    def handle(self, comando: CrearTipoProducto) -> TipoProductoDTO:
        tipo_producto_dto = TipoProductoDTO(
            nombre=comando.nombre,
            descripcion=comando.descripcion)
        tipo_producto_entidad = self.fabrica_tipo_producto.crear_objeto(tipo_producto_dto, MapeadorTipoProducto())
        repositorio = self.fabrica_repositorio.crear_objeto(RepositorioTipoProductoComando)
        repositorio.agregar(tipo_producto_entidad)
        return self.fabrica_tipo_producto.crear_objeto(tipo_producto_entidad, MapeadorTipoProducto())

@ejecutar_comando.register
def _(comando: CrearTipoProducto):
    handler = CrearTipoProductoHandler()
    return handler.handle(comando)