from seedwork.dominio.fabricas import Fabrica
from modulos.ventas.dominio.repositorios_comando import RepositorioPedidoComando
from modulos.ventas.dominio.repositorios_consulta import RepositorioPedidoConsulta
from modulos.ventas.infraestructura.repositorios import (
    RepositorioPedidoComandoPostgreSQL,
    RepositorioPedidoConsultaPostgreSQL
)

class FabricaRepositorioUnificada(Fabrica):
    """Fábrica unificada para crear repositorios de comandos y consultas"""
    
    def crear_objeto(self, obj_type, *args, **kwargs):
        """Crea repositorios basado en el tipo solicitado"""
        
        if obj_type == RepositorioPedidoComando:
            return RepositorioPedidoComandoPostgreSQL()
        elif obj_type == RepositorioPedidoConsulta:
            return RepositorioPedidoConsultaPostgreSQL()
        else:
            raise Exception(f"No existe implementación para el tipo {obj_type}")
    
    @property
    def fabrica_repositorio_comando(self):
        """Propiedad para acceso directo al repositorio de comandos"""
        return self.crear_objeto(RepositorioPedidoComando)
    
    @property
    def fabrica_repositorio_consulta(self):
        """Propiedad para acceso directo al repositorio de consultas"""
        return self.crear_objeto(RepositorioPedidoConsulta)
