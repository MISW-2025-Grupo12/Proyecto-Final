#!/usr/bin/env python3
"""
Script para configurar Google Cloud Platform Pub/Sub
"""

import os
import sys
import json
import logging
from google.cloud import pubsub_v1

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class GCPSetup:
    def __init__(self, project_id: str = None):
        self.project_id = project_id or os.getenv('GCP_PROJECT_ID', 'desarrolloswcloud')
        self.publisher = None
        self.subscriber = None
        self._initialize_clients()
    
    def _initialize_clients(self):
        """Inicializa los clientes de Pub/Sub"""
        try:
            self._setup_authentication()
            self.publisher = pubsub_v1.PublisherClient()
            self.subscriber = pubsub_v1.SubscriberClient()
            logger.info(f"Clientes de Pub/Sub inicializados para proyecto: {self.project_id}")
        except Exception as e:
            logger.error(f"Error inicializando clientes de Pub/Sub: {e}")
            sys.exit(1)
    
    def _setup_authentication(self):
        """Configura la autenticación para GCP"""
        if os.getenv('GOOGLE_APPLICATION_CREDENTIALS'):
            logger.info("Usando credenciales desde GOOGLE_APPLICATION_CREDENTIALS")
            return
        
        service_account_key = os.getenv('GCP_SERVICE_ACCOUNT_KEY')
        if service_account_key:
            try:
                json.loads(service_account_key)
                import tempfile
                with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
                    f.write(service_account_key)
                    os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = f.name
                    logger.info("Credenciales de GCP configuradas desde variable de entorno")
            except json.JSONDecodeError:
                logger.error("GCP_SERVICE_ACCOUNT_KEY no es un JSON válido")
                sys.exit(1)
            except Exception as e:
                logger.error(f"Error configurando credenciales de GCP: {e}")
                sys.exit(1)
        else:
            logger.info("Usando Application Default Credentials (ADC) para GCP")
    
    def create_topics(self):
        """Crea los topics necesarios"""
        topics = [
            'productos-stock-actualizado',
            'pedidos-creados'
        ]
        
        logger.info(f"Creando {len(topics)} topics...")
        
        for topic_name in topics:
            try:
                topic_path = self.publisher.topic_path(self.project_id, topic_name)
                self.publisher.create_topic(request={"name": topic_path})
                logger.info(f"✅ Topic '{topic_name}' creado exitosamente")
                
            except Exception as e:
                if "already exists" in str(e):
                    logger.info(f"ℹ️ Topic '{topic_name}' ya existe")
                else:
                    logger.error(f"❌ Error creando topic '{topic_name}': {e}")
    
    def create_subscriptions(self):
        """Crea las suscripciones necesarias"""
        subscriptions = [
            {
                'topic': 'pedidos-creados',
                'subscription': 'pedidos-creados-productos-sub',
                'description': 'Suscripción para el servicio de productos'
            }
        ]
        
        logger.info(f"Creando {len(subscriptions)} suscripciones...")
        
        for sub_config in subscriptions:
            try:
                topic_path = self.publisher.topic_path(self.project_id, sub_config['topic'])
                subscription_path = self.subscriber.subscription_path(
                    self.project_id, sub_config['subscription']
                )
                
                self.subscriber.create_subscription(
                    request={
                        "name": subscription_path, 
                        "topic": topic_path,
                        "ack_deadline_seconds": 60
                    }
                )
                logger.info(f"✅ Suscripción '{sub_config['subscription']}' creada exitosamente")
                
            except Exception as e:
                if "already exists" in str(e):
                    logger.info(f"ℹ️ Suscripción '{sub_config['subscription']}' ya existe")
                else:
                    logger.error(f"❌ Error creando suscripción '{sub_config['subscription']}': {e}")
    
    def list_topics(self):
        """Lista todos los topics del proyecto"""
        logger.info("Listando topics del proyecto...")
        
        try:
            project_path = f"projects/{self.project_id}"
            topics = self.publisher.list_topics(request={"project": project_path})
            
            topic_list = list(topics)
            if topic_list:
                logger.info(f"Topics encontrados ({len(topic_list)}):")
                for topic in topic_list:
                    topic_name = topic.name.split('/')[-1]
                    logger.info(f"  - {topic_name}")
            else:
                logger.info("No se encontraron topics")
                
        except Exception as e:
            logger.error(f"Error listando topics: {e}")
    
    def list_subscriptions(self):
        """Lista todas las suscripciones del proyecto"""
        logger.info("Listando suscripciones del proyecto...")
        
        try:
            project_path = f"projects/{self.project_id}"
            subscriptions = self.subscriber.list_subscriptions(request={"project": project_path})
            
            sub_list = list(subscriptions)
            if sub_list:
                logger.info(f"Suscripciones encontradas ({len(sub_list)}):")
                for subscription in sub_list:
                    sub_name = subscription.name.split('/')[-1]
                    topic_name = subscription.topic.split('/')[-1]
                    logger.info(f"  - {sub_name} (topic: {topic_name})")
            else:
                logger.info("No se encontraron suscripciones")
                
        except Exception as e:
            logger.error(f"Error listando suscripciones: {e}")

def main():
    """Función principal"""
    if len(sys.argv) < 2:
        print("Uso: python setup-gcp.py <comando>")
        print("Comandos disponibles:")
        print("  create-topics     - Crear todos los topics necesarios")
        print("  create-subs       - Crear todas las suscripciones necesarias")
        print("  setup             - Crear topics y suscripciones")
        print("  list-topics       - Listar topics existentes")
        print("  list-subs         - Listar suscripciones existentes")
        sys.exit(1)
    
    command = sys.argv[1]
    
    try:
        setup = GCPSetup()
        
        if command == "create-topics":
            setup.create_topics()
        elif command == "create-subs":
            setup.create_subscriptions()
        elif command == "setup":
            setup.create_topics()
            setup.create_subscriptions()
        elif command == "list-topics":
            setup.list_topics()
        elif command == "list-subs":
            setup.list_subscriptions()
        else:
            print(f"Comando desconocido: {command}")
            sys.exit(1)
            
    except Exception as e:
        logger.error(f"Error ejecutando comando '{command}': {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
