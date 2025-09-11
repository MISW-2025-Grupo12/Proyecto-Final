"""Reglas de negocio reusables parte del seedwork del proyecto

En este archivo usted encontrará reglas de negocio reusables parte del seedwork del proyecto

"""

from abc import ABC, abstractmethod

class ReglaNegocio(ABC):

    __mensaje: str ='La regla de negocio es invalida'

    def __init__(self, mensaje):
        self.__mensaje = mensaje

    def mensaje_error(self) -> str:
        return self.__mensaje

    @abstractmethod
    def es_valido(self) -> bool:
        ...

    def __str__(self):
        return f"{self.__class__.__name__} - {self.__mensaje}"


class IdEntidadEsInmutable(ReglaNegocio):

    def __init__(self, entidad, mensaje='El identificador de la entidad debe ser Inmutable'):
        super().__init__(mensaje)
        self.entidad = entidad

    def es_valido(self) -> bool:
        try:
            # Si _id ya existe, significa que el id ya fue asignado y no debe cambiarse
            if hasattr(self.entidad, '_id') and self.entidad._id is not None:
                return False
            return True
        except AttributeError:
            return True
