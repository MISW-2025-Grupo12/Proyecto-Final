"""
Consumidor de eventos para Google Cloud Pub/Sub
"""

import json
import logging
import threading
import time
from typing import Dict, Any
from google.cloud import pubsub_v1
from google.auth.exceptions import DefaultCredentialsError
from seedwork.dominio.eventos import EventoDominio, despachador_eventos
from seedwork.aplicacion.eventos import ejecutar_evento

logger = logging.getLogger(__name__)

class ConsumidorPubSub:
    """Consumidor de eventos que recibe mensajes de Google Cloud Pub/Sub"""
    
    def __init__(self, project_id: str = "medisupply-project", emulator_host: str = None, app=None):
        self.project_id = project_id
        import os
        self.emulator_host = emulator_host or os.environ.get('PUBSUB_EMULATOR_HOST', 'localhost:8085')
        self.app = app
        self._subscriber = None
        self._subscriptions = {}
        self._initialize_subscriber()
    
    def _initialize_subscriber(self):
        """Inicializa el cliente de Pub/Sub"""
        try:
            import os
            os.environ['PUBSUB_EMULATOR_HOST'] = self.emulator_host
            
            self._subscriber = pubsub_v1.SubscriberClient()
            logger.info(f"Consumidor Pub/Sub inicializado con emulador en {self.emulator_host}")
        except Exception as e:
            logger.warning(f"No se pudo inicializar consumidor Pub/Sub: {e}")
            self._subscriber = None
    
    def crear_suscripciones(self):
        """Crea las suscripciones necesarias para escuchar eventos"""
        if not self._subscriber:
            logger.warning("No se puede crear suscripciones: cliente no inicializado")
            return
        
        # Topics que este servicio necesita escuchar
        topics_a_escuchar = [
            'pedidos-creados'
        ]
        
        for topic_name in topics_a_escuchar:
            try:
                self._crear_suscripcion(topic_name)
            except Exception as e:
                logger.warning(f"Error creando suscripción para {topic_name}: {e}")
    
    def _crear_suscripcion(self, topic_name: str):
        """Crea una suscripción para un topic específico"""
        if not self._subscriber:
            return
        
        topic_path = self._subscriber.topic_path(self.project_id, topic_name)
        subscription_path = self._subscriber.subscription_path(
            self.project_id, f"{topic_name}-productos-sub"
        )
        
        try:
            # Crear la suscripción
            self._subscriber.create_subscription(
                request={"name": subscription_path, "topic": topic_path}
            )
            logger.info(f"✅ Suscripción creada: {subscription_path}")
            
            # Guardar referencia para poder iniciar escucha
            self._subscriptions[topic_name] = subscription_path
            
        except Exception as e:
            if "already exists" in str(e):
                logger.info(f"ℹ️ Suscripción ya existe: {subscription_path}")
                self._subscriptions[topic_name] = subscription_path
            else:
                logger.error(f"❌ Error creando suscripción {topic_name}: {e}")
    
    def iniciar_escucha(self):
        """Inicia la escucha de eventos en background"""
        if not self._subscriber:
            logger.warning("No se puede iniciar escucha: cliente no inicializado")
            return
        
        for topic_name, subscription_path in self._subscriptions.items():
            try:
                # Crear hilo para escuchar cada suscripción
                thread = threading.Thread(
                    target=self._escuchar_suscripcion,
                    args=(subscription_path, topic_name),
                    daemon=True
                )
                thread.start()
                logger.info(f"🎧 Iniciada escucha para {topic_name}")
                
            except Exception as e:
                logger.error(f"❌ Error iniciando escucha para {topic_name}: {e}")
    
    def _escuchar_suscripcion(self, subscription_path: str, topic_name: str):
        """Escucha mensajes de una suscripción específica"""
        try:
            def callback(message):
                try:
                    # Decodificar el mensaje
                    data = json.loads(message.data.decode('utf-8'))
                    
                    logger.info(f"📨 Recibido evento {data.get('tipo_evento')} desde {topic_name}")
                    
                    # Crear evento de dominio desde los datos
                    evento = self._crear_evento_desde_datos(data)
                    
                    if evento:
                        # Procesar el evento usando el sistema local con contexto de Flask
                        logger.info(f"🔄 Procesando evento {evento.__class__.__name__}")
                        
                        # Usar el contexto de la aplicación Flask si está disponible
                        if self.app:
                            with self.app.app_context():
                                ejecutar_evento(evento)
                        else:
                            ejecutar_evento(evento)
                        
                        logger.info(f"✅ Evento {evento.__class__.__name__} procesado exitosamente")
                    
                    # Confirmar que el mensaje fue procesado
                    message.ack()
                    
                except Exception as e:
                    logger.error(f"❌ Error procesando mensaje: {e}")
                    message.nack()
            
            # Usar subscribe() con la API correcta
            streaming_pull_future = self._subscriber.subscribe(
                subscription_path,
                callback=callback,
                flow_control=pubsub_v1.types.FlowControl(max_messages=10)
            )
            
            logger.info(f"✅ Escucha activa para {topic_name}")
            
            # Mantener el hilo vivo
            streaming_pull_future.result()
                
        except Exception as e:
            logger.error(f"❌ Error en escucha de {topic_name}: {e}")
    
    def _crear_evento_desde_datos(self, data: Dict[str, Any]) -> EventoDominio:
        """Crea un evento de dominio desde los datos del mensaje"""
        try:
            tipo_evento = data.get('tipo_evento')
            
            if tipo_evento == 'PedidoCreado':
                # Importar el evento PedidoCreado local
                from modulos.producto.dominio.eventos_externos import PedidoCreado, EstadoPedido
                from datetime import datetime
                import uuid
                
                datos_evento = data.get('datos', {})
                
                # Crear el evento PedidoCreado
                evento = PedidoCreado(
                    pedido_id=uuid.UUID(datos_evento.get('pedido_id')),
                    cliente_id=uuid.UUID(datos_evento.get('cliente_id')),
                    fecha_pedido=datetime.fromisoformat(datos_evento.get('fecha_pedido')) if datos_evento.get('fecha_pedido') else datetime.now(),
                    estado=EstadoPedido(datos_evento.get('estado')),
                    items_info=datos_evento.get('items_info', []),
                    total=float(datos_evento.get('total', 0))
                )
                
                return evento
            
            else:
                logger.warning(f"⚠️ Tipo de evento no reconocido: {tipo_evento}")
                return None
                
        except Exception as e:
            logger.error(f"❌ Error creando evento desde datos: {e}")
            return None