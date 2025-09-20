import seedwork.presentacion.api as api
import json
import time
from datetime import datetime
from modulos.ventas.aplicacion.mapeadores import MapeadorPedidoDTOJson, MapeadorPedido
from flask import request, Response, Blueprint
from modulos.ventas.aplicacion.comandos.crear_pedido import CrearPedido
from seedwork.aplicacion.comandos import ejecutar_comando
from modulos.ventas.aplicacion.consultas.obtener_todos_los_pedidos import ObtenerTodosLosPedidosConsulta
from seedwork.aplicacion.consultas import ejecutar_consulta


import logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


request_count = 0
start_time = time.time()

bp = api.crear_blueprint('ventas', '/api/ventas')


@bp.route('/', methods=['POST'])
def crear_pedido():
    global request_count
    request_count += 1
    
    start_time_pedido = time.time()
    timestamp = datetime.now().isoformat()
    
    logger.info(f"[METRICS-START] Crear pedido - Timestamp: {timestamp} - Request #{request_count}")
    
    try:
        # Validación y mapeo de datos
        start_validation = time.time()
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
        
        validation_time = (time.time() - start_validation) * 1000
        logger.info(f"[METRICS-VALIDATION] Validación y mapeo pedido - Latencia: {validation_time:.2f}ms - Cliente: {pedido_dto.cliente_id}")

        # Creación del comando
        start_command = time.time()
        comando = CrearPedido(
            cliente_id=pedido_dto.cliente_id,
            fecha_pedido=pedido_dto.fecha_pedido,
            estado=pedido_dto.estado,
            items=items_simplificados
        )

        resultado = ejecutar_comando(comando)
        command_time = (time.time() - start_command) * 1000
        
        total_time = (time.time() - start_time_pedido) * 1000
        logger.info(f"[METRICS-END] Crear pedido - Latencia total: {total_time:.2f}ms - Cliente: {pedido_dto.cliente_id} - Items: {len(items_simplificados)}")
        
        return Response('{}', status=202, mimetype='application/json')
        
        
    except ValueError as e:
        # Errores de validación (productos no encontrados, stock insuficiente, etc.)
        total_time = (time.time() - start_time_pedido) * 1000
        logger.warning(f"[METRICS-ERROR-VALIDATION] Error validación crear pedido - Latencia: {total_time:.2f}ms - Error: {e}")
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
        total_time = (time.time() - start_time_pedido) * 1000
        logger.error(f"[METRICS-ERROR-INTERNAL] Error interno crear pedido - Latencia: {total_time:.2f}ms - Error: {e}")
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
    global request_count
    request_count += 1
    
    start_time_query = time.time()
    timestamp = datetime.now().isoformat()
    
    logger.info(f"[METRICS-START] Consulta pedidos - Timestamp: {timestamp} - Request #{request_count}")
    
    try:
        consulta = ObtenerTodosLosPedidosConsulta()
        resultado = ejecutar_consulta(consulta)
            
        # Convertir las entidades de dominio a DTOs
        mapeador = MapeadorPedido()
        pedidos_dto = [mapeador.entidad_a_dto(pedido) for pedido in resultado.resultado]
        
        # Convertir DTOs a formato JSON externo
        mapeador_json = MapeadorPedidoDTOJson()
        pedidos_json = [mapeador_json.dto_a_externo(pedido_dto) for pedido_dto in pedidos_dto]
        
        end_time_query = time.time()
        latency_ms = (end_time_query - start_time_query) * 1000
        
        logger.info(f"[METRICS-END] Consulta pedidos - Latencia: {latency_ms:.2f}ms - Pedidos: {len(pedidos_json)} - Timestamp: {timestamp}")
        
        return Response(json.dumps(pedidos_json), status=200, mimetype='application/json')
    except Exception as e:
        end_time_query = time.time()
        latency_ms = (end_time_query - start_time_query) * 1000
        
        logger.error(f"[METRICS-ERROR] Consulta pedidos - Latencia: {latency_ms:.2f}ms - Error: {e} - Timestamp: {timestamp}")
        return Response(json.dumps(dict(error=str(e))), status=400, mimetype='application/json')
