from dataclasses import dataclass

from modulos.producto.dominio.repositorios import RepositorioProducto, RepositorioTipoProducto
from seedwork.dominio.fabricas import Fabrica
from seedwork.dominio.repositorios import Repositorio
from .excepciones import ExcepcionFabrica
from .repositorios import RepositorioProductoSQLite, RepositorioTipoProductoSQLite


@dataclass
class FabricaRepositorio(Fabrica):
    def crear_objeto(self, obj: type, mapeador: any = None) -> Repositorio:
        print(f"Creando objeto: {obj}")
        if obj == RepositorioProducto:
            return RepositorioProductoSQLite()
        elif obj == RepositorioTipoProducto:
            return RepositorioTipoProductoSQLite()
        else:
            raise ExcepcionFabrica()
