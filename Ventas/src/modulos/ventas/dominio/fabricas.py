from dataclasses import dataclass
from seedwork.dominio.fabricas import Fabrica
from seedwork.dominio.entidades import Entidad
from seedwork.dominio.repositorios import Mapeador
from .entidades import Pedido
from .reglas import ClienteIdNoPuedeSerVacio, FechaPedidoNoPuedeSerVacia, EstadoPedidoNoPuedeSerVacio
@dataclass
class FabricaPedido(Fabrica):
    def crear_objeto(self, obj: any, mapeador: Mapeador) -> any:
        if isinstance(obj, Entidad):
            return mapeador.entidad_a_dto(obj)
        else:
            print( "Fabricando pedido: ", obj)
            pedido: Pedido = mapeador.dto_a_entidad(obj)
            self.validar_regla(ClienteIdNoPuedeSerVacio(pedido.cliente_id))
            self.validar_regla(FechaPedidoNoPuedeSerVacia(pedido.fecha_pedido))
            self.validar_regla(EstadoPedidoNoPuedeSerVacio(pedido.estado))
            return pedido