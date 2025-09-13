from dataclasses import dataclass
from seedwork.aplicacion.comandos import Comando, ejecutar_comando
import uuid
from datetime import datetime
from typing import List
from modulos.ventas.aplicacion.dto import ItemDTO, EstadoPedido, PedidoDTO
from modulos.ventas.aplicacion.mapeadores import MapeadorPedido
from modulos.ventas.dominio.repositorios_comando import RepositorioPedidoComando
from modulos.ventas.dominio.fabricas import FabricaPedido
from modulos.ventas.aplicacion.comandos.base import PedidoComandoBaseHandler
from modulos.ventas.infraestructura.cliente_productos import ClienteProductos


@dataclass
class CrearPedido(Comando):
    cliente_id: uuid.UUID
    fecha_pedido: datetime
    estado: EstadoPedido
    items: List[ItemDTO]
    total: float

class CrearPedidoHandler(PedidoComandoBaseHandler):
    def __init__(self):
        super().__init__()
        self._mapeador = MapeadorPedido()
        self._fabrica_pedido = FabricaPedido()
        self._cliente_productos = ClienteProductos()
    
    def handle(self, comando: CrearPedido) -> PedidoDTO:
        # 1. Validar que todos los productos existen
        self._validar_productos(comando.items)
        
        # 2. Crear el DTO del pedido
        pedido_dto = PedidoDTO(
            cliente_id=comando.cliente_id,
            fecha_pedido=comando.fecha_pedido,
            estado=comando.estado,
            items=comando.items,
            total=comando.total)
        
        # 3. Convertir DTO a entidad de dominio usando la fábrica
        pedido_entidad = self._fabrica_pedido.crear_objeto(pedido_dto, self._mapeador)
        
        # 4. Guardar en el repositorio de comandos (que sincroniza automáticamente con consultas)
        repositorio_comando = self.repositorio_comando
        repositorio_comando.agregar(pedido_entidad)
        
        # 5. Disparar evento de creación (opcional)
        pedido_entidad.disparar_evento_creacion()
        
        # 6. Retornar el DTO del pedido creado
        return pedido_dto
    
    def _validar_productos(self, items: List[ItemDTO]):
        """Valida que todos los productos en el pedido existen y tienen stock disponible"""
        if not items:
            raise ValueError("El pedido debe tener al menos un item")
        
        # Convertir items a formato para validación
        items_dict = [
            {'producto_id': item.producto_id, 'cantidad': item.cantidad}
            for item in items
        ]
        
        # Validar existencia y stock de todos los productos de una vez
        validaciones = self._cliente_productos.validar_productos_y_stock(items_dict)
        
        # Verificar productos no encontrados
        productos_no_encontrados = [
            producto_id for producto_id, info in validaciones.items()
            if not info['existe']
        ]
        
        if productos_no_encontrados:
            raise ValueError(
                f"Los siguientes productos no existen: {productos_no_encontrados}"
            )
        
        # Verificar stock insuficiente
        productos_stock_insuficiente = [
            producto_id for producto_id, info in validaciones.items()
            if info['existe'] and not info['stock_ok']
        ]
        
        if productos_stock_insuficiente:
            errores_stock = []
            for producto_id in productos_stock_insuficiente:
                info = validaciones[producto_id]
                errores_stock.append(
                    f"Producto {producto_id}: solicitado {info['cantidad_solicitada']}, "
                    f"disponible {info['stock_disponible']}"
                )
            
            raise ValueError(
                f"Stock insuficiente para los siguientes productos: {'; '.join(errores_stock)}"
            ) 

@ejecutar_comando.register
def _(comando: CrearPedido):
    handler = CrearPedidoHandler()
    return handler.handle(comando)