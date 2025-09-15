from seedwork.dominio.reglas import ReglaNegocio
from datetime import datetime
from .entidades import EstadoPedido


class ClienteIdNoPuedeSerVacio(ReglaNegocio):
    cliente_id: any
    def __init__(self, cliente_id, mensaje='El ID del cliente no puede ser vacio'):
        super().__init__(mensaje)
        self.cliente_id = cliente_id

    def es_valido(self) -> bool:
        return self.cliente_id is not None
    
class FechaPedidoNoPuedeSerVacia(ReglaNegocio):
    fecha: datetime
    def __init__(self, fecha, mensaje='La fecha del pedido no puede ser vacia'):
        super().__init__(mensaje)
        self.fecha = fecha

    def es_valido(self) -> bool:
        return self.fecha is not None and self.fecha != ''

class EstadoPedidoNoPuedeSerVacio(ReglaNegocio):
    estado: EstadoPedido
    def __init__(self, estado, mensaje='El estado del pedido no puede ser vacio'):
        super().__init__(mensaje)
        self.estado = estado

    def es_valido(self) -> bool:
        return self.estado is not None