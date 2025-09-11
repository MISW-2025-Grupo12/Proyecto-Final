
from dataclasses import dataclass
from seedwork.aplicacion.consultas import Consulta
import uuid

@dataclass
class ObtenerProductosPorTipoConsulta(Consulta):
    tipo_producto_id: uuid.UUID
