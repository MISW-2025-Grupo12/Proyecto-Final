
from dataclasses import dataclass
from seedwork.aplicacion.consultas import Consulta
import uuid

@dataclass
class ObtenerProductoPorIdConsulta(Consulta):
    id: uuid.UUID
