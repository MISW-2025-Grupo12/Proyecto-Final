
import json
import os
import signal
import sys
from google.cloud import pubsub_v1

class EventViewer:
    def __init__(self):
        self.running = True
        self.subscriber = None
        
        self.project_id = os.getenv('GCP_PROJECT_ID', 'desarrolloswcloud')
        self.use_emulator = os.getenv('USE_PUBSUB_EMULATOR', 'false').lower() == 'true'
        self.emulator_host = os.getenv('PUBSUB_EMULATOR_HOST', 'localhost:8085')
        
        self.topics = [
            'productos-stock-actualizado',
            'pedidos-creados'
        ]
        
       
        if not self._setup_authentication():
            print("❌ Error configurando autenticación. Saliendo...")
            sys.exit(1)
        
        signal.signal(signal.SIGINT, self.signal_handler)
        signal.signal(signal.SIGTERM, self.signal_handler)
    
    def _setup_authentication(self):
        """Configura la autenticación para GCP"""
        if self.use_emulator:
            # Configurar para usar el emulador
            os.environ['PUBSUB_EMULATOR_HOST'] = self.emulator_host
            print(f"🔧 Usando emulador de Pub/Sub en {self.emulator_host}")
        else:
            # Configurar para usar GCP
            credentials_path = os.getenv('GOOGLE_APPLICATION_CREDENTIALS')
            if credentials_path:
                print(f"🔧 Usando credenciales desde: {credentials_path}")
                # Verificar que el archivo existe
                if os.path.exists(credentials_path):
                    print(f"✅ Archivo de credenciales encontrado")
                else:
                    print(f"❌ Archivo de credenciales no encontrado: {credentials_path}")
                    return False
            elif os.getenv('GCP_SERVICE_ACCOUNT_KEY'):
                print("🔧 Usando credenciales desde variable de entorno GCP_SERVICE_ACCOUNT_KEY")
            else:
                print("❌ No se encontraron credenciales de GCP")
                print("💡 Configura GOOGLE_APPLICATION_CREDENTIALS o GCP_SERVICE_ACCOUNT_KEY")
                return False
            
            print(f"🔧 Proyecto: {self.project_id}")
        return True
    
    def signal_handler(self, signum, frame):
        """Maneja las señales para salir limpiamente"""
        print("\n👋 Deteniendo visualizador de eventos...")
        self.running = False
        sys.exit(0)
    
    def callback(self, message):
        """Procesa cada mensaje recibido"""
        try:
           
            data = json.loads(message.data.decode('utf-8'))
            
            print(f"\n📨 EVENTO RECIBIDO - {data.get('tipo_evento', 'Desconocido')}")
            print(f"🆔 ID del Evento: {data.get('id')}")
            print(f"📅 Fecha: {data.get('fecha_evento')}")
            print(f"🔢 Versión: {data.get('version')}")
            print(f"📋 Datos del Evento:")
            
           
            datos_evento = data.get('datos', {})
            for key, value in datos_evento.items():
                print(f"   • {key}: {value}")
            
            print("-" * 60)
            
           
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
            
           
            self.setup_subscriptions()
            
            print("\n🚀 Listo para recibir eventos...")
            print("💡 Crea productos en tu API para ver los eventos aquí")
            print("📡 Presiona Ctrl+C para detener")
            print("-" * 60)
            
           
            streaming_futures = []
            
            for topic_name in self.topics:
                subscription_path = self.subscriber.subscription_path(
                    self.project_id, f"{topic_name}-sub-continuo"
                )
                
                try:
                    print(f"🎧 Iniciando escucha para {topic_name}...")
                    
                   
                    streaming_pull_future = self.subscriber.subscribe(
                        subscription_path,
                        callback=self.callback
                    )
                    streaming_futures.append(streaming_pull_future)
                    
                except Exception as e:
                    print(f"⚠️  Error iniciando escucha para {topic_name}: {e}")
            

            try:
               
                for future in streaming_futures:
                    future.result()
            except KeyboardInterrupt:
                print("\n👋 Deteniendo visualizador de eventos...")
               
                for future in streaming_futures:
                    future.cancel()
                    future.result()

def main():
    """Función principal"""
    viewer = EventViewer()
    viewer.start_listening()

if __name__ == "__main__":
    main()
