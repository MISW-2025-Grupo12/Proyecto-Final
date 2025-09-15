# src/config/config/db_postgres.py
from flask_sqlalchemy import SQLAlchemy
from flask import Flask
import os

# Una sola instancia de SQLAlchemy para manejar múltiples bases de datos
db = SQLAlchemy()

def init_databases(app: Flask):
    """Inicializa las bases de datos PostgreSQL con múltiples binds"""
    
    # URLs de conexión desde variables de entorno
    commands_db_url = os.getenv(
        'COMMANDS_DATABASE_URL', 
        'postgresql://postgres:password@localhost:5432/productos_commands'
    )
    
    queries_db_url = os.getenv(
        'QUERIES_DATABASE_URL', 
        'postgresql://postgres:password@localhost:5433/productos_queries'
    )
    
    # Configurar SQLAlchemy binds para múltiples bases de datos
    app.config['SQLALCHEMY_BINDS'] = {
        'commands': commands_db_url,
        'queries': queries_db_url
    }
    
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    # Inicializar la instancia única de SQLAlchemy
    db.init_app(app)
    
    print(f"[INFO] Bases de datos PostgreSQL configuradas:")
    print(f"   Comandos: {commands_db_url}")
    print(f"   Consultas: {queries_db_url}")

def create_all_tables(app: Flask):
    """Crea todas las tablas en ambas bases de datos"""
    with app.app_context():
        try:
            print("[INFO] Creando tablas de comandos...")
            # Importar modelos de comandos para asegurar que estén registrados
            from modulos.producto.infraestructura.dto_postgres import TipoProductoComando, ProductoComando
            
            # Crear tablas para modelos de comandos
            TipoProductoComando.__table__.create(bind=db.get_engine(bind_key='commands'), checkfirst=True)
            ProductoComando.__table__.create(bind=db.get_engine(bind_key='commands'), checkfirst=True)
            
            print("[INFO] Creando tablas de consultas...")
            # Importar modelos de consultas para asegurar que estén registrados
            from modulos.producto.infraestructura.dto_postgres import TipoProductoConsulta, ProductoConsulta
            
            # Crear tablas para modelos de consultas
            TipoProductoConsulta.__table__.create(bind=db.get_engine(bind_key='queries'), checkfirst=True)
            ProductoConsulta.__table__.create(bind=db.get_engine(bind_key='queries'), checkfirst=True)
            
            print("[INFO] Todas las tablas creadas exitosamente")
            
            # Sincronizar datos iniciales de comandos a consultas
            sync_commands_to_queries()
            
        except Exception as e:
            print(f"[ERROR] Error creando tablas: {e}")
            raise

def sync_commands_to_queries():
    """Sincroniza datos de la base de comandos a la base de consultas"""
    try:
        print("[INFO] Sincronizando datos de comandos a consultas...")
        
        # Importar modelos
        from modulos.producto.infraestructura.dto_postgres import (
            TipoProductoComando, ProductoComando,
            TipoProductoConsulta, ProductoConsulta
        )
        
        # Limpiar datos existentes en consultas
        ProductoConsulta.query.delete()
        TipoProductoConsulta.query.delete()
        
        # Copiar tipos de producto de comandos a consultas
        tipos_comando = TipoProductoComando.query.all()
        for tipo_comando in tipos_comando:
            tipo_consulta = TipoProductoConsulta(
                id=tipo_comando.id,
                nombre=tipo_comando.nombre,
                descripcion=tipo_comando.descripcion,
                created_at=tipo_comando.created_at,
                updated_at=tipo_comando.updated_at,
                cantidad_productos=0  # Se calculará después
            )
            db.session.add(tipo_consulta)
        
        # Copiar productos de comandos a consultas (denormalizados)
        productos_comando = ProductoComando.query.all()
        for producto_comando in productos_comando:
            # Buscar el tipo de producto correspondiente
            tipo_producto = TipoProductoComando.query.filter_by(id=producto_comando.tipo_producto_id).first()
            
            producto_consulta = ProductoConsulta(
                id=producto_comando.id,
                nombre=producto_comando.nombre,
                descripcion=producto_comando.descripcion,
                precio=producto_comando.precio,
                stock=producto_comando.stock,
                marca=producto_comando.marca,
                lote=producto_comando.lote,
                tipo_producto_id=producto_comando.tipo_producto_id,
                tipo_producto_nombre=tipo_producto.nombre if tipo_producto else "Desconocido",
                tipo_producto_descripcion=tipo_producto.descripcion if tipo_producto else "Desconocido",
                created_at=producto_comando.created_at,
                updated_at=producto_comando.updated_at
            )
            db.session.add(producto_consulta)
        
        # Calcular cantidad de productos por tipo
        for tipo_consulta in TipoProductoConsulta.query.all():
            cantidad = ProductoConsulta.query.filter_by(tipo_producto_id=tipo_consulta.id).count()
            tipo_consulta.cantidad_productos = cantidad
        
        db.session.commit()
        print("[INFO] Datos sincronizados exitosamente")
        
    except Exception as e:
        print(f"[ERROR] Error sincronizando datos: {e}")
        db.session.rollback()
        # No bajar la aplicación si la sincronización falla

# Alias para compatibilidad con el código existente
db_commands = db
db_queries = db