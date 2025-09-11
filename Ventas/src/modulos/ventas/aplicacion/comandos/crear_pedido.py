from dataclasses import dataclass
from seedwork.aplicacion.comandos import Comando, ejecutar_comando
import uuid
from datetime import datetime
from typing import List
from modulos.ventas.aplicacion.dto import ItemDTO, EstadoPedido, PedidoDTO
from modulos.ventas.aplicacion.mapeadores import MapeadorPedido
from modulos.ventas.dominio.repositorios import RepositorioPedido
from modulos.ventas.dominio.fabricas import FabricaPedido
from modulos.ventas.aplicacion.comandos.base import PedidoBaseHandler


@dataclass
class CrearPedido(Comando):
    cliente_id: uuid.UUID
    fecha_pedido: datetime
    estado: EstadoPedido
    items: List[ItemDTO]
    total: float

class CrearPedidoHandler(PedidoBaseHandler):
    def __init__(self):
        super().__init__()
        self._mapeador = MapeadorPedido()
    
    def handle(self, comando: CrearPedido) -> PedidoDTO:
        # 1. Obtener el cliente existente
        #repositorio_cliente = self.fabrica_repositorio.crear_objeto(RepositorioPedido)
        #cliente = repositorio_cliente.obtener_por_id(comando.cliente_id)
        
        #if not cliente:
        #    raise ValueError(f"Cliente con ID {comando.cliente_id} no encontrado")
        
        # 2. Crear el DTO del pedido
        pedido_dto = PedidoDTO(
            cliente_id=comando.cliente_id,
            fecha_pedido=comando.fecha_pedido,
            estado=comando.estado,
            items=comando.items,
            total=comando.total)
        
        # 3. Convertir DTO a entidad de dominio usando la fábrica
        pedido_entidad = self.fabrica_pedido.crear_objeto(pedido_dto, MapeadorPedido())
        
        # 4. Guardar en el repositorio
        repositorio_pedido = self.fabrica_repositorio.crear_objeto(RepositorioPedido)
        repositorio_pedido.agregar(pedido_entidad)
        
        # 5. Disparar evento de creación
        #pedido_entidad.disparar_evento_creacion()
        
        # 6. Retornar el DTO del pedido creado
        return pedido_dto 

@ejecutar_comando.register
def _(comando: CrearPedido):
    handler = CrearPedidoHandler()
    return handler.handle(comando)