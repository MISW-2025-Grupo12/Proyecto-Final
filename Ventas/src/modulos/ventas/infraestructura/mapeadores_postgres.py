# src/modulos/ventas/infraestructura/mapeadores_postgres.py
from seedwork.dominio.repositorios import Mapeador
from modulos.ventas.dominio.entidades import Pedido, Item, EstadoPedido
from modulos.ventas.infraestructura.dto_postgres import (
    PedidoComando, ItemComando,
    PedidoConsulta, ItemConsulta
)
from datetime import datetime
import json

class MapeadorPedidoComando(Mapeador):
    """Mapeador para modelos de comandos PostgreSQL"""

    def obtener_tipo(self) -> type:
        return PedidoComando

    def entidad_a_dto(self, entidad: Pedido) -> PedidoComando:
        return PedidoComando(
            id=entidad.id,
            cliente_id=entidad.cliente_id,
            fecha_pedido=entidad.fecha_pedido,
            estado=entidad.estado.value,
            total=entidad.total
        )

    def dto_a_entidad(self, dto: PedidoComando) -> Pedido:
        # Convertir items del modelo a entidades de dominio
        items_entidad = []
        for item_modelo in dto.items:
            item_entidad = Item(
                id=item_modelo.id,
                producto_id=item_modelo.producto_id,
                cantidad=item_modelo.cantidad,
                precio=float(item_modelo.precio),
                total=float(item_modelo.total)
            )
            items_entidad.append(item_entidad)
        
        return Pedido(
            id=dto.id,
            cliente_id=dto.cliente_id,
            fecha_pedido=dto.fecha_pedido,
            estado=EstadoPedido(dto.estado),
            items=items_entidad,
            total=float(dto.total)
        )

class MapeadorPedidoConsulta(Mapeador):
    """Mapeador para modelos de consultas PostgreSQL (desnormalizados)"""

    def obtener_tipo(self) -> type:
        return PedidoConsulta

    def entidad_a_dto(self, entidad: Pedido) -> PedidoConsulta:
        # Convertir items a JSON string para almacenamiento desnormalizado
        items_detalle = json.dumps([
            {
                'producto_id': str(item.producto_id),
                'cantidad': item.cantidad,
                'precio': float(item.precio),
                'total': float(item.total)
            } for item in entidad.items
        ])
        
        return PedidoConsulta(
            id=entidad.id,
            cliente_id=entidad.cliente_id,
            fecha_pedido=entidad.fecha_pedido,
            estado=entidad.estado.value,
            total=entidad.total,
            cantidad_items=len(entidad.items),
            items_detalle=items_detalle,
            fecha_ultima_actualizacion=datetime.utcnow()
        )

    def dto_a_entidad(self, dto: PedidoConsulta) -> Pedido:
        # Convertir items desde JSON string
        items_entidad = []
        if dto.items_detalle:
            try:
                items_data = json.loads(dto.items_detalle)
                for item_data in items_data:
                    item_entidad = Item(
                        producto_id=item_data['producto_id'],
                        cantidad=item_data['cantidad'],
                        precio=item_data['precio'],
                        total=item_data['total']
                    )
                    items_entidad.append(item_entidad)
            except (json.JSONDecodeError, KeyError):
                pass  # Si hay error, dejar lista vacía
        
        pedido = Pedido(
            cliente_id=dto.cliente_id,
            fecha_pedido=dto.fecha_pedido,
            estado=EstadoPedido(dto.estado),
            items=items_entidad,
            total=float(dto.total)
        )
        # Asignar el ID después de crear la entidad
        pedido._id = dto.id
        return pedido

class MapeadorItemComando(Mapeador):
    """Mapeador para items de comandos PostgreSQL"""

    def obtener_tipo(self) -> type:
        return ItemComando

    def entidad_a_dto(self, entidad: Item) -> ItemComando:
        return ItemComando(
            id=entidad.id,
            producto_id=entidad.producto_id,
            cantidad=entidad.cantidad,
            precio=entidad.precio,
            total=entidad.total
        )

    def dto_a_entidad(self, dto: ItemComando) -> Item:
        return Item(
            id=dto.id,
            producto_id=dto.producto_id,
            cantidad=dto.cantidad,
            precio=float(dto.precio),
            total=float(dto.total)
        )
