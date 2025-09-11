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

def importar_modelos_alchemy():
    try:
        from modulos.ventas.infraestructura.dto import db
        from modulos.ventas.infraestructura.dto import Pedido, Item
        logger.info("Modelos de SQLAlchemy importados correctamente")
    except Exception as e:
        logger.error(f"Error importando modelos: {e}")
        raise
    
    return db



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