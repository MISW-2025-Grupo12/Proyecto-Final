import os
import logging

from flask import Flask, jsonify, redirect, render_template, request, url_for
from flask_swagger import swagger

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Identifica el directorio base
basedir = os.path.abspath(os.path.dirname(__file__))

def importar_modelos_alchemy():
    try:
        from modulos.producto.infraestructura.dto import db
        from modulos.producto.infraestructura.dto import Producto, TipoProducto
        logger.info("Modelos de SQLAlchemy importados correctamente")
    except Exception as e:
        logger.error(f"Error importando modelos: {e}")
        raise

def inicializar_sistema_eventos():
    """Inicializa el sistema de eventos y pub/sub"""
    try:
        print("Inicializando sistema de eventos...")
        from seedwork.infraestructura.pubsub import PublicadorPubSub
        from seedwork.dominio.eventos import despachador_eventos
        
        # Crear y registrar el publicador Pub/Sub
        print("Creando publicador Pub/Sub...")
        publicador = PublicadorPubSub()
        print("Registrando publicador en el despachador...")
        despachador_eventos.registrar_publicador(publicador)
        print(f"✅ Publicador registrado. Total publicadores: {len(despachador_eventos._publicadores)}")
        publicador.crear_topics()
        

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
        logger.info("Aplicación Flask creada")

        if configuracion is not None and configuracion["TESTING"]:
            app.config['SQLALCHEMY_DATABASE_URI'] =\
                'sqlite:///' + configuracion["DATABASE"]
        
        # Configuracion de BD
        else:
            app.config['SQLALCHEMY_DATABASE_URI'] =\
                'sqlite:///' + os.path.join(basedir, 'database.db')
        app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
        
        # Configurar Flask para no redirigir automáticamente URLs sin barra final
        app.url_map.strict_slashes = False

         # Inicializa la DB
        from config.config.db import init_db, db
        
        init_db(app)
        importar_modelos_alchemy()

        with app.app_context():
            db.create_all()
            logger.info("Base de datos inicializada")

        inicializar_sistema_eventos()

         # Importa Blueprints
        from . import producto

        # Registro de Blueprints
        app.register_blueprint(producto.bp)

        @app.route("/spec")
        def spec():
            swag = swagger(app)
            swag['info']['version'] = "1.0"
            swag['info']['title'] = "Productos API"
            return jsonify(swag)

        @app.route("/health")
        def health():
            return {"status": "up"}

        logger.info("Aplicación Flask configurada correctamente")
        return app
        
    except Exception as e:
        logger.error(f"Error creando la aplicación: {e}")
        raise

# Crear la aplicación para que Flask pueda encontrarla
app = create_app()