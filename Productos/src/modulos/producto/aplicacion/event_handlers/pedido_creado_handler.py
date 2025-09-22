"""
Handler para el evento PedidoCreado que actualiza el stock de productos
"""

import logging
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
        try:
            # Extraer datos del evento
            datos_evento = evento._get_datos_evento()
            
            logger.info(f"📦 Procesando evento PedidoCreado para pedido {datos_evento.get('pedido_id')}")
            
            # Obtener items del pedido
            items_info = datos_evento.get('items_info', [])
            
            if not items_info:
                logger.warning(f"⚠️ Pedido {datos_evento.get('pedido_id')} no tiene items")
                return
            
            # Actualizar stock para cada producto
            for item_info in items_info:
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
                    
                    logger.info(f"✅ Stock actualizado para producto {producto_id}: -{cantidad_vendida} unidades")
                    
                except Exception as e:
                    logger.error(f"❌ Error actualizando stock para producto {producto_id}: {e}")
                    continue
            
            logger.info(f"✅ Procesamiento completo del evento PedidoCreado para pedido {datos_evento.get('pedido_id')}")
            
        except Exception as e:
            logger.error(f"❌ Error procesando evento PedidoCreado: {e}")

@ejecutar_evento.register(PedidoCreado)
def _(evento: PedidoCreado):
    """Registra el handler para eventos PedidoCreado"""
    handler = PedidoCreadoHandler()
    handler.handle(evento)
