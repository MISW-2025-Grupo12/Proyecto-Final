from modulos.producto.dominio.repositorios import RepositorioProducto, RepositorioTipoProducto
from modulos.producto.dominio.fabricas import FabricaProducto, FabricaTipoProducto
from modulos.producto.dominio.entidades import Producto, TipoProducto
from modulos.producto.infraestructura.mapeadores import MapeadorProducto, MapeadorTipoProducto
from config.config.db import db
from modulos.producto.infraestructura.dto import TipoProducto as TipoProductoModelo, Producto as ProductoModelo
from uuid import UUID

class RepositorioProductoSQLite(RepositorioProducto):
    print(f"Repositorio producto SQLite")
    def __init__(self):
        self._fabrica_producto = FabricaProducto()

    @property
    def fabrica_producto(self):
        return self._fabrica_producto

    def agregar(self, producto: Producto):
        print(f"Agregando producto: {producto}")
        
        # Verificar si el tipo de producto ya existe
        tipo_producto_existente = TipoProductoModelo.query.filter_by(id=producto.tipo.id).first()
        if not tipo_producto_existente:
            # Crear el tipo de producto si no existe
            tipo_producto_dto = TipoProductoModelo(
                id=producto.tipo.id,
                nombre=producto.tipo.nombre.nombre,
                descripcion=producto.tipo.descripcion.descripcion
            )
            db.session.add(tipo_producto_dto)
        
        # Crear el producto
        producto_dto = self._fabrica_producto.crear_objeto(producto, MapeadorProducto())
        db.session.add(producto_dto)
        db.session.commit()

    def actualizar(self, producto: Producto):
        producto_modelo = ProductoModelo.query.filter_by(id=producto.id).first()
        if producto_modelo:
            producto_modelo.nombre = producto.nombre.nombre
            producto_modelo.descripcion = producto.descripcion.descripcion
            producto_modelo.precio = producto.precio.precio
            producto_modelo.stock = producto.stock.stock
            producto_modelo.marca = producto.marca.nombre
            producto_modelo.lote = producto.lote.codigo
            db.session.commit()
        return None
        
    def eliminar(self, id: UUID):
        producto_modelo = ProductoModelo.query.filter_by(id=id).first()
        if producto_modelo:
            db.session.delete(producto_modelo)
            db.session.commit()

    def obtener_por_id(self, id: UUID) -> Producto:
        producto_modelo = ProductoModelo.query.filter_by(id=id).first()
        if producto_modelo:
            return MapeadorProducto().dto_a_entidad(producto_modelo)
        return None

    def obtener_todos(self) -> list[Producto]:
        producto_modelos = ProductoModelo.query.all()
        return [MapeadorProducto().dto_a_entidad(producto_modelo) for producto_modelo in producto_modelos]

class RepositorioTipoProductoSQLite(RepositorioTipoProducto):
    def __init__(self):
        self._fabrica_tipo_producto = FabricaTipoProducto()
        
    @property
    def fabrica_tipo_producto(self):
        return self._fabrica_tipo_producto

    def agregar(self, tipo_producto: TipoProducto):
        tipo_producto_dto = self._fabrica_tipo_producto.crear_objeto(tipo_producto, MapeadorTipoProducto())
        db.session.add(tipo_producto_dto)
        db.session.commit()

    def actualizar(self, tipo_producto: TipoProducto):
        # TODO: Implementar
        raise NotImplementedError("No implementado")

    def eliminar(self, id: UUID):
        # TODO: Implementar
        raise NotImplementedError("No implementado")
    
    def obtener_por_id(self, id: UUID) -> TipoProducto:
        tipo_producto_modelo = TipoProductoModelo.query.filter_by(id=id).first()
        if tipo_producto_modelo:
            return MapeadorTipoProducto().dto_a_entidad(tipo_producto_modelo)
        return None
    
    def obtener_todos(self) -> list[TipoProducto]:
        tipo_producto_modelos = TipoProductoModelo.query.all()
        return [MapeadorTipoProducto().dto_a_entidad(tipo_producto_modelo) for tipo_producto_modelo in tipo_producto_modelos]