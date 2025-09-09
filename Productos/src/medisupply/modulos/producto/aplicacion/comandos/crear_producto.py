
from dataclasses import dataclass
from medisupply.seedwork.aplicacion.comandos import Comando, ejecutar_comando
import uuid
from medisupply.modulos.producto.aplicacion.dto import ProductoDTO
from medisupply.modulos.producto.aplicacion.mapeadores import MapeadorProducto
from medisupply.modulos.producto.dominio.repositorios import RepositorioProducto, RepositorioTipoProducto
from medisupply.modulos.producto.aplicacion.comandos.base import CrearProductoBaseHandler

@dataclass
class CrearProducto(Comando):
    nombre: str
    descripcion: str
    precio: float
    stock: int
    marca: str
    lote: str
    tipo_producto_id: uuid.UUID

class CrearProductoHandler(CrearProductoBaseHandler):
    def __init__(self):
        super().__init__()
        self._mapeador = MapeadorProducto()

    def handle(self, comando: CrearProducto) -> ProductoDTO:
        # 1. Obtener el tipo de producto existente
        repositorio_tipo = self.fabrica_repositorio.crear_objeto(RepositorioTipoProducto)
        tipo_producto = repositorio_tipo.obtener_por_id(comando.tipo_producto_id)
        
        if not tipo_producto:
            raise ValueError(f"Tipo de producto con ID {comando.tipo_producto_id} no encontrado")
        
        # 2. Crear el DTO del producto
        producto_dto = ProductoDTO(
            nombre=comando.nombre,
            descripcion=comando.descripcion,
            precio=comando.precio,
            stock=comando.stock,
            marca=comando.marca,
            lote=comando.lote,
            tipo_producto_id=comando.tipo_producto_id
        )
        
        # 3. Convertir DTO a entidad de dominio usando la fábrica
        producto_entidad = self.fabrica_producto.crear_objeto(producto_dto, MapeadorProducto())
        
        # 4. Guardar en el repositorio
        repositorio_producto = self.fabrica_repositorio.crear_objeto(RepositorioProducto)
        repositorio_producto.agregar(producto_entidad)
        
        # 5. Retornar el DTO del producto creado
        return self.fabrica_producto.crear_objeto(producto_entidad, MapeadorProducto())

@ejecutar_comando.register
def _(comando: CrearProducto):
    handler = CrearProductoHandler()
    return handler.handle(comando)