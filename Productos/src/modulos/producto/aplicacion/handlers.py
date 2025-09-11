from seedwork.aplicacion.comandos import ManejadorComando
from modulos.producto.aplicacion.comandos.crear_producto import CrearProductoComando
from modulos.producto.aplicacion.dto import ProductoDTO
from modulos.producto.aplicacion.mapeadores import MapeadorProductoDTOJson
from modulos.producto.aplicacion.servicios import ServicioProducto

class HandlerProductoIntegracion(ManejadorComando):
    def __init__(self):
        self._servicio = ServicioProducto()
        self._mapeador = MapeadorProductoDTOJson()
    
    def ejecutar(self, comando: CrearProductoComando) -> ProductoDTO:
        # Convertir comando a DTO
        producto_dto = ProductoDTO(
            nombre=comando.nombre,
            descripcion=comando.descripcion,
            precio=comando.precio,
            stock=comando.stock,
            marca=comando.marca,
            lote=comando.lote,
            tipo_producto_id=comando.tipo_producto_id
        )
        
        # Ejecutar la lógica de negocio
        return self._servicio.crear_producto(producto_dto)