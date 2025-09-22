# src/modulos/producto/infraestructura/repositorios_postgres.py
from seedwork.dominio.repositorios import Repositorio
from abc import ABC
from modulos.producto.dominio.repositorios_comando import RepositorioProductoComando, RepositorioTipoProductoComando
from modulos.producto.dominio.repositorios_consulta import RepositorioProductoConsulta, RepositorioTipoProductoConsulta
from modulos.producto.dominio.fabricas import FabricaProducto, FabricaTipoProducto
from modulos.producto.dominio.entidades import Producto, TipoProducto
from modulos.producto.infraestructura.mapeadores import (
    MapeadorProductoComando, MapeadorTipoProductoComando,
    MapeadorProductoConsulta, MapeadorTipoProductoConsulta
)
from modulos.producto.infraestructura.dto_postgres import (
    ProductoComando as ProductoComandoModelo, 
    TipoProductoComando as TipoProductoComandoModelo,
    ProductoConsulta as ProductoConsultaModelo,
    TipoProductoConsulta as TipoProductoConsultaModelo
)
from config.config.db_postgres import db
from uuid import UUID

# =============================================================================
# CLASES BASE ORIGINALES (Para compatibilidad con código existente)
# =============================================================================

class RepositorioProducto(Repositorio, ABC):
    """Clase base abstracta para repositorios de productos"""
    pass

class RepositorioTipoProducto(Repositorio, ABC):
    """Clase base abstracta para repositorios de tipos de producto"""
    pass

# =============================================================================
# REPOSITORIOS DE COMANDOS (PostgreSQL - Base normalizada)
# =============================================================================

class RepositorioProductoComandoPostgreSQL(RepositorioProductoComando):
    """Implementación del repositorio de comandos para productos usando PostgreSQL"""
    
    def __init__(self):
        self._fabrica_producto = FabricaProducto()
        self._mapeador = MapeadorProductoComando()

    @property
    def fabrica_producto(self):
        return self._fabrica_producto

    def agregar(self, producto: Producto):
        print(f"[COMANDO-POSTGRES] Agregando producto: {producto}")
        
        # Verificar si el tipo de producto ya existe
        tipo_producto_existente = TipoProductoComandoModelo.query.filter_by(id=producto.tipo.id).first()
        tipo_producto_dto = None
        
        if not tipo_producto_existente:
            # Crear el tipo de producto si no existe
            tipo_producto_dto = TipoProductoComandoModelo(
                id=producto.tipo.id,
                nombre=producto.tipo.nombre.nombre,
                descripcion=producto.tipo.descripcion.descripcion
            )
            db.session.add(tipo_producto_dto)
        else:
            # Usar el tipo de producto existente
            tipo_producto_dto = tipo_producto_existente
        
        # Crear el producto
        producto_modelo = ProductoComandoModelo(
            id=producto.id,
            nombre=producto.nombre.nombre,
            descripcion=producto.descripcion.descripcion,
            precio=producto.precio.precio,
            stock=producto.stock.stock,
            marca=producto.marca.nombre,
            lote=producto.lote.codigo,
            tipo_producto_id=producto.tipo.id
        )
        
        db.session.add(producto_modelo)
        db.session.commit()
        
        # Sincronizar a la base de consultas
        self._sync_to_queries(producto_modelo, tipo_producto_dto)
        
        print(f"[COMANDO-POSTGRES] Producto agregado exitosamente: {producto.id}")

    def _sync_to_queries(self, producto_comando: ProductoComandoModelo, tipo_producto_comando: TipoProductoComandoModelo):
        """Sincroniza un producto de comandos a consultas"""
        print(f"[SYNC] Iniciando sincronización para producto {producto_comando.id} con stock {producto_comando.stock}")
        try:
            # Verificar si el tipo ya existe en consultas
            tipo_consulta = TipoProductoConsultaModelo.query.filter_by(id=tipo_producto_comando.id).first()
            if not tipo_consulta:
                tipo_consulta = TipoProductoConsultaModelo(
                    id=tipo_producto_comando.id,
                    nombre=tipo_producto_comando.nombre,
                    descripcion=tipo_producto_comando.descripcion,
                    created_at=tipo_producto_comando.created_at,
                    updated_at=tipo_producto_comando.updated_at,
                    cantidad_productos=0
                )
                db.session.add(tipo_consulta)
            
            # Verificar si el producto ya existe en consultas
            producto_consulta = ProductoConsultaModelo.query.filter_by(id=producto_comando.id).first()
            if producto_consulta:
                # Actualizar producto existente
                producto_consulta.nombre = producto_comando.nombre
                producto_consulta.descripcion = producto_comando.descripcion
                producto_consulta.precio = producto_comando.precio
                producto_consulta.stock = producto_comando.stock
                producto_consulta.marca = producto_comando.marca
                producto_consulta.lote = producto_comando.lote
                producto_consulta.tipo_producto_id = producto_comando.tipo_producto_id
                producto_consulta.tipo_producto_nombre = tipo_producto_comando.nombre
                producto_consulta.tipo_producto_descripcion = tipo_producto_comando.descripcion
                producto_consulta.updated_at = producto_comando.updated_at
                print(f"[SYNC] Producto actualizado en consultas: {producto_comando.id}")
            else:
                # Crear nuevo producto en consultas
                producto_consulta = ProductoConsultaModelo(
                    id=producto_comando.id,
                    nombre=producto_comando.nombre,
                    descripcion=producto_comando.descripcion,
                    precio=producto_comando.precio,
                    stock=producto_comando.stock,
                    marca=producto_comando.marca,
                    lote=producto_comando.lote,
                    tipo_producto_id=producto_comando.tipo_producto_id,
                    tipo_producto_nombre=tipo_producto_comando.nombre,
                    tipo_producto_descripcion=tipo_producto_comando.descripcion,
                    created_at=producto_comando.created_at,
                    updated_at=producto_comando.updated_at
                )
                db.session.add(producto_consulta)
                print(f"[SYNC] Producto creado en consultas: {producto_comando.id}")
            
            # Actualizar contador de productos
            tipo_consulta.cantidad_productos = ProductoConsultaModelo.query.filter_by(tipo_producto_id=tipo_producto_comando.id).count()
            
            db.session.commit()
            print(f"[SYNC] ✅ Sincronización completada exitosamente para producto {producto_comando.id}")
            
        except Exception as e:
            print(f"[SYNC] Error sincronizando producto: {e}")
            db.session.rollback()

    def actualizar(self, producto: Producto):
        print(f"[COMANDO-POSTGRES] Actualizando producto: {producto.id}")
        producto_modelo = ProductoComandoModelo.query.filter_by(id=producto.id).first()
        if producto_modelo:
            producto_modelo.nombre = producto.nombre.nombre
            producto_modelo.descripcion = producto.descripcion.descripcion
            producto_modelo.precio = producto.precio.precio
            producto_modelo.stock = producto.stock.stock
            producto_modelo.marca = producto.marca.nombre
            producto_modelo.lote = producto.lote.codigo
            db.session.commit()
            print(f"[COMANDO-POSTGRES] Producto actualizado exitosamente: {producto.id}")
            
            # Sincronizar con la base de consultas
            if producto_modelo.tipo_producto_id:
                tipo_producto_modelo = TipoProductoComandoModelo.query.filter_by(id=producto_modelo.tipo_producto_id).first()
                if tipo_producto_modelo:
                    self._sync_to_queries(producto_modelo, tipo_producto_modelo)
        else:
            print(f"[COMANDO-POSTGRES] Producto no encontrado para actualizar: {producto.id}")
        return None
        
    def eliminar(self, id: UUID):
        print(f"[COMANDO-POSTGRES] Eliminando producto: {id}")
        producto_modelo = ProductoComandoModelo.query.filter_by(id=id).first()
        if producto_modelo:
            db.session.delete(producto_modelo)
            db.session.commit()
            print(f"[COMANDO-POSTGRES] Producto eliminado exitosamente: {id}")
        else:
            print(f"[COMANDO-POSTGRES] Producto no encontrado para eliminar: {id}")

    def obtener_por_id(self, id: UUID) -> Producto:
        """Obtiene un producto por ID para operaciones de comando"""
        producto_modelo = ProductoComandoModelo.query.filter_by(id=id).first()
        if producto_modelo:
            return self._mapeador.dto_a_entidad(producto_modelo)
        return None

class RepositorioTipoProductoComandoPostgreSQL(RepositorioTipoProductoComando):
    """Implementación del repositorio de comandos para tipos de producto usando PostgreSQL"""
    
    def __init__(self):
        self._fabrica_tipo_producto = FabricaTipoProducto()
        self._mapeador = MapeadorTipoProductoComando()

    @property
    def fabrica_tipo_producto(self):
        return self._fabrica_tipo_producto

    def agregar(self, tipo_producto: TipoProducto):
        print(f"[COMANDO-POSTGRES] Agregando tipo de producto: {tipo_producto}")
        
        tipo_producto_modelo = TipoProductoComandoModelo(
            id=tipo_producto.id,
            nombre=tipo_producto.nombre.nombre,
            descripcion=tipo_producto.descripcion.descripcion
        )
        
        db.session.add(tipo_producto_modelo)
        db.session.commit()
        
        # Sincronizar a la base de consultas
        self._sync_to_queries(tipo_producto_modelo)
        
        print(f"[COMANDO-POSTGRES] Tipo de producto agregado exitosamente: {tipo_producto.id}")

    def _sync_to_queries(self, tipo_producto_comando: TipoProductoComandoModelo):
        """Sincroniza un tipo de producto de comandos a consultas"""
        try:
            tipo_consulta = TipoProductoConsultaModelo(
                id=tipo_producto_comando.id,
                nombre=tipo_producto_comando.nombre,
                descripcion=tipo_producto_comando.descripcion,
                created_at=tipo_producto_comando.created_at,
                updated_at=tipo_producto_comando.updated_at,
                cantidad_productos=0
            )
            db.session.add(tipo_consulta)
            db.session.commit()
            print(f"[SYNC] Tipo de producto sincronizado a consultas: {tipo_producto_comando.id}")
            
        except Exception as e:
            print(f"[SYNC] Error sincronizando tipo de producto: {e}")
            db.session.rollback()

    def actualizar(self, tipo_producto: TipoProducto):
        print(f"[COMANDO-POSTGRES] Actualizando tipo de producto: {tipo_producto.id}")
        tipo_producto_modelo = TipoProductoComandoModelo.query.filter_by(id=tipo_producto.id).first()
        if tipo_producto_modelo:
            tipo_producto_modelo.nombre = tipo_producto.nombre.nombre
            tipo_producto_modelo.descripcion = tipo_producto.descripcion.descripcion
            db.session.commit()
            print(f"[COMANDO-POSTGRES] Tipo de producto actualizado exitosamente: {tipo_producto.id}")
            
            # Sincronizar con la base de consultas
            self._sync_to_queries(tipo_producto_modelo)
        else:
            print(f"[COMANDO-POSTGRES] Tipo de producto no encontrado para actualizar: {tipo_producto.id}")
        return None
        
    def eliminar(self, id: UUID):
        print(f"[COMANDO-POSTGRES] Eliminando tipo de producto: {id}")
        tipo_producto_modelo = TipoProductoComandoModelo.query.filter_by(id=id).first()
        if tipo_producto_modelo:
            db.session.delete(tipo_producto_modelo)
            db.session.commit()
            print(f"[COMANDO-POSTGRES] Tipo de producto eliminado exitosamente: {id}")
        else:
            print(f"[COMANDO-POSTGRES] Tipo de producto no encontrado para eliminar: {id}")

    def obtener_por_id(self, id: UUID) -> TipoProducto:
        """Obtiene un tipo de producto por ID para operaciones de comando"""
        tipo_producto_modelo = TipoProductoComandoModelo.query.filter_by(id=id).first()
        if tipo_producto_modelo:
            return self._mapeador.dto_a_entidad(tipo_producto_modelo)
        return None

# =============================================================================
# REPOSITORIOS DE CONSULTAS (PostgreSQL - Base denormalizada)
# =============================================================================

class RepositorioProductoConsultaPostgreSQL(RepositorioProductoConsulta):
    """Implementación del repositorio de consultas para productos usando PostgreSQL"""
    
    def __init__(self):
        self._mapeador = MapeadorProductoConsulta()
    
    def obtener_por_id(self, id: UUID) -> Producto:
        """Obtiene un producto por ID optimizado para consultas"""
        print(f"[CONSULTA-POSTGRES] Obteniendo producto por ID: {id}")
        producto_modelo = ProductoConsultaModelo.query.filter_by(id=id).first()
        if producto_modelo:
            producto = self._mapeador.dto_a_entidad(producto_modelo)
            print(f"[CONSULTA-POSTGRES] Producto encontrado: {producto.id}")
            return producto
        print(f"[CONSULTA-POSTGRES] Producto no encontrado: {id}")
        return None

    def obtener_todos(self) -> list[Producto]:
        """Obtiene todos los productos optimizado para consultas"""
        print(f"[CONSULTA-POSTGRES] Obteniendo todos los productos")
        producto_modelos = ProductoConsultaModelo.query.all()
        productos = [self._mapeador.dto_a_entidad(producto_modelo) for producto_modelo in producto_modelos]
        print(f"[CONSULTA-POSTGRES] Encontrados {len(productos)} productos")
        return productos


    # Métodos de escritura no disponibles en repositorio de consultas
    def agregar(self, producto: Producto):
        raise NotImplementedError("El repositorio de consultas no permite operaciones de escritura")

    def actualizar(self, producto: Producto):
        raise NotImplementedError("El repositorio de consultas no permite operaciones de escritura")

    def eliminar(self, id: UUID):
        raise NotImplementedError("El repositorio de consultas no permite operaciones de escritura")

class RepositorioTipoProductoConsultaPostgreSQL(RepositorioTipoProductoConsulta):
    """Implementación del repositorio de consultas para tipos de producto usando PostgreSQL"""
    
    def __init__(self):
        self._mapeador = MapeadorTipoProductoConsulta()
    
    def obtener_por_id(self, id: UUID) -> TipoProducto:
        """Obtiene un tipo de producto por ID optimizado para consultas"""
        print(f"[CONSULTA-POSTGRES] Obteniendo tipo de producto por ID: {id}")
        tipo_producto_modelo = TipoProductoConsultaModelo.query.filter_by(id=id).first()
        if tipo_producto_modelo:
            tipo_producto = self._mapeador.dto_a_entidad(tipo_producto_modelo)
            print(f"[CONSULTA-POSTGRES] Tipo de producto encontrado: {tipo_producto.id}")
            return tipo_producto
        print(f"[CONSULTA-POSTGRES] Tipo de producto no encontrado: {id}")
        return None

    def obtener_todos(self) -> list[TipoProducto]:
        """Obtiene todos los tipos de producto optimizado para consultas"""
        print(f"[CONSULTA-POSTGRES] Obteniendo todos los tipos de producto")
        tipo_producto_modelos = TipoProductoConsultaModelo.query.all()
        tipos_producto = [self._mapeador.dto_a_entidad(tipo_producto_modelo) for tipo_producto_modelo in tipo_producto_modelos]
        print(f"[CONSULTA-POSTGRES] Encontrados {len(tipos_producto)} tipos de producto")
        return tipos_producto

    # Métodos de escritura no disponibles en repositorio de consultas
    def agregar(self, tipo_producto: TipoProducto):
        raise NotImplementedError("El repositorio de consultas no permite operaciones de escritura")

    def actualizar(self, tipo_producto: TipoProducto):
        raise NotImplementedError("El repositorio de consultas no permite operaciones de escritura")

    def eliminar(self, id: UUID):
        raise NotImplementedError("El repositorio de consultas no permite operaciones de escritura")

