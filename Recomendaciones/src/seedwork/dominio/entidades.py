"""Entidades reusables parte del seedwork del proyecto

En este archivo usted encontrará las entidades reusables parte del seedwork del proyecto

"""

from dataclasses import dataclass, field
from .mixins import ValidarReglasMixin
from .reglas import IdEntidadEsInmutable
from .excepciones import IdDebeSerInmutableExcepcion
from datetime import datetime
import uuid

@dataclass
class Entidad:
    id: uuid.UUID = field(default_factory=uuid.uuid4, hash=True)
    _id: uuid.UUID = field(init=False, repr=False, hash=True)
    fecha_creacion: datetime = field(default_factory=datetime.now)
    fecha_actualizacion: datetime = field(default_factory=datetime.now)

    def __post_init__(self):
        self._id = self.id

    @classmethod
    def siguiente_id(cls) -> uuid.UUID:
        return uuid.uuid4()

    @property
    def id(self):
        return self._id

    @id.setter
    def id(self, id: uuid.UUID) -> None:
        if not IdEntidadEsInmutable(self).es_valido():
            raise IdDebeSerInmutableExcepcion()
        self._id = id
        

@dataclass
class AgregacionRaiz(Entidad, ValidarReglasMixin):
    def __post_init__(self):
        super().__post_init__()


@dataclass
class Locacion(Entidad):
    def __str__(self) -> str:
        return f"Locacion(id={self.id})"