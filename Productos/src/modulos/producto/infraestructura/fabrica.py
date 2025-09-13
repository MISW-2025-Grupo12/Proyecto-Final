from seedwork.dominio.fabricas import Fabrica
from modulos.producto.dominio.repositorios_comando import RepositorioProductoComando, RepositorioTipoProductoComando
from modulos.producto.dominio.repositorios_consulta import RepositorioProductoConsulta, RepositorioTipoProductoConsulta
from modulos.producto.infraestructura.repositorios import (
    RepositorioProductoComandoPostgreSQL, 
    RepositorioTipoProductoComandoPostgreSQL,
    RepositorioProductoConsultaPostgreSQL,
    RepositorioTipoProductoConsultaPostgreSQL
)

class FabricaRepositorio(Fabrica):
    """Fábrica unificada para crear todos los repositorios CQRS con PostgreSQL"""
    
    def crear_objeto(self, tipo_repositorio) -> any:
        # Repositorios de comandos (escritura) - Base de datos normalizada
        if tipo_repositorio == RepositorioProductoComando:
            return RepositorioProductoComandoPostgreSQL()
        elif tipo_repositorio == RepositorioTipoProductoComando:
            return RepositorioTipoProductoComandoPostgreSQL()
        
        # Repositorios de consultas (lectura) - Base de datos denormalizada
        elif tipo_repositorio == RepositorioProductoConsulta:
            return RepositorioProductoConsultaPostgreSQL()
        elif tipo_repositorio == RepositorioTipoProductoConsulta:
            return RepositorioTipoProductoConsultaPostgreSQL()
        
        # Si no es ninguno de los anteriores
        else:
            raise ValueError(f"Tipo de repositorio no soportado: {tipo_repositorio}")