"""Publicador de eventos para Google Cloud Pub/Sub"""

import json
import logging
from typing import Dict, Any
from google.cloud import pubsub_v1
from google.auth.exceptions import DefaultCredentialsError
from medisupply.seedwork.dominio.eventos import PublicadorEventos, EventoDominio

logger = logging.getLogger(__name__)


class PublicadorPubSub(PublicadorEventos):
    """Publicador de eventos que envía mensajes a Google Cloud Pub/Sub"""
    
    def __init__(self, project_id: str = "medisupply-project", emulator_host: str = None):
        self.project_id = project_id
        # Usar la variable de entorno si está disponible, sino usar localhost por defecto
        import os
        self.emulator_host = emulator_host or os.environ.get('PUBSUB_EMULATOR_HOST', 'localhost:8085')
        self._publisher = None
        self._topics_creados = False
        self._initialize_publisher()
    
    def _initialize_publisher(self):
        """Inicializa el cliente de Pub/Sub"""
        try:
            # Configurar para usar el emulador
            import os
            os.environ['PUBSUB_EMULATOR_HOST'] = self.emulator_host
            
            self._publisher = pubsub_v1.PublisherClient()
            logger.info(f"Publicador Pub/Sub inicializado con emulador en {self.emulator_host}")
        except Exception as e:
            logger.warning(f"No se pudo inicializar publicador Pub/Sub: {e}")
            self._publisher = None
    
    def publicar(self, evento: EventoDominio):
        """Publica un evento a Pub/Sub"""
        print(f"PubSub: Iniciando publicación de evento {evento.__class__.__name__}")
        
        if not self._publisher:
            print("PubSub: Publicador no disponible, evento no publicado")
            logger.debug("Publicador Pub/Sub no disponible, evento no publicado")
            return
        
        try:
            print(f"🔧 PubSub: Publicador disponible, procediendo con la publicación")
            
            # Crear topics si no se han creado
            if not self._topics_creados:
                print("📁 PubSub: Creando topics necesarios...")
                self.crear_topics()
                self._topics_creados = True
                print("✅ PubSub: Topics creados exitosamente")
            else:
                print("ℹ️ PubSub: Topics ya existen, continuando...")
            
            # Determinar el topic basado en el tipo de evento
            topic_name = self._get_topic_name(evento)
            topic_path = self._publisher.topic_path(self.project_id, topic_name)
            print(f"📡 PubSub: Topic seleccionado: {topic_name} -> {topic_path}")
            
            # Serializar el evento
            mensaje_data = json.dumps(evento.to_dict()).encode('utf-8')
            print(f"📦 PubSub: Evento serializado, tamaño: {len(mensaje_data)} bytes")
            
            # Publicar el mensaje
            print(f"📤 PubSub: Enviando mensaje a Pub/Sub...")
            future = self._publisher.publish(topic_path, mensaje_data)
            message_id = future.result()
            
            print(f"✅ PubSub: Evento {evento.__class__.__name__} publicado con ID: {message_id}")
            print(f"📋 PubSub: Datos del evento: {evento.to_dict()}")
            logger.info(f"✅ Evento {evento.__class__.__name__} publicado con ID: {message_id}")
            logger.info(f"📋 Datos del evento: {evento.to_dict()}")
            
        except Exception as e:
            print(f"❌ PubSub: Error publicando evento {evento.__class__.__name__}: {e}")
            logger.warning(f"Error publicando evento {evento.__class__.__name__}: {e}")
    
    def _get_topic_name(self, evento: EventoDominio) -> str:
        """Determina el nombre del topic basado en el tipo de evento"""
        tipo_evento = evento.__class__.__name__
        
        # Mapeo de eventos a topics
        topic_mapping = {
            'ProductoCreado': 'productos-creados',
            'ProductoStockActualizado': 'productos-stock-actualizado',
            'TipoProductoCreado': 'tipos-productos-creados'
        }
        
        return topic_mapping.get(tipo_evento, 'eventos-generales')
    
    def crear_topics(self):
        """Crea los topics necesarios en Pub/Sub"""
        if not self._publisher:
            print("Publicador no disponible, no se pueden crear topics")
            logger.warning("Publicador no disponible, no se pueden crear topics")
            return
        
        topics = [
            'productos-creados',
            'productos-stock-actualizado', 
            'tipos-productos-creados',
            'eventos-generales'
        ]
        
        print(f"📁 PubSub: Creando {len(topics)} topics...")
        for topic_name in topics:
            try:
                topic_path = self._publisher.topic_path(self.project_id, topic_name)
                print(f"🔧 PubSub: Creando topic: {topic_name} -> {topic_path}")
                self._publisher.create_topic(request={"name": topic_path})
                print(f"✅ PubSub: Topic {topic_name} creado exitosamente")
                logger.info(f"Topic {topic_name} creado exitosamente")
            except Exception as e:
                print(f"⚠️ PubSub: Topic {topic_name} ya existe o error creándolo: {e}")
                logger.warning(f"Topic {topic_name} ya existe o error creándolo: {e}")