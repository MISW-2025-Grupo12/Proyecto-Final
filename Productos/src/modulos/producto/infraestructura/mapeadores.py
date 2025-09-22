from seedwork.dominio.repositorios import Mapeador
from modulos.producto.dominio.entidades import Producto as ProductoDominio
from modulos.producto.dominio.entidades import TipoProducto as TipoProductoDominio
from modulos.producto.infraestructura.dto_postgres import (
    ProductoComando as ProductoComandoModelo,
    TipoProductoComando as TipoProductoComandoModelo,
    ProductoConsulta as ProductoConsultaModelo,
    TipoProductoConsulta as TipoProductoConsultaModelo
)
from modulos.producto.dominio.objetos_valor import Nombre, Descripcion, Precio, Stock, Marca, Lote
from datetime import datetime

class MapeadorProductoComando(Mapeador):
    """Mapeador para modelos de comandos PostgreSQL"""

    def obtener_tipo(self) -> type:
        return ProductoComandoModelo

    def entidad_a_dto(self, entidad: ProductoDominio) -> ProductoComandoModelo:
        return ProductoComandoModelo(
            id=entidad.id,
            nombre=entidad.nombre.nombre,
            descripcion=entidad.descripcion.descripcion,
            precio=entidad.precio.precio,
            stock=entidad.stock.stock,
            marca=entidad.marca.nombre,
            lote=entidad.lote.codigo,
            tipo_producto_id=entidad.tipo.id
        )

    def dto_a_entidad(self, dto: ProductoComandoModelo) -> ProductoDominio:
        print(f"Modelo comando a entidad: {dto}")
        
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

class MapeadorProductoConsulta(Mapeador):
    """Mapeador para modelos de consultas PostgreSQL (denormalizados)"""

    def obtener_tipo(self) -> type:
        return ProductoConsultaModelo

    def entidad_a_dto(self, entidad: ProductoDominio) -> ProductoConsultaModelo:
        return ProductoConsultaModelo(
            id=entidad.id,
            nombre=entidad.nombre.nombre,
            descripcion=entidad.descripcion.descripcion,
            precio=entidad.precio.precio,
            stock=entidad.stock.stock,
            marca=entidad.marca.nombre,
            lote=entidad.lote.codigo,
            tipo_producto_id=entidad.tipo.id,
            tipo_producto_nombre=entidad.tipo.nombre.nombre,
            tipo_producto_descripcion=entidad.tipo.descripcion.descripcion,
            created_at=datetime.now(),
            updated_at=datetime.now()
        )

    def dto_a_entidad(self, dto: ProductoConsultaModelo) -> ProductoDominio:
        print(f"Modelo consulta a entidad: {dto}")
        
        # Crear el tipo de producto de dominio usando los campos denormalizados
        tipo_producto_dominio = TipoProductoDominio(
            id=dto.tipo_producto_id,
            nombre=Nombre(dto.tipo_producto_nombre),
            descripcion=Descripcion(dto.tipo_producto_descripcion)
        )
        
        return ProductoDominio(
            id=dto.id,
            nombre=Nombre(dto.nombre),
            tipo=tipo_producto_dominio,
            descripcion=Descripcion(dto.descripcion),
            precio=Precio(dto.precio),
            stock=Stock(dto.stock),
            marca=Marca(dto.marca),
            lote=Lote(dto.lote, dto.created_at or datetime.now(), dto.updated_at or datetime.now())
        )

class MapeadorTipoProductoComando(Mapeador):
    """Mapeador para tipos de producto de comandos PostgreSQL"""

    def obtener_tipo(self) -> type:
        return TipoProductoComandoModelo

    def entidad_a_dto(self, entidad: TipoProductoDominio) -> TipoProductoComandoModelo:
        return TipoProductoComandoModelo(
            id=entidad.id,
            nombre=entidad.nombre.nombre,
            descripcion=entidad.descripcion.descripcion
        )

    def dto_a_entidad(self, dto: TipoProductoComandoModelo) -> TipoProductoDominio:
        return TipoProductoDominio(
            id=dto.id,
            nombre=Nombre(dto.nombre),
            descripcion=Descripcion(dto.descripcion)
        )

class MapeadorTipoProductoConsulta(Mapeador):
    """Mapeador para tipos de producto de consultas PostgreSQL"""

    def obtener_tipo(self) -> type:
        return TipoProductoConsultaModelo

    def entidad_a_dto(self, entidad: TipoProductoDominio) -> TipoProductoConsultaModelo:
        return TipoProductoConsultaModelo(
            id=entidad.id,
            nombre=entidad.nombre.nombre,
            descripcion=entidad.descripcion.descripcion,
            created_at=datetime.now(),
            updated_at=datetime.now(),
            cantidad_productos=0
        )

    def dto_a_entidad(self, dto: TipoProductoConsultaModelo) -> TipoProductoDominio:
        return TipoProductoDominio(
            id=dto.id,
            nombre=Nombre(dto.nombre),
            descripcion=Descripcion(dto.descripcion)
        )