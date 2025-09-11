from modulos.ventas.dominio.repositorios import RepositorioPedido
from modulos.ventas.dominio.fabricas import FabricaPedido
from modulos.ventas.dominio.entidades import Pedido
from modulos.ventas.infraestructura.mapeadores import MapeadorPedido
from modulos.ventas.infraestructura.dto import Pedido as PedidoModelo
from config.config.db import db
from uuid import UUID

class RepositorioPedidoSQLite(RepositorioPedido):
    def __init__(self):
        self._fabrica_pedido = FabricaPedido()
    
    @property
    def fabrica_pedido(self):
        return self._fabrica_pedido

    def agregar(self, pedido: Pedido):
        pedido_dto = self._fabrica_pedido.crear_objeto(pedido, MapeadorPedido())
        db.session.add(pedido_dto)
        db.session.commit()

    def actualizar(self, pedido: Pedido):
        # TODO: Implementar
        raise NotImplementedError("No implementado")
    
    def eliminar(self, id: UUID):
        # TODO: Implementar
        raise NotImplementedError("No implementado")
    
    def obtener_por_id(self, id: UUID) -> Pedido:
        pedido_modelo = PedidoModelo.query.filter_by(id=id).first()
        if pedido_modelo:
            return MapeadorPedido().dto_a_entidad(pedido_modelo)
        return None
    
    def obtener_todos(self) -> list[Pedido]:
        pedido_modelos = PedidoModelo.query.all()
        return [MapeadorPedido().dto_a_entidad(pedido_modelo) for pedido_modelo in pedido_modelos]