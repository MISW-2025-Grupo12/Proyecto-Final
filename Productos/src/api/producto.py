import seedwork.presentacion.api as api
import json
from modulos.producto.aplicacion.servicios import ServicioProducto
from modulos.producto.aplicacion.mapeadores import MapeadorProductoDTOJson, MapeadorTipoProductoDTOJson, MapeadorProducto, MapeadorTipoProducto  
from flask import request, Response, Blueprint
from modulos.producto.aplicacion.comandos.crear_producto import CrearProducto
from modulos.producto.aplicacion.comandos.crear_tipo_producto import CrearTipoProducto
from seedwork.aplicacion.comandos import ejecutar_comando
from modulos.producto.aplicacion.consultas.obtener_todos_los_productos import ObtenerTodosLosProductosConsulta
from seedwork.aplicacion.consultas import ejecutar_consulta
from modulos.producto.aplicacion.consultas.obtener_todos_los_tipo_productos import ObtenerTodosLosTiposDeProductoConsulta

import modulos.producto.aplicacion.comandos

import logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

bp = api.crear_blueprint('producto', '/api/producto')

# Servicio crear producto
@bp.route('/servicio-producto', methods=['POST'])
def crear_producto():
    try:
        producto_dict = request.json
        map_producto = MapeadorProductoDTOJson()
        producto_dto = map_producto.externo_a_dto(producto_dict)
        servicio = ServicioProducto()
        resultado_dto = servicio.crear_producto(producto_dto)
        return map_producto.dto_a_externo(resultado_dto)

    except Exception as e:
        return Response(json.dumps(dict(error=str(e))), status=400, mimetype='application/json')

# Comando crear producto
@bp.route('/', methods=['POST'])
def crear_producto_comando():
    try:
        producto_dict = request.json
        map_producto = MapeadorProductoDTOJson()
        producto_dto = map_producto.externo_a_dto(producto_dict)

        comando = CrearProducto(
            nombre=producto_dto.nombre,
            descripcion=producto_dto.descripcion,
            precio=producto_dto.precio,
            stock=producto_dto.stock,
            marca=producto_dto.marca,
            lote=producto_dto.lote,
            tipo_producto_id=producto_dto.tipo_producto_id
        )

        ejecutar_comando(comando)
        return Response('{}', status=202, mimetype='application/json')
    except Exception as e:
        return Response(json.dumps(dict(error=str(e))), status=400, mimetype='application/json')

# Query obtener todos los productos
@bp.route('/', methods=['GET'])
def obtener_todos_los_productos():
    try:
        consulta = ObtenerTodosLosProductosConsulta()
        resultado = ejecutar_consulta(consulta)
        
        # Convertir las entidades de dominio a DTOs
        mapeador = MapeadorProducto()
        productos_dto = [mapeador.entidad_a_dto(producto) for producto in resultado.resultado]
        
        # Convertir DTOs a formato JSON externo
        mapeador_json = MapeadorProductoDTOJson()
        productos_json = [mapeador_json.dto_a_externo(producto_dto) for producto_dto in productos_dto]
        
        return json.dumps(productos_json)
    except Exception as e:
        logger.error(f"Error al obtener todos los productos: {e}")
        return Response(json.dumps(dict(error=str(e))), status=400, mimetype='application/json')

# Servicio crear tipo producto
@bp.route('/tipo-producto', methods=['POST'])
def crear_tipo_producto():
    try:
        tipo_producto_dict = request.json
        map_tipo_producto = MapeadorTipoProductoDTOJson()
        tipo_producto_dto = map_tipo_producto.externo_a_dto(tipo_producto_dict)
        servicio = ServicioProducto()
        resultado_dto = servicio.crear_tipo_producto(tipo_producto_dto)
        return map_tipo_producto.dto_a_externo(resultado_dto)
    except Exception as e:
        return Response(json.dumps(dict(error=str(e))), status=400, mimetype='application/json')

# Command crear tipo producto
@bp.route('/tipo-producto-comando', methods=['POST'])
def crear_tipo_producto_comando():
    try:
        tipo_producto_dict = request.json
        map_tipo_producto = MapeadorTipoProductoDTOJson()
        tipo_producto_dto = map_tipo_producto.externo_a_dto(tipo_producto_dict)

        comando = CrearTipoProducto(
            nombre=tipo_producto_dto.nombre,
            descripcion=tipo_producto_dto.descripcion)

        ejecutar_comando(comando)
        return Response('{}', status=202, mimetype='application/json')
        
    except Exception as e:
        return Response(json.dumps(dict(error=str(e))), status=400, mimetype='application/json')

# Query obtener todos los tipos de producto
@bp.route('/tipo-producto', methods=['GET'])
def obtener_todos_los_tipos_de_producto():
    try:
        consulta = ObtenerTodosLosTiposDeProductoConsulta()
        resultado = ejecutar_consulta(consulta)

        mapeador = MapeadorTipoProducto()
        tipos_productos_dto = [mapeador.entidad_a_dto(tipo_producto) for tipo_producto in resultado.resultado]
        mapeador_json = MapeadorTipoProductoDTOJson()
        tipos_productos_json = [mapeador_json.dto_a_externo(tipo_producto_dto) for tipo_producto_dto in tipos_productos_dto]
        return json.dumps(tipos_productos_json)
    except Exception as e:
        return Response(json.dumps(dict(error=str(e))), status=400, mimetype='application/json')
