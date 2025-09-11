#!/usr/bin/env python3
"""
Script mejorado para ver eventos publicados en Pub/Sub de forma continua
"""

import json
import os
import signal
import sys
from google.cloud import pubsub_v1

class EventViewer:
    def __init__(self):
        self.running = True
        self.subscriber = None
        self.project_id = "medisupply-project"
        self.topics = [
            'productos-creados',
            'productos-stock-actualizado', 
            'tipos-productos-creados'
        ]
        
        # Configurar emulador
        os.environ['PUBSUB_EMULATOR_HOST'] = 'localhost:8085'
        
        # Configurar manejo de señales para salir limpiamente
        signal.signal(signal.SIGINT, self.signal_handler)
        signal.signal(signal.SIGTERM, self.signal_handler)
    
    def signal_handler(self, signum, frame):
        """Maneja las señales para salir limpiamente"""
        print("\n👋 Deteniendo visualizador de eventos...")
        self.running = False
        sys.exit(0)
    
    def callback(self, message):
        """Procesa cada mensaje recibido"""
        try:
            # Decodificar el mensaje
            data = json.loads(message.data.decode('utf-8'))
            
            print(f"\n📨 EVENTO RECIBIDO - {data.get('tipo_evento', 'Desconocido')}")
            print(f"🆔 ID del Evento: {data.get('id')}")
            print(f"📅 Fecha: {data.get('fecha_evento')}")
            print(f"🔢 Versión: {data.get('version')}")
            print(f"📋 Datos del Evento:")
            
            # Mostrar datos específicos del evento
            datos_evento = data.get('datos', {})
            for key, value in datos_evento.items():
                print(f"   • {key}: {value}")
            
            print("-" * 60)
            
            # Confirmar que el mensaje fue procesado
            message.ack()
            
        except Exception as e:
            print(f"❌ Error procesando mensaje: {e}")
            message.nack()
    
    def setup_subscriptions(self):
        """Configura las suscripciones para cada topic"""
        print("🔧 Configurando suscripciones...")
        
        for topic_name in self.topics:
            subscription_path = self.subscriber.subscription_path(
                self.project_id, f"{topic_name}-sub-continuo"
            )
            topic_path = self.subscriber.topic_path(self.project_id, topic_name)
            
            try:
                # Crear suscripción si no existe
                self.subscriber.create_subscription(
                    request={"name": subscription_path, "topic": topic_path}
                )
                print(f"✅ Suscripción creada para {topic_name}")
            except Exception as e:
                if "already exists" in str(e):
                    print(f"ℹ️  Suscripción para {topic_name} ya existe")
                else:
                    print(f"⚠️  Error con {topic_name}: {e}")
    
    def start_listening(self):
        """Inicia la escucha continua de eventos"""
        with pubsub_v1.SubscriberClient() as subscriber:
            self.subscriber = subscriber
            
            # Configurar suscripciones
            self.setup_subscriptions()
            
            print("\n🚀 Listo para recibir eventos...")
            print("💡 Crea productos en tu API para ver los eventos aquí")
            print("📡 Presiona Ctrl+C para detener")
            print("-" * 60)
            
            # Crear suscripciones para cada topic
            streaming_futures = []
            
            for topic_name in self.topics:
                subscription_path = self.subscriber.subscription_path(
                    self.project_id, f"{topic_name}-sub-continuo"
                )
                
                try:
                    print(f"🎧 Iniciando escucha para {topic_name}...")
                    
                    # Crear suscripción continua
                    streaming_pull_future = self.subscriber.subscribe(
                        subscription_path,
                        callback=self.callback
                    )
                    streaming_futures.append(streaming_pull_future)
                    
                except Exception as e:
                    print(f"⚠️  Error iniciando escucha para {topic_name}: {e}")
            
            # Mantener el script corriendo
            try:
                # Esperar a que todas las suscripciones terminen
                for future in streaming_futures:
                    future.result()
            except KeyboardInterrupt:
                print("\n👋 Deteniendo visualizador de eventos...")
                # Cancelar todas las suscripciones
                for future in streaming_futures:
                    future.cancel()
                    future.result()

def main():
    """Función principal"""
    viewer = EventViewer()
    viewer.start_listening()

if __name__ == "__main__":
    main()
