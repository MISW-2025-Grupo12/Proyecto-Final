from typing import Dict, List
from seedwork.dominio.eventos import ManejadorEvento, PublicadorEventos, EventoDominio
from functools import singledispatch

class DespachadorEventos:
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

@singledispatch
def ejecutar_evento(evento):
    """Función genérica para ejecutar eventos usando singledispatch"""
    raise NotImplementedError(f"No existe implementacion para el evento de tipo: {type(evento).__name__}")