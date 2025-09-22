# src/modulos/ventas/infraestructura/cliente_productos.py
import requests
import os
import logging
from typing import Dict, List, Optional
from uuid import UUID

logger = logging.getLogger(__name__)

class ProductoInfo:
    """DTO para información de producto desde el servicio de productos"""
    def __init__(self, id: str, nombre: str, precio: float, stock: int, tipo_producto: str):
        self.id = UUID(id) if isinstance(id, str) else id
        self.nombre = nombre
        self.precio = precio
        self.stock = stock
        self.tipo_producto = tipo_producto

class ClienteProductos:
    """Cliente HTTP para comunicarse con el servicio de productos"""
    
    def __init__(self):
        self.base_url = os.getenv('PRODUCTOS_SERVICE_URL', 'http://productos:5000')
        self.timeout = int(os.getenv('PRODUCTOS_SERVICE_TIMEOUT', '10'))
        
    def validar_producto_existe(self, producto_id: UUID) -> bool:
        """Valida si un producto existe en el servicio de productos"""
        try:
            url = f"{self.base_url}/api/producto/{producto_id}"
            response = requests.get(url, timeout=self.timeout)
            
            if response.status_code == 200:
                logger.info(f"Producto {producto_id} validado exitosamente")
                return True
            elif response.status_code == 404:
                logger.warning(f"Producto {producto_id} no encontrado")
                return False
            else:
                logger.error(f"Error validando producto {producto_id}: {response.status_code}")
                return False
                
        except requests.exceptions.RequestException as e:
            logger.error(f"Error de conexión validando producto {producto_id}: {e}")
            # En caso de error de conexión, asumimos que el producto existe para no bloquear ventas
            # En un entorno de producción, podrías querer un comportamiento diferente
            return True
    
    def obtener_producto(self, producto_id: UUID) -> Optional[ProductoInfo]:
        """Obtiene información completa de un producto"""
        try:
            url = f"{self.base_url}/api/producto/{producto_id}"
            response = requests.get(url, timeout=self.timeout)
            
            if response.status_code == 200:
                data = response.json()
                producto = ProductoInfo(
                    id=data['id'],
                    nombre=data['nombre'],
                    precio=data['precio'],
                    stock=data['stock'],
                    tipo_producto=data.get('tipo_producto', 'GENERICO')
                )
                logger.info(f"✅ Producto {producto_id} obtenido: {producto.nombre}")
                return producto
            elif response.status_code == 404:
                logger.warning(f"Producto {producto_id} no encontrado")
                return None
            else:
                logger.error(f"Error obteniendo producto {producto_id}: {response.status_code}")
                return None
                
        except requests.exceptions.RequestException as e:
            logger.error(f"Error de conexión obteniendo producto {producto_id}: {e}")
            return None
    
    def validar_productos_existen(self, producto_ids: List[UUID]) -> Dict[UUID, bool]:
        """Valida múltiples productos de una vez"""
        resultados = {}
        
        for producto_id in producto_ids:
            resultados[producto_id] = self.validar_producto_existe(producto_id)
        
        productos_no_encontrados = [pid for pid, existe in resultados.items() if not existe]
        if productos_no_encontrados:
            logger.warning(f"Productos no encontrados: {productos_no_encontrados}")
        
        return resultados
    
    def obtener_productos(self, producto_ids: List[UUID]) -> Dict[UUID, Optional[ProductoInfo]]:
        """Obtiene información de múltiples productos"""
        resultados = {}
        
        for producto_id in producto_ids:
            resultados[producto_id] = self.obtener_producto(producto_id)
        
        return resultados
    
    def validar_stock_disponible(self, producto_id: UUID, cantidad_solicitada: int) -> bool:
        """Valida si hay stock suficiente para un producto"""
        producto = self.obtener_producto(producto_id)
        
        if not producto:
            logger.warning(f"No se pudo validar stock para producto {producto_id}: producto no encontrado")
            return False
        
        stock_disponible = producto.stock >= cantidad_solicitada
        
        if not stock_disponible:
            logger.warning(f"Stock insuficiente para producto {producto_id}: solicitado {cantidad_solicitada}, disponible {producto.stock}")
        
        return stock_disponible
    
    def validar_productos_y_stock(self, items: List[dict]) -> Dict[UUID, dict]:
        """
        Valida existencia y stock de productos de manera eficiente.
        Retorna un diccionario con información de validación para cada producto.
        
        Args:
            items: Lista de diccionarios con 'producto_id' y 'cantidad'
            
        Returns:
            Dict con estructura: {producto_id: {'existe': bool, 'stock_ok': bool, 'producto': ProductoInfo}}
        """
        logger.info(f"Validando productos y stock: {items}")
        resultados = {}
        
        # Extraer IDs únicos de productos
        producto_ids = list(set(item['producto_id'] for item in items))
        
        # Obtener información de todos los productos en una sola pasada
        productos_info = self.obtener_productos(producto_ids)
        
        # Crear diccionario de cantidades por producto
        cantidades = {item['producto_id']: item['cantidad'] for item in items}
        
        # Validar cada producto
        for producto_id in producto_ids:
            producto = productos_info.get(producto_id)
            
            if producto:
                stock_ok = producto.stock >= cantidades[producto_id]
                resultados[producto_id] = {
                    'existe': True,
                    'stock_ok': stock_ok,
                    'producto': producto,
                    'stock_disponible': producto.stock,
                    'cantidad_solicitada': cantidades[producto_id]
                }
                
                if not stock_ok:
                    logger.warning(f"Stock insuficiente para producto {producto_id}: solicitado {cantidades[producto_id]}, disponible {producto.stock}")
            else:
                resultados[producto_id] = {
                    'existe': False,
                    'stock_ok': False,
                    'producto': None,
                    'stock_disponible': 0,
                    'cantidad_solicitada': cantidades[producto_id]
                }
                logger.warning(f"Producto {producto_id} no encontrado")
        
        return resultados
