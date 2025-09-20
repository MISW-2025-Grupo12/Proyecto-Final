from dataclasses import dataclass
from seedwork.aplicacion.comandos import Comando, ejecutar_comando
import uuid
import time
import logging
from datetime import datetime
from typing import List
from modulos.ventas.aplicacion.dto import ItemDTO, EstadoPedido, PedidoDTO
from modulos.ventas.aplicacion.mapeadores import MapeadorPedido
from modulos.ventas.dominio.repositorios_comando import RepositorioPedidoComando
from modulos.ventas.dominio.fabricas import FabricaPedido
from modulos.ventas.aplicacion.comandos.base import PedidoComandoBaseHandler
from modulos.ventas.infraestructura.cliente_productos import ClienteProductos

logger = logging.getLogger(__name__)


@dataclass
class CrearPedido(Comando):
    cliente_id: uuid.UUID
    fecha_pedido: datetime
    estado: EstadoPedido
    items: List[dict]  # Lista de dicts con producto_id y cantidad

class CrearPedidoHandler(PedidoComandoBaseHandler):
    def __init__(self):
        super().__init__()
        self._mapeador = MapeadorPedido()
        self._fabrica_pedido = FabricaPedido()
        self._cliente_productos = ClienteProductos()
    
    def handle(self, comando: CrearPedido) -> PedidoDTO:
        start_time_command = time.time()
        timestamp = datetime.now().isoformat()
        
        logger.info(f"[METRICS-START] Crear pedido comando - Timestamp: {timestamp} - Cliente: {comando.cliente_id}")
        
        try:
            # 1. Obtener precios de productos y crear items completos
            start_products = time.time()
            items_completos = self._obtener_precios_y_crear_items(comando.items)
            products_time = (time.time() - start_products) * 1000
            logger.info(f"[METRICS-PRODUCTS] Obtención precios productos - Latencia: {products_time:.2f}ms - Items: {len(items_completos)}")
            
            # 2. Calcular el total del pedido
            start_calculation = time.time()
            total_pedido = sum(item.total for item in items_completos)
            calculation_time = (time.time() - start_calculation) * 1000
            logger.info(f"[METRICS-CALCULATION] Cálculo total pedido - Latencia: {calculation_time:.2f}ms - Total: {total_pedido}")
            
            # 3. Crear el DTO del pedido
            start_dto_creation = time.time()
            pedido_dto = PedidoDTO(
                cliente_id=comando.cliente_id,
                fecha_pedido=comando.fecha_pedido,
                estado=comando.estado,
                items=items_completos,
                total=total_pedido)
            
            # 4. Convertir DTO a entidad de dominio usando la fábrica
            pedido_entidad = self._fabrica_pedido.crear_objeto(pedido_dto, self._mapeador)
            dto_creation_time = (time.time() - start_dto_creation) * 1000
            logger.info(f"[METRICS-DTO] Creación DTO y entidad - Latencia: {dto_creation_time:.2f}ms")
            
            # 5. Guardar en el repositorio de comandos (que sincroniza automáticamente con consultas)
            start_persistence = time.time()
            repositorio_comando = self.repositorio_comando
            repositorio_comando.agregar(pedido_entidad)
            persistence_time = (time.time() - start_persistence) * 1000
            logger.info(f"[METRICS-PERSISTENCE] Persistencia comando - Latencia: {persistence_time:.2f}ms")
            
            # 6. Disparar evento de creación (opcional)
            start_event = time.time()
            pedido_entidad.disparar_evento_creacion()
            event_time = (time.time() - start_event) * 1000
            logger.info(f"[METRICS-EVENT] Disparo evento creación - Latencia: {event_time:.2f}ms")
            
            # 7. Retornar el DTO del pedido creado
            total_time = (time.time() - start_time_command) * 1000
            logger.info(f"[METRICS-END] Crear pedido comando - Latencia total: {total_time:.2f}ms - Cliente: {comando.cliente_id}")
            
            return pedido_dto
            
        except Exception as e:
            total_time = (time.time() - start_time_command) * 1000
            logger.error(f"[METRICS-ERROR] Crear pedido comando - Latencia: {total_time:.2f}ms - Error: {e} - Timestamp: {timestamp}")
            raise
    
    def _obtener_precios_y_crear_items(self, items: List[dict]) -> List[ItemDTO]:
        """Obtiene los precios de los productos y crea los items completos"""
        if not items:
            raise ValueError("El pedido debe tener al menos un item")
        
        items_completos = []
        for item_data in items:
            producto_id = uuid.UUID(item_data['producto_id'])
            cantidad = item_data['cantidad']
            
            try:
                # Obtener información del producto desde el servicio de productos
                producto_info = self._cliente_productos.obtener_producto(producto_id)
                
                if not producto_info:
                    raise ValueError(f"Producto con ID {producto_id} no encontrado")
                
                # Verificar stock disponible
                stock_disponible = producto_info.stock
                if stock_disponible < cantidad:
                    raise ValueError(f"Stock insuficiente para el producto {producto_id}. Disponible: {stock_disponible}, Solicitado: {cantidad}")
                
                # Obtener precio del servicio de productos
                precio = producto_info.precio
                if precio <= 0:
                    raise ValueError(f"Precio inválido para el producto {producto_id}: {precio}")
                
                # Calcular total del item
                total_item = precio * cantidad
                
                # Crear ItemDTO completo
                item_dto = ItemDTO(
                    producto_id=producto_id,
                    cantidad=cantidad,
                    precio=precio,
                    total=total_item
                )
                items_completos.append(item_dto)
                
            except Exception as e:
                if "Producto con ID" in str(e) or "Stock insuficiente" in str(e) or "Precio inválido" in str(e):
                    raise e
                else:
                    raise ValueError(f"Error obteniendo información del producto {producto_id}: {str(e)}")
        
        return items_completos 

@ejecutar_comando.register
def _(comando: CrearPedido):
    handler = CrearPedidoHandler()
    return handler.handle(comando)