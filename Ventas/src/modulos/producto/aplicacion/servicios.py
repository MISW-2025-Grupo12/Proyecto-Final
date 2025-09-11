from medisupply.seedwork.dominio.servicios import Servicio

from medisupply.modulos.producto.dominio.fabricas import FabricaProducto, FabricaTipoProducto
from medisupply.modulos.producto.dominio.entidades import Producto, TipoProducto
from medisupply.modulos.producto.infraestructura.repositorios import RepositorioProducto, RepositorioTipoProducto
from medisupply.modulos.producto.infraestructura.fabricas import FabricaRepositorio

from .dto import ProductoDTO, TipoProductoDTO
from .mapeadores import MapeadorProducto, MapeadorTipoProducto

class ServicioProducto(Servicio):

    def __init__(self):
        self._fabrica_repositorio = FabricaRepositorio()
        self._fabrica_producto = FabricaProducto()
        self._fabrica_tipo_producto = FabricaTipoProducto()

    @property
    def fabrica_repositorio(self):
        return self._fabrica_repositorio

    @property
    def fabrica_producto(self):
        return self._fabrica_producto

    @property
    def fabrica_tipo_producto(self):
        return self._fabrica_tipo_producto

    def crear_producto(self, producto_dto: ProductoDTO) -> ProductoDTO:
        # Obtener el tipo de producto existente
        repositorio_tipo = self.fabrica_repositorio.crear_objeto(RepositorioTipoProducto)
        tipo_producto = repositorio_tipo.obtener_por_id(producto_dto.tipo_producto_id)
        
        if not tipo_producto:
            raise ValueError(f"Tipo de producto con ID {producto_dto.tipo_producto_id} no encontrado")
        
        # Crear el producto con el tipo de producto correcto
        map_producto = MapeadorProducto()
        producto: Producto = map_producto.dto_a_entidad(producto_dto, tipo_producto)
        
        # Guardar el producto
        repositorio_producto = self.fabrica_repositorio.crear_objeto(RepositorioProducto)
        repositorio_producto.agregar(producto)
        
        # Retornar el DTO del producto creado
        return map_producto.entidad_a_dto(producto)

    def crear_tipo_producto(self, tipo_producto_dto: TipoProductoDTO) -> TipoProductoDTO:
        print(f"Creando tipo de producto: {tipo_producto_dto}")
        map_tipo_producto = MapeadorTipoProducto()
        tipo_producto: TipoProducto = self.fabrica_tipo_producto.crear_objeto(tipo_producto_dto, MapeadorTipoProducto())
        repositorio = self.fabrica_repositorio.crear_objeto(RepositorioTipoProducto)
        repositorio.agregar(tipo_producto)
        return self.fabrica_tipo_producto.crear_objeto(tipo_producto, MapeadorTipoProducto())