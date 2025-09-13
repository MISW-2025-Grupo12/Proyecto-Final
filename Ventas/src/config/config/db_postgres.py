# src/config/config/db_postgres.py
from flask_sqlalchemy import SQLAlchemy
from flask import Flask
import os
import json

# Una sola instancia de SQLAlchemy para manejar múltiples bases de datos
db = SQLAlchemy()

def init_databases(app: Flask):
    """Inicializa las bases de datos PostgreSQL con múltiples binds"""
    
    # URLs de conexión desde variables de entorno
    commands_db_url = os.getenv(
        'COMMANDS_DATABASE_URL', 
        'postgresql://postgres:password@postgres-commands:5432/ventas_commands'
    )
    queries_db_url = os.getenv(
        'QUERIES_DATABASE_URL', 
        'postgresql://postgres:password@postgres-queries:5432/ventas_queries'
    )
    
    # Configurar SQLAlchemy con múltiples binds
    app.config['SQLALCHEMY_DATABASE_URI'] = commands_db_url  # Base de datos por defecto
    app.config['SQLALCHEMY_BINDS'] = {
        'commands': commands_db_url,
        'queries': queries_db_url
    }
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    # Inicializar SQLAlchemy con la aplicación
    db.init_app(app)
    
    print(f"✅ Bases de datos configuradas:")
    print(f"   📝 Commands: {commands_db_url}")
    print(f"   📊 Queries: {queries_db_url}")

def create_all_tables():
    """Crea todas las tablas en ambas bases de datos"""
    try:
        # Importar modelos para que estén registrados en metadata
        from modulos.ventas.infraestructura.dto_postgres import (
            # Modelos de comandos
            PedidoComando, ItemComando,
            # Modelos de consultas
            PedidoConsulta, ItemConsulta
        )
        
        print("🔨 Creando tablas de comandos...")
        # Crear tablas de comandos usando bind específico
        PedidoComando.__table__.create(bind=db.get_engine(bind_key='commands'), checkfirst=True)
        ItemComando.__table__.create(bind=db.get_engine(bind_key='commands'), checkfirst=True)
        print("✅ Tablas de comandos creadas")
        
        print("🔨 Creando tablas de consultas...")
        # Crear tablas de consultas usando bind específico
        PedidoConsulta.__table__.create(bind=db.get_engine(bind_key='queries'), checkfirst=True)
        ItemConsulta.__table__.create(bind=db.get_engine(bind_key='queries'), checkfirst=True)
        print("✅ Tablas de consultas creadas")
        
        # Sincronizar datos iniciales si es necesario
        sync_initial_data()
        
    except Exception as e:
        print(f"❌ Error creando tablas: {e}")
        raise

def sync_initial_data():
    """Sincroniza datos iniciales entre las bases de datos"""
    try:
        # Importar modelos
        from modulos.ventas.infraestructura.dto_postgres import (
            PedidoComando, ItemComando,
            PedidoConsulta, ItemConsulta
        )
        
        # Obtener todos los pedidos de la base de comandos
        pedidos_comando = PedidoComando.query.all()
        
        for pedido_comando in pedidos_comando:
            # Verificar si ya existe en consultas
            pedido_consulta_existente = PedidoConsulta.query.filter_by(id=pedido_comando.id).first()
            
            if not pedido_consulta_existente:
                # Crear pedido desnormalizado para consultas
                pedido_consulta = PedidoConsulta(
                    id=pedido_comando.id,
                    cliente_id=pedido_comando.cliente_id,
                    fecha_pedido=pedido_comando.fecha_pedido,
                    estado=pedido_comando.estado,
                    total=pedido_comando.total,
                    # Campos desnormalizados
                    cantidad_items=len(pedido_comando.items),
                    items_detalle=json.dumps([{
                        'producto_id': str(item.producto_id),
                        'cantidad': item.cantidad,
                        'precio': float(item.precio),
                        'total': float(item.total)
                    } for item in pedido_comando.items])
                )
                
                db.session.add(pedido_consulta)
        
        db.session.commit()
        print("✅ Datos iniciales sincronizados")
        
    except Exception as e:
        print(f"⚠️ Error sincronizando datos iniciales: {e}")
        db.session.rollback()

# Exportar instancias para uso en repositorios
db_commands = db
db_queries = db
