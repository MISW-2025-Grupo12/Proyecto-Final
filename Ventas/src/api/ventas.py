import seedwork.presentacion.api as api
import json
from modulos.ventas.aplicacion.mapeadores import MapeadorPedidoDTOJson, MapeadorPedido
from flask import request, Response, Blueprint
from modulos.ventas.aplicacion.comandos.crear_pedido import CrearPedido
from seedwork.aplicacion.comandos import ejecutar_comando
from modulos.ventas.aplicacion.consultas.obtener_todos_los_pedidos import ObtenerTodosLosPedidosConsulta
from seedwork.aplicacion.consultas import ejecutar_consulta

import modulos.ventas.aplicacion.comandos.crear_pedido

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

        comando = CrearPedido(
            cliente_id=pedido_dto.cliente_id,
            fecha_pedido=pedido_dto.fecha_pedido,
            estado=pedido_dto.estado,
            items=pedido_dto.items,
            total=pedido_dto.total
        )

        ejecutar_comando(comando)
        return Response('{}', status=202, mimetype='application/json')
    except Exception as e:
        return Response(json.dumps(dict(error=str(e))), status=400, mimetype='application/json')

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
