from seedwork.aplicacion.dto import Mapeador as AppMap
from seedwork.dominio.repositorios import Mapeador as RepMap
from modulos.producto.aplicacion.dto import ProductoDTO, TipoProductoDTO
from modulos.producto.dominio.entidades import Producto
from modulos.producto.dominio.entidades import TipoProducto
from modulos.producto.dominio.objetos_valor import Nombre, Descripcion, Precio, Stock, Marca, Lote
from datetime import datetime
import uuid
from decimal import Decimal

class MapeadorProductoDTOJson(AppMap):

    def externo_a_dto(self, externo: dict) -> ProductoDTO:
        tipo_producto_id = externo.get('tipo_producto_id')
        if tipo_producto_id:
            tipo_producto_id = uuid.UUID(tipo_producto_id)
        
        return ProductoDTO(
            nombre=externo['nombre'],
            descripcion=externo['descripcion'],
            precio=externo['precio'],
            stock=externo['stock'],
            marca=externo['marca'],
            lote=externo['lote'],
            tipo_producto_id=tipo_producto_id)
    
    def dto_a_externo(self, dto: ProductoDTO) -> dict:
        # Convertir Decimal a float para serialización JSON
        precio = float(dto.precio) if isinstance(dto.precio, Decimal) else dto.precio
        
        return {
            'id': str(dto.id),
            'nombre': dto.nombre,
            'descripcion': dto.descripcion,
            'precio': precio,
            'stock': dto.stock,
            'marca': dto.marca,
            'lote': dto.lote,
            'tipo_producto_id': str(dto.tipo_producto_id) if dto.tipo_producto_id else None
        }

class MapeadorProducto(RepMap):
    def obtener_tipo(self) -> type:
        return ProductoDTO.__class__

    def entidad_a_dto(self, entidad: Producto) -> ProductoDTO:
        id = entidad.id
        nombre = entidad.nombre.nombre
        descripcion = entidad.descripcion.descripcion
        precio = entidad.precio.precio
        stock = entidad.stock.stock
        marca = entidad.marca.nombre
        lote = entidad.lote.codigo
        tipo_producto_id = entidad.tipo.id if entidad.tipo and entidad.tipo.id else None
        return ProductoDTO(id=id, nombre=nombre, descripcion=descripcion, precio=precio, stock=stock, marca=marca, lote=lote, tipo_producto_id=tipo_producto_id)

    def dto_a_entidad(self, dto: ProductoDTO, tipo_producto: TipoProducto = None) -> Producto:
        # Si no se proporciona el tipo de producto, crear uno básico
        if tipo_producto is None:
            tipo_producto = TipoProducto(
                id=dto.tipo_producto_id,
                nombre=Nombre("Tipo por defecto"),
                descripcion=Descripcion("Descripción por defecto")
            )
        
        return Producto(	
            id=dto.id,
            nombre=Nombre(dto.nombre),
            tipo=tipo_producto,
            descripcion=Descripcion(dto.descripcion),
            precio=Precio(dto.precio),
            stock=Stock(dto.stock),
            marca=Marca(dto.marca),
            lote=Lote(dto.lote, datetime.now(), datetime.now()))

class MapeadorTipoProductoDTOJson(AppMap):
    def externo_a_dto(self, externo: dict) -> TipoProductoDTO:
        return TipoProductoDTO(
            nombre=externo['nombre'],
            descripcion=externo['descripcion'],
            id=uuid.uuid4() 
        )
    
    def dto_a_externo(self, dto: TipoProductoDTO) -> dict:
        return {
            'id': str(dto.id) if dto.id else None,
            'nombre': dto.nombre,
            'descripcion': dto.descripcion}

class MapeadorTipoProducto(RepMap):
    def obtener_tipo(self) -> type:
        return TipoProductoDTO.__class__

    def entidad_a_dto(self, entidad: TipoProducto) -> TipoProductoDTO:
        return TipoProductoDTO(
            nombre=entidad.nombre.nombre,
            descripcion=entidad.descripcion.descripcion,
            id=entidad.id
        )
    
    def dto_a_entidad(self, dto: TipoProductoDTO) -> TipoProducto:
        return TipoProducto(
            id=dto.id,
            nombre=Nombre(dto.nombre),
            descripcion=Descripcion(dto.descripcion))