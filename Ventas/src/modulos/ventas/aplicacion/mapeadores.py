from seedwork.aplicacion.dto import Mapeador as AppMap
from seedwork.dominio.repositorios import Mapeador as RepMap
from modulos.ventas.aplicacion.dto import PedidoDTO, ItemDTO
from modulos.ventas.dominio.entidades import EstadoPedido, Pedido
from datetime import datetime
import uuid

class MapeadorPedidoDTOJson(AppMap):

    def externo_a_dto(self, externo: dict) -> PedidoDTO:
        # Convertir items de diccionarios a ItemDTOs
        items_dto = []
        for item in externo['items']:
            items_dto.append(ItemDTO(
                producto_id=uuid.UUID(item['producto_id']),
                cantidad=item['cantidad'],
                precio=0.0,  # Se obtendrá del servicio de productos
                total=0.0   # Calculado
            ))
        
        return PedidoDTO(
            cliente_id=uuid.UUID(externo['cliente_id']),
            fecha_pedido=datetime.fromisoformat(externo['fecha_pedido']),
            estado=EstadoPedido(externo['estado']),
            items=items_dto,
            total=0.0)  # Calculado
    
    def dto_a_externo(self, dto: PedidoDTO) -> dict:
        # Convertir items de ItemDTOs a diccionarios
        items_externo = []
        for item in dto.items:
            items_externo.append({
                'producto_id': str(item.producto_id),
                'cantidad': item.cantidad,
                'precio': item.precio,
                'total': item.total
            })
        
        return {
            'id': str(dto.id),
            'cliente_id': str(dto.cliente_id),
            'fecha_pedido': dto.fecha_pedido.isoformat(),
            'estado': dto.estado.value,
            'items': items_externo,
            'total': dto.total}

class MapeadorPedido(RepMap):
    def obtener_tipo(self) -> type:
        return PedidoDTO.__class__

    def entidad_a_dto(self, entidad: Pedido) -> PedidoDTO:
        # Convertir items de entidades de dominio a ItemDTOs
        items_dto = []
        for item in entidad.items:
            items_dto.append(ItemDTO(
                producto_id=item.producto_id,
                cantidad=item.cantidad,
                precio=item.precio,
                total=item.total
            ))
        
        return PedidoDTO(
            id=entidad.id,
            cliente_id=entidad.cliente_id,
            fecha_pedido=entidad.fecha_pedido,
            estado=entidad.estado,
            items=items_dto,
            total=entidad.total)
        
    def dto_a_entidad(self, dto: PedidoDTO) -> Pedido:
        # Convertir items de ItemDTOs a entidades de dominio
        from modulos.ventas.dominio.entidades import Item
        items_entidad = []
        for item in dto.items:
            items_entidad.append(Item(
                producto_id=item.producto_id,
                cantidad=item.cantidad,
                precio=item.precio,
                total=item.total
            ))
        
        return Pedido(
            cliente_id=dto.cliente_id,
            fecha_pedido=dto.fecha_pedido,
            estado=dto.estado,
            items=items_entidad,
            total=dto.total)
