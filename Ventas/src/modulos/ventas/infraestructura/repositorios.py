import json
from modulos.ventas.dominio.repositorios import RepositorioPedido
from modulos.ventas.dominio.repositorios_comando import RepositorioPedidoComando
from modulos.ventas.dominio.repositorios_consulta import RepositorioPedidoConsulta
from modulos.ventas.dominio.fabricas import FabricaPedido
from modulos.ventas.dominio.entidades import Pedido
from modulos.ventas.infraestructura.mapeadores import MapeadorPedido
from modulos.ventas.infraestructura.mapeadores_postgres import (
    MapeadorPedidoComando, MapeadorPedidoConsulta
)
# Usando modelos PostgreSQL en lugar del modelo SQLAlchemy antiguo
from modulos.ventas.infraestructura.dto_postgres import (
    PedidoComando, ItemComando, PedidoConsulta, ItemConsulta
)
from config.config.db import db
from config.config.db_postgres import db as db_postgres
from uuid import UUID
from datetime import datetime

# =============================================================================
# REPOSITORIOS POSTGRESQL CQRS
# =============================================================================

class RepositorioPedidoComandoPostgreSQL(RepositorioPedidoComando):
    """Implementación del repositorio de comandos para pedidos usando PostgreSQL"""
    
    def __init__(self):
        self._mapeador = MapeadorPedidoComando()
    
    def agregar(self, pedido: Pedido):
        """Agrega un pedido a la base de datos de comandos"""
        try:
            # Crear pedido en base de comandos
            pedido_modelo = self._mapeador.entidad_a_dto(pedido)
            db_postgres.session.add(pedido_modelo)
            db_postgres.session.flush()  # Flush para obtener el ID del pedido
            
            # Crear items asociados usando el ID del pedido del modelo
            for item in pedido.items:
                item_modelo = ItemComando(
                    pedido_id=pedido_modelo.id,  # Usar el ID del modelo, no de la entidad
                    producto_id=item.producto_id,
                    cantidad=item.cantidad,
                    precio=item.precio,
                    total=item.total
                )
                db_postgres.session.add(item_modelo)
            
            db_postgres.session.commit()
            
            # Sincronizar con base de consultas
            self._sync_to_queries(pedido_modelo)
            
        except Exception as e:
            db_postgres.session.rollback()
            raise e
    
    def actualizar(self, pedido: Pedido):
        """Actualiza un pedido en la base de datos de comandos"""
        try:
            # Actualizar pedido
            pedido_modelo = PedidoComando.query.filter_by(id=pedido.id).first()
            if pedido_modelo:
                pedido_modelo.cliente_id = pedido.cliente_id
                pedido_modelo.fecha_pedido = pedido.fecha_pedido
                pedido_modelo.estado = pedido.estado.value
                pedido_modelo.total = pedido.total
                
                # Actualizar items (eliminar existentes y crear nuevos)
                ItemComando.query.filter_by(pedido_id=pedido_modelo.id).delete()
                for item in pedido.items:
                    item_modelo = ItemComando(
                        pedido_id=pedido_modelo.id,  # Usar el ID del modelo
                        producto_id=item.producto_id,
                        cantidad=item.cantidad,
                        precio=item.precio,
                        total=item.total
                    )
                    db_postgres.session.add(item_modelo)
                
                db_postgres.session.commit()
                
                # Sincronizar con base de consultas
                self._sync_to_queries(pedido_modelo)
                
        except Exception as e:
            db_postgres.session.rollback()
            raise e
    
    def eliminar(self, id: UUID):
        """Elimina un pedido de la base de datos de comandos"""
        try:
            # Eliminar de base de comandos
            PedidoComando.query.filter_by(id=id).delete()
            db_postgres.session.commit()
            
            # Eliminar de base de consultas
            PedidoConsulta.query.filter_by(id=id).delete()
            db_postgres.session.commit()
            
        except Exception as e:
            db_postgres.session.rollback()
            raise e
    
    def obtener_por_id(self, id: UUID) -> Pedido:
        """Obtiene un pedido por ID desde la base de comandos"""
        pedido_modelo = PedidoComando.query.filter_by(id=id).first()
        if pedido_modelo:
            return self._mapeador.dto_a_entidad(pedido_modelo)
        return None
    
    def obtener_todos(self) -> list[Pedido]:
        """Obtiene todos los pedidos desde la base de comandos"""
        pedido_modelos = PedidoComando.query.all()
        return [self._mapeador.dto_a_entidad(pedido_modelo) for pedido_modelo in pedido_modelos]
    
    def _sync_to_queries(self, pedido_modelo: PedidoComando):
        """Sincroniza un pedido desde comandos hacia consultas"""
        try:
            # Verificar si ya existe en consultas
            pedido_consulta_existente = PedidoConsulta.query.filter_by(id=pedido_modelo.id).first()
            
            if pedido_consulta_existente:
                # Actualizar existente
                pedido_consulta_existente.cliente_id = pedido_modelo.cliente_id
                pedido_consulta_existente.fecha_pedido = pedido_modelo.fecha_pedido
                pedido_consulta_existente.estado = pedido_modelo.estado
                pedido_consulta_existente.total = pedido_modelo.total
                pedido_consulta_existente.cantidad_items = len(pedido_modelo.items)
                pedido_consulta_existente.items_detalle = json.dumps([{
                    'producto_id': str(item.producto_id),
                    'cantidad': item.cantidad,
                    'precio': float(item.precio),
                    'total': float(item.total)
                } for item in pedido_modelo.items])
                pedido_consulta_existente.fecha_ultima_actualizacion = datetime.utcnow()
            else:
                # Crear nuevo
                pedido_consulta = PedidoConsulta(
                    id=pedido_modelo.id,
                    cliente_id=pedido_modelo.cliente_id,
                    fecha_pedido=pedido_modelo.fecha_pedido,
                    estado=pedido_modelo.estado,
                    total=pedido_modelo.total,
                    cantidad_items=len(pedido_modelo.items),
                    items_detalle=json.dumps([{
                        'producto_id': str(item.producto_id),
                        'cantidad': item.cantidad,
                        'precio': float(item.precio),
                        'total': float(item.total)
                    } for item in pedido_modelo.items]),
                    fecha_ultima_actualizacion=datetime.utcnow()
                )
                db_postgres.session.add(pedido_consulta)
            
            db_postgres.session.commit()
            
        except Exception as e:
            print(f"⚠️ Error sincronizando pedido {pedido_modelo.id} a consultas: {e}")
            db_postgres.session.rollback()

class RepositorioPedidoConsultaPostgreSQL(RepositorioPedidoConsulta):
    """Implementación del repositorio de consultas para pedidos usando PostgreSQL"""
    
    def __init__(self):
        self._mapeador = MapeadorPedidoConsulta()
    
    def obtener_por_id(self, id: UUID) -> Pedido:
        """Obtiene un pedido por ID desde la base de consultas"""
        pedido_modelo = PedidoConsulta.query.filter_by(id=id).first()
        if pedido_modelo:
            return self._mapeador.dto_a_entidad(pedido_modelo)
        return None
    
    def obtener_todos(self) -> list[Pedido]:
        """Obtiene todos los pedidos desde la base de consultas"""
        pedido_modelos = PedidoConsulta.query.all()
        return [self._mapeador.dto_a_entidad(pedido_modelo) for pedido_modelo in pedido_modelos]
    
    def obtener_por_cliente(self, cliente_id: UUID) -> list[Pedido]:
        """Obtiene pedidos por cliente desde la base de consultas"""
        pedido_modelos = PedidoConsulta.query.filter_by(cliente_id=cliente_id).all()
        return [self._mapeador.dto_a_entidad(pedido_modelo) for pedido_modelo in pedido_modelos]
    
    def obtener_por_estado(self, estado: str) -> list[Pedido]:
        """Obtiene pedidos por estado desde la base de consultas"""
        pedido_modelos = PedidoConsulta.query.filter_by(estado=estado).all()
        return [self._mapeador.dto_a_entidad(pedido_modelo) for pedido_modelo in pedido_modelos]
    
    def obtener_pedidos_con_total_mayor(self, total_minimo: float) -> list[Pedido]:
        """Obtiene pedidos con total mayor al especificado desde la base de consultas"""
        pedido_modelos = PedidoConsulta.query.filter(PedidoConsulta.total >= total_minimo).all()
        return [self._mapeador.dto_a_entidad(pedido_modelo) for pedido_modelo in pedido_modelos]

    def actualizar(self):
        ##todo: implementar
        raise NotImplementedError("No implementado")

    def eliminar(self, id: UUID):
        ##todo: implementar
        raise NotImplementedError("No implementado")
    
    def agregar(self, pedido: Pedido):
        ##todo: implementar
        raise NotImplementedError("No implementado")