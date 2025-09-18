# 🚀 Instrucciones de Despliegue a Google Kubernetes Engine (GKE)

## 📋 Prerrequisitos

- Google Cloud CLI instalado y configurado
- Docker instalado
- kubectl instalado
- Proyecto GCP configurado: `desarrolloswcloud` o el que proyecto que tenga configurado
- Credenciales de service account en `./credentials/service-account-key.json` (crear desde el archivo de ejemplo)

## 🔧 Configuración Inicial

### 1. Autenticación y Configuración del Proyecto

```cmd
# Autenticarse con GCP
gcloud auth login

# Configurar el proyecto
gcloud config set project desarrolloswcloud

# Habilitar APIs necesarias
gcloud services enable container.googleapis.com
gcloud services enable containerregistry.googleapis.com
gcloud services enable pubsub.googleapis.com
gcloud services enable compute.googleapis.com
```

### 2. Configurar Docker para Google Container Registry

```cmd
gcloud auth configure-docker
```

### 3. Crear Temas y Suscripciones de Pub/Sub

```cmd
# Crear tema para eventos de stock de productos
gcloud pubsub topics create productos-stock-actualizado

# Crear tema para eventos de pedidos creados
gcloud pubsub topics create pedidos-creados

# Crear suscripción para el tema de pedidos (usado por el servicio de productos)
gcloud pubsub subscriptions create pedidos-creados-productos-sub --topic=pedidos-creados

# Verificar que se crearon correctamente
gcloud pubsub topics list
gcloud pubsub subscriptions list
```

## 🏗️ Crear Cluster de GKE

### Opción 1: Cluster

```cmd
# Crear cluster con nodos e2-small (2GB RAM) - Comando en una línea
gcloud container clusters create medisupply-cluster --zone=us-central1-a --num-nodes=1 --machine-type=e2-small --disk-size=20GB --disk-type=pd-standard --enable-autoscaling --min-nodes=0 --max-nodes=2 --enable-autorepair --preemptible
```

### 2. Conectar kubectl al Cluster

```cmd
gcloud container clusters get-credentials medisupply-cluster --zone=us-central1-a
```

## 🐳 Construir y Subir Imágenes Docker

### 1. Construir y Subir Imagen de Productos

```cmd
# Navegar al directorio de Productos
cd Productos

# Construir la imagen
docker build -t gcr.io/desarrolloswcloud/productos:latest .

# Subir la imagen
docker push gcr.io/desarrolloswcloud/productos:latest
```

### 2. Construir y Subir Imagen de Ventas

```cmd
# Navegar al directorio de Ventas
cd ..\Ventas

# Construir la imagen
docker build -t gcr.io/desarrolloswcloud/ventas:latest .

# Subir la imagen
docker push gcr.io/desarrolloswcloud/ventas:latest
```

### 3. Verificar Imágenes Subidas

```cmd
# Volver al directorio raíz
cd ..

# Ver las imágenes en el registry
gcloud container images list --repository=gcr.io/desarrolloswcloud
```

## 🚀 Desplegar Aplicaciones en Kubernetes

### 1. Crear Namespace y Configuraciones

```cmd
# Crear el namespace
kubectl apply -f k8s\namespace.yaml

# Aplicar el configmap
kubectl apply -f k8s\configmap.yaml
```

### 2. Configurar Credenciales de Service Account

```cmd
# Copiar el archivo de ejemplo y configurar con tus credenciales reales
copy .\credentials\service-account-key.json.example .\credentials\service-account-key.json

# Editar el archivo con tus credenciales reales de GCP
# Obtener las credenciales desde: https://console.cloud.google.com/iam-admin/serviceaccounts
```

### 3. Crear Secret con Credenciales de GCP

```cmd
kubectl create secret generic gcp-credentials --from-file=service-account-key.json=.\credentials\service-account-key.json --namespace=medisupply
```

### 4. Desplegar Bases de Datos PostgreSQL

```cmd
kubectl apply -f k8s\postgres-deployment.yaml
```

### 5. Desplegar Aplicaciones

```cmd
# Desplegar servicio de productos
kubectl apply -f k8s\productos-deployment.yaml

# Desplegar servicio de ventas
kubectl apply -f k8s\ventas-deployment.yaml
```

### 6. Configurar Acceso Externo (Ingress)

```cmd
# Crear IP estática global para el Ingress
gcloud compute addresses create medisupply-ip --global

# Aplicar el certificado SSL y Ingress unificado
kubectl apply -f k8s\ingress.yaml
```

## ✅ Verificar el Despliegue

### 1. Verificar Estado de los Pods

```cmd
kubectl get pods -n medisupply
```

### 2. Verificar Servicios

```cmd
kubectl get services -n medisupply
```

### 3. Obtener IP Externa del Ingress

```cmd
# Ver la IP externa del Ingress (puede tomar 2-5 minutos)
kubectl get ingress -n medisupply

# También puedes verificar la IP estática creada
gcloud compute addresses describe medisupply-ip --global
```

### 4. Probar las Aplicaciones

```cmd
# Obtener la IP externa del Ingress
kubectl get ingress medisupply-ingress -n medisupply -o jsonpath='{.status.loadBalancer.ingress[0].ip}'

# Probar el servicio de productos
curl http://[IP_EXTERNA]/api/producto/tipo-producto

# Probar el servicio de ventas
curl http://[IP_EXTERNA]/api/ventas/

# Ejemplo con IP real (reemplaza con tu IP):
# curl http://35.201.122.13/api/producto/tipo-producto
# curl http://35.201.122.13/api/ventas/

# Rutas disponibles:
# - Productos: /api/producto/ (GET, POST), /api/producto/<id> (GET), /api/producto/tipo-producto (GET)
# - Ventas: /api/ventas/ (GET, POST)
# - Ruta por defecto: / → redirige a productos
```


## 🔍 Comandos de Monitoreo y Gestión

### Ver Estado General

```cmd
kubectl get all -n medisupply
```

### Ver Logs de Aplicaciones

```cmd
# Ver logs del servicio de productos
kubectl logs -l app=productos -n medisupply

# Ver logs del servicio de ventas
kubectl logs -l app=ventas -n medisupply
```

### Escalar Aplicaciones

```cmd
# Escalar el servicio de productos
kubectl scale deployment productos-deployment --replicas=2 -n medisupply

# Escalar el servicio de ventas
kubectl scale deployment ventas-deployment --replicas=2 -n medisupply
```

### Ver Uso de Recursos

```cmd
kubectl top nodes
kubectl top pods -n medisupply
```



## 🧹 Eliminar Despliegue

### Limpieza Rápida

```cmd
# Eliminar el cluster (esto elimina automáticamente todos los recursos de Kubernetes)
gcloud container clusters delete medisupply-cluster --zone=us-central1-a
```

```cmd
# Ver las imágenes disponibles
gcloud container images list --repository=gcr.io/desarrolloswcloud

# Eliminar imagen de productos
gcloud container images delete gcr.io/desarrolloswcloud/productos:latest --force-delete-tags

# Eliminar imagen de ventas
gcloud container images delete gcr.io/desarrolloswcloud/ventas:latest --force-delete-tags

# Verificar que se eliminaron
gcloud container images list-tags gcr.io/desarrolloswcloud/productos
gcloud container images list-tags gcr.io/desarrolloswcloud/ventas

# Eliminar repositorios vacíos
# gcloud container images delete gcr.io/desarrolloswcloud/productos --force-delete-tags
# gcloud container images delete gcr.io/desarrolloswcloud/ventas --force-delete-tags
```

### Eliminar IP Estática

```cmd
# Eliminar la IP estática
gcloud compute addresses delete medisupply-ip --global

# Verificar que se eliminó
gcloud compute addresses list
```

### Eliminar Temas y Suscripciones de Pub/Sub

```cmd
# Eliminar suscripción
gcloud pubsub subscriptions delete pedidos-creados-productos-sub

# Eliminar temas
gcloud pubsub topics delete productos-stock-actualizado
gcloud pubsub topics delete pedidos-creados

# Verificar que se eliminaron
gcloud pubsub topics list
gcloud pubsub subscriptions list
```

### Verificación Final

```cmd
# Verificar que no hay clusters
gcloud container clusters list

# Verificar que no hay imágenes
gcloud container images list --repository=gcr.io/desarrolloswcloud

# Verificar que no hay IPs estáticas
gcloud compute addresses list

# Verificar que no hay temas de Pub/Sub
gcloud pubsub topics list

# Verificar que no hay suscripciones de Pub/Sub
gcloud pubsub subscriptions list
```
