from seedwork.dominio.repositorios import Mapeador
from modulos.ventas.dominio.entidades import Pedido, Item
from modulos.ventas.infraestructura.dto import Pedido as PedidoModelo, Item as ItemModelo


class MapeadorPedido(Mapeador):
    def obtener_tipo(self) -> type:
        return PedidoModelo

    def entidad_a_dto(self, entidad: Pedido) -> PedidoModelo:
        # Convertir items de dominio a modelos de SQLAlchemy
        items_modelo = []
        for item in entidad.items:
            items_modelo.append(ItemModelo(
                producto_id=item.producto_id,
                cantidad=item.cantidad,
                precio=item.precio,
                total=item.total
            ))
        
        return PedidoModelo(
            id=entidad.id,
            cliente_id=entidad.cliente_id,
            fecha_pedido=entidad.fecha_pedido,
            estado=entidad.estado.value if hasattr(entidad.estado, 'value') else str(entidad.estado),
            items=items_modelo,
            total=entidad.total)
        
    def dto_a_entidad(self, dto: PedidoModelo) -> Pedido:
        # Convertir items de modelos SQLAlchemy a entidades de dominio
        items_entidad = []
        for item in dto.items:
            items_entidad.append(Item(
                producto_id=item.producto_id,
                cantidad=item.cantidad,
                precio=item.precio,
                total=item.total
            ))
        
        # Convertir string de estado a enum
        from modulos.ventas.dominio.entidades import EstadoPedido
        estado_enum = EstadoPedido(dto.estado) if isinstance(dto.estado, str) else dto.estado
        
        return Pedido(
            id=dto.id,
            cliente_id=dto.cliente_id,
            fecha_pedido=dto.fecha_pedido,
            estado=estado_enum,
            items=items_entidad,
            total=dto.total)    
    