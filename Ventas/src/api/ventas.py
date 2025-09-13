import seedwork.presentacion.api as api
import json
from modulos.ventas.aplicacion.mapeadores import MapeadorPedidoDTOJson, MapeadorPedido
from flask import request, Response, Blueprint
from modulos.ventas.aplicacion.comandos.crear_pedido import CrearPedido
from seedwork.aplicacion.comandos import ejecutar_comando
from modulos.ventas.aplicacion.consultas.obtener_todos_los_pedidos import ObtenerTodosLosPedidosConsulta
from seedwork.aplicacion.consultas import ejecutar_consulta


import logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

bp = api.crear_blueprint('ventas', '/api/ventas')


@bp.route('/', methods=['POST'])
def crear_pedido():
    try:
        pedido_dict = request.json
        map_pedido = MapeadorPedidoDTOJson()
        pedido_dto = map_pedido.externo_a_dto(pedido_dict)

        # Extraer solo producto_id y cantidad de los items
        items_simplificados = []
        for item in pedido_dto.items:
            items_simplificados.append({
                'producto_id': str(item.producto_id),
                'cantidad': item.cantidad
            })

        comando = CrearPedido(
            cliente_id=pedido_dto.cliente_id,
            fecha_pedido=pedido_dto.fecha_pedido,
            estado=pedido_dto.estado,
            items=items_simplificados
        )

        resultado = ejecutar_comando(comando)
        logger.info(f"Pedido creado: {resultado}")
        return Response('{}', status=202, mimetype='application/json')
        
        
    except ValueError as e:
        # Errores de validación (productos no encontrados, stock insuficiente, etc.)
        logger.warning(f"Error de validación al crear pedido: {e}")
        return Response(
            json.dumps({
                "error": "Error de validación",
                "message": str(e),
                "type": "validation_error"
            }), 
            status=400, 
            mimetype='application/json'
        )
    except Exception as e:
        # Otros errores del sistema
        logger.error(f"Error interno al crear pedido: {e}")
        return Response(
            json.dumps({
                "error": "Error interno del servidor",
                "message": "Ha ocurrido un error inesperado",
                "type": "internal_error"
            }), 
            status=500, 
            mimetype='application/json'
        )

@bp.route('/', methods=['GET'])
def obtener_todos_los_pedidos():
    try:
        consulta = ObtenerTodosLosPedidosConsulta()
        resultado = ejecutar_consulta(consulta)
            
        # Convertir las entidades de dominio a DTOs
        mapeador = MapeadorPedido()
        pedidos_dto = [mapeador.entidad_a_dto(pedido) for pedido in resultado.resultado]
        
        # Convertir DTOs a formato JSON externo
        mapeador_json = MapeadorPedidoDTOJson()
        pedidos_json = [mapeador_json.dto_a_externo(pedido_dto) for pedido_dto in pedidos_dto]
        
        return Response(json.dumps(pedidos_json), status=200, mimetype='application/json')
    except Exception as e:
        return Response(json.dumps(dict(error=str(e))), status=400, mimetype='application/json')
