"""
Comando para actualizar el stock de un producto
"""

from dataclasses import dataclass
from seedwork.aplicacion.comandos import Comando, ejecutar_comando
import uuid
from modulos.producto.aplicacion.dto import ProductoDTO
from modulos.producto.aplicacion.mapeadores import MapeadorProducto
from modulos.producto.dominio.repositorios import RepositorioProducto
from modulos.producto.dominio.fabricas import FabricaProducto
from modulos.producto.aplicacion.comandos.base import ProductoComandoBaseHandler
import logging

logger = logging.getLogger(__name__)

@dataclass
class ActualizarStockProducto(Comando):
    producto_id: uuid.UUID
    cantidad_vendida: int

class ActualizarStockProductoHandler(ProductoComandoBaseHandler):
    """Handler para actualizar el stock de un producto"""
    
    def __init__(self):
        super().__init__()
        self._mapeador = MapeadorProducto()
        self._fabrica_producto = FabricaProducto()
    
    def handle(self, comando: ActualizarStockProducto) -> ProductoDTO:
        """Actualiza el stock del producto restando la cantidad vendida"""
        
        logger.info(f"Actualizando stock del producto {comando.producto_id} con cantidad vendida {comando.cantidad_vendida}")
        # 1. Obtener el producto desde el repositorio
        repositorio = self.repositorio_comando
        producto_entidad = repositorio.obtener_por_id(comando.producto_id)
        
        if not producto_entidad:
            raise ValueError(f"Producto con ID {comando.producto_id} no encontrado")
        
        # 2. Verificar que hay stock suficiente

        if producto_entidad.stock.stock < comando.cantidad_vendida:
            raise ValueError(
                f"Stock insuficiente para producto {comando.producto_id}. "
                f"Disponible: {producto_entidad.stock.stock}, "
                f"Solicitado: {comando.cantidad_vendida}"
            )
        
        # 3. Actualizar el stock
        from modulos.producto.dominio.objetos_valor import Stock
        producto_entidad.stock = Stock(producto_entidad.stock.stock - comando.cantidad_vendida)
        
        # 4. Guardar los cambios
        repositorio.actualizar(producto_entidad)
        
        # 5. Convertir a DTO y retornar
        return self._mapeador.entidad_a_dto(producto_entidad)

@ejecutar_comando.register
def _(comando: ActualizarStockProducto):
    """Registra el handler para el comando ActualizarStockProducto"""
    handler = ActualizarStockProductoHandler()
    return handler.handle(comando)
