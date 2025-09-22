# Medisupply - Sistema de Gestión de Productos Médicos

## 📋 Requisitos

- Python 3.9+
- Flask 3.0.3
- SQLAlchemy 2.0.38
- PostgreSQL (opcional, por defecto usa SQLite)

## 🛠️ Instalación

### Opción 1: Entorno Virtual (Recomendado)

1. **Clonar el repositorio**
```bash
git clone <repository-url>
cd Experimento
```

2. **Crear entorno virtual**
```bash
python -m venv venv
```

3. **Activar entorno virtual**
```bash
# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate
```

4. **Instalar dependencias**
```bash
pip install -r requirements.txt
```

5. **Ejecutar la aplicación**
```bash
flask --app src/medisupply/api run
```

### Opción 2: Docker

1. **Construir la imagen**
```bash
docker build -t medisupply .
```

2. **Ejecutar el contenedor**
```bash
docker run -p 5000:5000 medisupply
```

## 📚 API Endpoints

### Productos

| Método | Endpoint | Descripción |
|--------|----------|-------------|
| POST | `/api/producto/servicio-producto` | Crear producto (servicio) |
| POST | `/api/producto/comando-producto` | Crear producto (comando CQRS) |
| GET | `/api/producto/` | Obtener todos los productos |
| GET | `/api/producto/{id}` | Obtener producto por ID |

### Tipos de Producto

| Método | Endpoint | Descripción |
|--------|----------|-------------|
| POST | `/api/producto/tipo-producto` | Crear tipo de producto (servicio) |
| POST | `/api/producto/comando-tipo-producto` | Crear tipo de producto (comando CQRS) |
| GET | `/api/producto/tipo-producto` | Obtener todos los tipos de producto |

## 📝 Ejemplos de Uso

### Crear un Tipo de Producto

```bash
curl -X POST http://localhost:5000/api/producto/tipo-producto \
  -H "Content-Type: application/json" \
  -d '{
    "nombre": "Medicamentos",
    "descripcion": "Productos farmacéuticos y medicamentos"
  }'
```

### Crear un Producto

```bash
curl -X POST http://localhost:5000/api/producto/comando-producto \
  -H "Content-Type: application/json" \
  -d '{
    "nombre": "Paracetamol 500mg",
    "descripcion": "Analgésico y antipirético",
    "precio": 5000,
    "stock": 100,
    "marca": "Genfar",
    "lote": "LOT001",
    "tipo_producto_id": "uuid-del-tipo-producto"
  }'
```

### Obtener Todos los Productos

```bash
curl -X GET http://localhost:5000/api/producto/
```
