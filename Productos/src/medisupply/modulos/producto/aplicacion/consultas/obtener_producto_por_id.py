
from dataclasses import dataclass
from medisupply.seedwork.aplicacion.consultas import Consulta
import uuid

@dataclass
class ObtenerProductoPorIdConsulta(Consulta):
    id: uuid.UUID
