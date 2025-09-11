"""Sistema de eventos de dominio reusables parte del seedwork del proyecto

En este archivo usted encontrará las clases base para el manejo de eventos de dominio
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Any, Dict
import uuid
import json


@dataclass
class EventoDominio(ABC):
    """Clase base para todos los eventos de dominio"""
    id: uuid.UUID = field(default_factory=uuid.uuid4)
    fecha_evento: datetime = field(default_factory=datetime.now)
    version: int = field(default=1)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convierte el evento a diccionario para serialización"""
        return {
            'id': str(self.id),
            'fecha_evento': self.fecha_evento.isoformat(),
            'version': self.version,
            'tipo_evento': self.__class__.__name__,
            'datos': self._get_datos_evento()
        }
    
    @abstractmethod
    def _get_datos_evento(self) -> Dict[str, Any]:
        """Retorna los datos específicos del evento"""
        pass


class ManejadorEvento(ABC):
    """Interfaz para manejadores de eventos"""
    
    @abstractmethod
    def manejar(self, evento: EventoDominio):
        """Maneja un evento de dominio"""
        pass


class PublicadorEventos(ABC):
    """Interfaz para publicadores de eventos"""
    
    @abstractmethod
    def publicar(self, evento: EventoDominio):
        """Publica un evento de dominio"""
        pass


class DespachadorEventos:
    """Despachador de eventos que maneja la publicación y distribución"""
    
    def __init__(self):
        self._manejadores: Dict[str, List[ManejadorEvento]] = {}
        self._publicadores: List[PublicadorEventos] = []
    
    def registrar_manejador(self, tipo_evento: str, manejador: ManejadorEvento):
        """Registra un manejador para un tipo de evento"""
        if tipo_evento not in self._manejadores:
            self._manejadores[tipo_evento] = []
        self._manejadores[tipo_evento].append(manejador)
    
    def registrar_publicador(self, publicador: PublicadorEventos):
        """Registra un publicador de eventos"""
        self._publicadores.append(publicador)
    
    def publicar_evento(self, evento: EventoDominio):
        """Publica un evento y lo distribuye a los manejadores"""
        print(f"📡 Despachador: Recibido evento {evento.__class__.__name__} con ID: {evento.id}")
        print(f"📋 Despachador: Datos del evento: {evento.to_dict()}")
        
        # Publicar a sistemas externos
        print(f"🔄 Despachador: Publicando a {len(self._publicadores)} publicadores externos")
        for publicador in self._publicadores:
            print(f"📤 Despachador: Enviando a publicador: {publicador.__class__.__name__}")
            publicador.publicar(evento)
        
        # Distribuir a manejadores locales
        tipo_evento = evento.__class__.__name__
        print(f"🏠 Despachador: Buscando manejadores locales para {tipo_evento}")
        if tipo_evento in self._manejadores:
            print(f"✅ Despachador: Encontrados {len(self._manejadores[tipo_evento])} manejadores")
            for manejador in self._manejadores[tipo_evento]:
                print(f"🎯 Despachador: Ejecutando manejador: {manejador.__class__.__name__}")
                manejador.manejar(evento)
        else:
            print(f"⚠️ Despachador: No hay manejadores registrados para {tipo_evento}")


# Instancia global del despachador
despachador_eventos = DespachadorEventos()
