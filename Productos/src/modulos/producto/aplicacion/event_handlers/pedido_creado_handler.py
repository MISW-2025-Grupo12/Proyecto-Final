"""
Handler para el evento PedidoCreado que actualiza el stock de productos
"""

import logging
import time
from datetime import datetime
from typing import Dict, Any
from seedwork.aplicacion.eventos import ejecutar_evento
from seedwork.dominio.eventos import EventoDominio
from modulos.producto.dominio.eventos_externos import PedidoCreado
from modulos.producto.aplicacion.comandos.actualizar_stock_producto import ActualizarStockProducto, ActualizarStockProductoHandler
from modulos.producto.dominio.repositorios import RepositorioProducto

logger = logging.getLogger(__name__)

class PedidoCreadoHandler:
    """Handler para procesar eventos de pedidos creados y actualizar stock"""
    
    def __init__(self):
        self._repositorio_producto = None
    
    @property
    def repositorio_producto(self) -> RepositorioProducto:
        """Obtiene el repositorio de productos"""
        if self._repositorio_producto is None:
            from modulos.producto.infraestructura.fabrica import FabricaRepositorioUnificada
            fabrica = FabricaRepositorioUnificada()
            self._repositorio_producto = fabrica.fabrica_repositorio_comando
        return self._repositorio_producto
    
    def handle(self, evento: EventoDominio) -> None:
        """Procesa el evento PedidoCreado y actualiza el stock"""
        start_time_event = time.time()
        timestamp = datetime.now().isoformat()
        
        try:
            # Extraer datos del evento
            start_extraction = time.time()
            datos_evento = evento._get_datos_evento()
            extraction_time = (time.time() - start_extraction) * 1000
            
            pedido_id = datos_evento.get('pedido_id')
            logger.info(f"[METRICS-START] Procesar evento PedidoCreado - Timestamp: {timestamp} - Pedido: {pedido_id}")
            logger.info(f"[METRICS-EXTRACTION] Extracción datos evento - Latencia: {extraction_time:.2f}ms")
            
            # Obtener items del pedido
            items_info = datos_evento.get('items_info', [])
            
            if not items_info:
                logger.warning(f"⚠️ Pedido {pedido_id} no tiene items")
                return
            
            # Actualizar stock para cada producto
            start_stock_update = time.time()
            items_processed = 0
            
            for item_info in items_info:
                item_start_time = time.time()
                producto_id = item_info.get('producto_id')
                cantidad_vendida = item_info.get('cantidad', 0)
                
                if not producto_id or cantidad_vendida <= 0:
                    logger.warning(f"⚠️ Item inválido en pedido: {item_info}")
                    continue
                
                try:
                    # Crear comando para actualizar stock
                    comando = ActualizarStockProducto(
                        producto_id=producto_id,
                        cantidad_vendida=cantidad_vendida
                    )
                    
                    # Ejecutar comando
                    handler = ActualizarStockProductoHandler()
                    resultado = handler.handle(comando)
                    
                    item_time = (time.time() - item_start_time) * 1000
                    items_processed += 1
                    logger.info(f"[METRICS-ITEM] Stock actualizado producto {producto_id} - Latencia: {item_time:.2f}ms - Cantidad: -{cantidad_vendida}")
                    
                except Exception as e:
                    item_time = (time.time() - item_start_time) * 1000
                    logger.error(f"[METRICS-ITEM-ERROR] Error actualizando stock producto {producto_id} - Latencia: {item_time:.2f}ms - Error: {e}")
                    continue
            
            stock_update_time = (time.time() - start_stock_update) * 1000
            total_time = (time.time() - start_time_event) * 1000
            
            logger.info(f"[METRICS-END] Procesar evento PedidoCreado - Latencia total: {total_time:.2f}ms - Items procesados: {items_processed} - Pedido: {pedido_id}")
            
        except Exception as e:
            total_time = (time.time() - start_time_event) * 1000
            logger.error(f"[METRICS-ERROR] Error procesando evento PedidoCreado - Latencia: {total_time:.2f}ms - Error: {e} - Timestamp: {timestamp}")
            raise

@ejecutar_evento.register(PedidoCreado)
def _(evento: PedidoCreado):
    """Registra el handler para eventos PedidoCreado"""
    handler = PedidoCreadoHandler()
    handler.handle(evento)
