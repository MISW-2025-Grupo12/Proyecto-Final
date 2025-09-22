import os
import sys
import logging

# Agregar el directorio src al path de Python para que las importaciones funcionen
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from flask import Flask, jsonify, redirect, render_template, request, url_for
from flask_swagger import swagger

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def importar_modelos_postgres():
    """Importa los modelos PostgreSQL para comandos y consultas"""
    try:
        from modulos.producto.infraestructura.dto_postgres import (
            # Modelos de comandos
            TipoProductoComando, ProductoComando,
            # Modelos de consultas
            ProductoConsulta, TipoProductoConsulta
        )
        logger.info("✅ Modelos PostgreSQL importados correctamente")
        logger.info("   �� Modelos de comandos: TipoProductoComando, ProductoComando")
        logger.info("   �� Modelos de consultas: ProductoConsulta, TipoProductoConsulta")
    except Exception as e:
        logger.error(f"❌ Error importando modelos PostgreSQL: {e}")
        raise

def inicializar_sistema_eventos(app):
    """Inicializa el sistema de eventos y pub/sub"""
    try:
        print("Inicializando sistema de eventos...")
        from seedwork.infraestructura.pubsub import PublicadorPubSub
        from seedwork.infraestructura.consumidor_pubsub import ConsumidorPubSub
        from seedwork.dominio.eventos import despachador_eventos
        
        # Crear y registrar el publicador Pub/Sub
        print("Creando publicador Pub/Sub...")
        publicador = PublicadorPubSub()
        print("Registrando publicador en el despachador...")
        despachador_eventos.registrar_publicador(publicador)
        print(f"✅ Publicador registrado. Total publicadores: {len(despachador_eventos._publicadores)}")
        publicador.crear_topics()
        
        # Crear y configurar el consumidor Pub/Sub
        print("Creando consumidor Pub/Sub...")
        consumidor = ConsumidorPubSub(app=app)
        print("Creando suscripciones...")
        consumidor.crear_suscripciones()
        print("Iniciando escucha de eventos...")
        consumidor.iniciar_escucha()
        
        logger.info("Sistema de eventos inicializado correctamente")
        print("✅ Sistema de eventos inicializado correctamente")
    except Exception as e:
        print(f"Error inicializando sistema de eventos: {e}")
        logger.warning(f"Error inicializando sistema de eventos: {e}")
        # No fallar la aplicación si el sistema de eventos no funciona

def create_app(configuracion=None):
    try:
        # Init la aplicacion de Flask
        app = Flask(__name__, instance_relative_config=True)
        logger.info("🚀 Aplicación Flask creada")

        # Configurar Flask para no redirigir automáticamente URLs sin barra final
        app.url_map.strict_slashes = False

        # Inicializar bases de datos PostgreSQL
        from config.config.db_postgres import init_databases, create_all_tables
        
        init_databases(app)
        importar_modelos_postgres()

        with app.app_context():
            create_all_tables(app)
            logger.info("✅ Bases de datos PostgreSQL inicializadas")

        # Inicializar sistema de eventos
        inicializar_sistema_eventos(app)
        
        # Importar handlers de eventos para registrarlos
        import modulos.producto.aplicacion.event_handlers.pedido_creado_handler

        # Importa Blueprints
        from . import producto

        # Registro de Blueprints
        app.register_blueprint(producto.bp)

        @app.route("/spec")
        def spec():
            swag = swagger(app)
            swag['info']['version'] = "1.0"
            swag['info']['title'] = "Productos API - PostgreSQL CQRS"
            return jsonify(swag)

        @app.route("/health")
        def health():
            return {
                "status": "up",
                "database": "postgresql",
                "mode": "cqrs",
                "commands_db": "productos_commands",
                "queries_db": "productos_queries"
            }

        logger.info("✅ Aplicación Flask configurada correctamente con PostgreSQL CQRS")
        return app
        
    except Exception as e:
        logger.error(f"❌ Error creando la aplicación: {e}")
        raise

# Crear la aplicación para que Flask pueda encontrarla
app = create_app()