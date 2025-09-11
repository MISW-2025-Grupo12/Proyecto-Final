from seedwork.aplicacion.comandos import ManejadorComando
from modulos.ventas.aplicacion.comandos.crear_pedido import CrearPedido
from modulos.ventas.aplicacion.dto import PedidoDTO
from modulos.ventas.aplicacion.mapeadores import MapeadorPedidoDTOJson
from modulos.ventas.aplicacion.servicios import ServicioPedido


class HandlerPedidoIntegracion(ManejadorComando):
    def __init__(self):
        self._servicio = ServicioPedido()
        self._mapeador = MapeadorPedidoDTOJson()
    
    def ejecutar(self, comando: CrearPedido) -> PedidoDTO:
        # Convertir comando a DTO
        pedido_dto = PedidoDTO(
            cliente_id=comando.cliente_id,
            fecha_pedido=comando.fecha_pedido,
            estado=comando.estado,
            items=comando.items,
            total=comando.total)
    
        return self._servicio.crear_pedido(pedido_dto)