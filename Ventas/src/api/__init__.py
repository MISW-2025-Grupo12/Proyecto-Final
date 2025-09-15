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
# Identifica el directorio base
basedir = os.path.abspath(os.path.dirname(__file__))

def importar_modelos_postgres():
    """Importa los modelos PostgreSQL para comandos y consultas"""
    try:
        from modulos.ventas.infraestructura.dto_postgres import (
            # Modelos de comandos
            PedidoComando, ItemComando,
            # Modelos de consultas
            PedidoConsulta, ItemConsulta
        )
        logger.info("✅ Modelos PostgreSQL importados correctamente")
    except Exception as e:
        logger.error(f"❌ Error importando modelos PostgreSQL: {e}")
        raise

def inicializar_sistema_eventos():
    """Inicializa el sistema de eventos"""
    try:
        from modulos.ventas.aplicacion.configuracion_eventos import configurar_sistema_eventos
        if configurar_sistema_eventos():
            logger.info("✅ Sistema de eventos inicializado correctamente")
        else:
            logger.warning("⚠️ Sistema de eventos no se pudo configurar")
    except Exception as e:
        logger.warning(f"⚠️ Sistema de eventos no disponible: {e}")



def create_app(configuracion=None):
    try:
        # Init la aplicacion de Flask
        app = Flask(__name__, instance_relative_config=True)
        logger.info("Aplicación Flask creada")

        # Configurar Flask para no redirigir automáticamente URLs sin barra final
        app.url_map.strict_slashes = False

        # Inicializar PostgreSQL con CQRS
        from config.config.db_postgres import init_databases, create_all_tables
        
        init_databases(app)
        importar_modelos_postgres()
        inicializar_sistema_eventos()

        with app.app_context():
            create_all_tables()
            logger.info("✅ Bases de datos PostgreSQL inicializadas")

        
        # Importa Blueprints
        from . import ventas

        # Registro de Blueprints
        app.register_blueprint(ventas.bp)

        @app.route("/spec")
        def spec():
            swag = swagger(app)
            swag['info']['version'] = "1.0"
            swag['info']['title'] = "Ventas API"
            return jsonify(swag)

        @app.route("/health")
        def health():
            return {"status": "up"}

        logger.info("Aplicación Flask configurada correctamente")
        return app
        
    except Exception as e:
        logger.error(f"Error creando la aplicación: {e}")
        raise