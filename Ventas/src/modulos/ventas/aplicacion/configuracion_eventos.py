"""
Configuración de eventos para el módulo de ventas.
Esta capa de aplicación configura las dependencias entre dominio e infraestructura.
"""

import logging
from seedwork.infraestructura.pubsub import PublicadorPubSub
from seedwork.dominio.eventos import despachador_eventos

logger = logging.getLogger(__name__)

def configurar_sistema_eventos():
    """Configura el sistema de eventos registrando el publicador Pub/Sub"""
    try:
        # Crear instancia del publicador
        publicador_pubsub = PublicadorPubSub()
        
        # Registrar el publicador en el despachador global
        despachador_eventos.registrar_publicador(publicador_pubsub)
        
        logger.info("✅ Sistema de eventos configurado correctamente")
        logger.info("📡 Publicador Pub/Sub registrado en despachador global")
        
        return True
        
    except Exception as e:
        logger.error(f"❌ Error configurando sistema de eventos: {e}")
        return False
