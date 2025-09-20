
from dataclasses import dataclass
from seedwork.aplicacion.comandos import Comando, ejecutar_comando
import uuid
import time
import logging
from datetime import datetime
from modulos.producto.aplicacion.dto import ProductoDTO
from modulos.producto.aplicacion.mapeadores import MapeadorProducto
from modulos.producto.dominio.repositorios_comando import RepositorioProductoComando, RepositorioTipoProductoComando
from modulos.producto.dominio.repositorios_consulta import RepositorioTipoProductoConsulta
from modulos.producto.aplicacion.comandos.base import ProductoComandoBaseHandler

logger = logging.getLogger(__name__)

@dataclass
class CrearProducto(Comando):
    nombre: str
    descripcion: str
    precio: float
    stock: int
    marca: str
    lote: str
    tipo_producto_id: uuid.UUID

class CrearProductoHandler(ProductoComandoBaseHandler):
    def __init__(self):
        super().__init__()
        self._mapeador = MapeadorProducto()

    def handle(self, comando: CrearProducto) -> ProductoDTO:
        start_time_command = time.time()
        timestamp = datetime.now().isoformat()
        
        logger.info(f"[METRICS-START] Crear producto - Timestamp: {timestamp} - Producto: {comando.nombre}")
        
        try:
            # 1. Obtener el tipo de producto existente (usando repositorio de consulta)
            start_validation = time.time()
            repositorio_tipo_consulta = self.fabrica_repositorio.crear_objeto(RepositorioTipoProductoConsulta)
            tipo_producto = repositorio_tipo_consulta.obtener_por_id(comando.tipo_producto_id)
            
            if not tipo_producto:
                raise ValueError(f"Tipo de producto con ID {comando.tipo_producto_id} no encontrado")
            
            validation_time = (time.time() - start_validation) * 1000
            logger.info(f"[METRICS-VALIDATION] Validación tipo producto - Latencia: {validation_time:.2f}ms")
            
            # 2. Crear el DTO del producto
            start_dto_creation = time.time()
            producto_dto = ProductoDTO(
                nombre=comando.nombre,
                descripcion=comando.descripcion,
                precio=comando.precio,
                stock=comando.stock,
                marca=comando.marca,
                lote=comando.lote,
                tipo_producto_id=comando.tipo_producto_id
            )
            
            # 3. Convertir DTO a entidad de dominio usando la fábrica
            producto_entidad = self.fabrica_producto.crear_objeto(producto_dto, MapeadorProducto())
            dto_creation_time = (time.time() - start_dto_creation) * 1000
            logger.info(f"[METRICS-DTO] Creación DTO y entidad - Latencia: {dto_creation_time:.2f}ms")
            
            # 4. Guardar en el repositorio de comandos (escritura)
            start_persistence = time.time()
            repositorio_producto_comando = self.fabrica_repositorio.crear_objeto(RepositorioProductoComando)
            repositorio_producto_comando.agregar(producto_entidad)
            persistence_time = (time.time() - start_persistence) * 1000
            logger.info(f"[METRICS-PERSISTENCE] Persistencia comando - Latencia: {persistence_time:.2f}ms")
            
            # 5. Disparar evento de creación
            start_event = time.time()
            producto_entidad.disparar_evento_creacion()
            event_time = (time.time() - start_event) * 1000
            logger.info(f"[METRICS-EVENT] Disparo evento creación - Latencia: {event_time:.2f}ms")
            
            # 6. Retornar el DTO del producto creado
            total_time = (time.time() - start_time_command) * 1000
            logger.info(f"[METRICS-END] Crear producto - Latencia total: {total_time:.2f}ms - Producto: {comando.nombre}")
            
            return producto_dto
            
        except Exception as e:
            total_time = (time.time() - start_time_command) * 1000
            logger.error(f"[METRICS-ERROR] Crear producto - Latencia: {total_time:.2f}ms - Error: {e} - Timestamp: {timestamp}")
            raise

@ejecutar_comando.register
def _(comando: CrearProducto):
    handler = CrearProductoHandler()
    return handler.handle(comando)