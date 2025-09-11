from dataclasses import dataclass
from seedwork.dominio.fabricas import Fabrica
from seedwork.dominio.repositorios import Repositorio
from modulos.ventas.dominio.repositorios import RepositorioPedido
from modulos.ventas.infraestructura.repositorios import RepositorioPedidoSQLite
from modulos.ventas.infraestructura.excepciones import ExcepcionFabrica

@dataclass
class FabricaRepositorio(Fabrica):
    def crear_objeto(self, obj: type, mapeador: any = None) -> Repositorio:
        print(f"Creando objeto: {obj}")
        if obj == RepositorioPedido:
            return RepositorioPedidoSQLite()
        else:
            raise ExcepcionFabrica()
