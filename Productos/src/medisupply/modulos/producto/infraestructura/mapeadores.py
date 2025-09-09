from medisupply.seedwork.dominio.repositorios import Mapeador
from medisupply.modulos.producto.dominio.entidades import Producto as ProductoDominio
from medisupply.modulos.producto.dominio.entidades import TipoProducto as TipoProductoDominio
from medisupply.modulos.producto.infraestructura.dto import Producto as ProductoModelo
from medisupply.modulos.producto.infraestructura.dto import TipoProducto as TipoProductoModelo
from medisupply.modulos.producto.dominio.objetos_valor import Nombre, Descripcion, Precio, Stock, Marca, Lote
from datetime import datetime

class MapeadorProducto(Mapeador):

    def obtener_tipo(self) -> type:
        return ProductoModelo

    def entidad_a_dto(self, entidad: ProductoDominio) -> ProductoModelo:
        return ProductoModelo(
            id=entidad.id,
            nombre=entidad.nombre.nombre,
            descripcion=entidad.descripcion.descripcion,
            precio=entidad.precio.precio,
            stock=entidad.stock.stock,
            marca=entidad.marca.nombre,
            lote=entidad.lote.codigo,
            tipo_producto_id=entidad.tipo.id
        )

    def dto_a_entidad(self, dto: ProductoModelo) -> ProductoDominio:
        print(f"Modelo a entidad infraestructura: {dto}")
        
        # Crear el tipo de producto de dominio
        tipo_producto_dominio = TipoProductoDominio(
            id=dto.tipo_producto.id,
            nombre=Nombre(dto.tipo_producto.nombre),
            descripcion=Descripcion(dto.tipo_producto.descripcion)
        )
        
        return ProductoDominio(
            id=dto.id,
            nombre=Nombre(dto.nombre),
            tipo=tipo_producto_dominio,
            descripcion=Descripcion(dto.descripcion),
            precio=Precio(dto.precio),
            stock=Stock(dto.stock),
            marca=Marca(dto.marca),
            lote=Lote(dto.lote, datetime.now(), datetime.now())
        )
    
class MapeadorTipoProducto(Mapeador):
    def obtener_tipo(self) -> type:
        return TipoProductoModelo

    def entidad_a_dto(self, entidad: TipoProductoDominio) -> TipoProductoModelo:
        return TipoProductoModelo(
            id=entidad.id,
            nombre=entidad.nombre.nombre,
            descripcion=entidad.descripcion.descripcion)

    def dto_a_entidad(self, dto: TipoProductoModelo) -> TipoProductoDominio:
        return TipoProductoDominio(
            id=dto.id,
            nombre=Nombre(dto.nombre),
            descripcion=Descripcion(dto.descripcion))
    