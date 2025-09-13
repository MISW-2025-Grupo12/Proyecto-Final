from modulos.ventas.infraestructura.fabrica_unificada_cqrs import FabricaRepositorioUnificada

class PedidoConsultaBaseHandler:
    """Handler base para consultas de pedidos con soporte CQRS"""
    
    def __init__(self):
        self.fabrica_repositorio = FabricaRepositorioUnificada()
    
    @property
    def repositorio_consulta(self):
        """Acceso al repositorio de consultas"""
        return self.fabrica_repositorio.fabrica_repositorio_consulta
