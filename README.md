# YOLO Light API 🚀

**Tiny YOLO11n object detection API** optimizada para **Raspberry Pi 4** con compilación automática via GitHub Actions.

Detecta objetos en imágenes usando el modelo YOLO ultraligero (12MB Float16) con FastAPI en un contenedor Docker.

## ✨ Características

- ✅ **Ultraligero**: Modelo YOLO parametrizable (default: YOLOv5n)
- ✅ **Multiperfil**: Detecta 80 clases COCO (personas, objetos, animales, etc.)
- ✅ **Multi-arquitectura**: amd64, arm64 con GitHub Actions
- ✅ **API REST**: 3 endpoints + health check dinámico
- ✅ **Docker-native**: Compilación automática y distribución en Docker Hub
- ✅ **Flexible**: Selecciona modelo mediante variable de entorno MODEL_NAME
- ✅ **Eficiente**: ~800MB-1.2GB en runtime en RPi4

## 📋 Requisitos

| Componente | Mínimo | Recomendado |
|-----------|--------|-------------|
| Hardware | RPi4 2GB | RPi4 4GB+ |
| Docker | Sí | Sí |
| Imagen | 1.5-2GB | 2GB+ |
| RAM Runtime | 800MB | 1.2GB+ |
| Arquitectura | arm64 | amd64, arm64, arm/v7 |

## 🚀 Inicio Rápido

### Opción 1: CasaOS (Interfaz Gráfica)

```bash
# En tu RPi4 con CasaOS:
# 1. Abre http://casaos.local:81
# 2. App Management → Compose
# 3. Importa el archivo docker-compose.yml
# 4. Click Deploy

# Espera 1-2 minutos

# Verificar:
curl http://casaos.local:8000/health
```

📖 Ver guía completa: [CASAOS_IMPORT.md](CASAOS_IMPORT.md)

### Opción 2: Desde Docker Hub (Terminal)

```bash
# RPi4 - Descargar imagen compilada
docker pull hn8888/yolo-light:arm64

# Ejecutar con modelo por defecto (YOLOv5n)
docker run -d \
  -p 8000:8000 \
  --name yolo-api \
  --memory=1.5G \
  hn8888/yolo-light:arm64

# Ejecutar con modelo personalizado
docker run -d \
  -e MODEL_NAME=yolov5m.pt \
  -p 8000:8000 \
  --memory=1.5G \
  hn8888/yolo-light:arm64

# Verificar
curl http://localhost:8000/health
```

### Opción 3: Compilar Localmente

```bash
# Clonar repo
git clone https://github.com/tuusuario/yolo-light.git
cd yolo-light

# Compilar para tu arquitectura
docker build -t yolo-light:latest .

# Ejecutar
docker run -d -p 8000:8000 --memory=1.5G yolo-light:latest
```

### Opción 4: GitHub Actions (Multi-arquitectura)

El proyecto compila automáticamente para **amd64, arm64, arm/v7** en cada push.

📖 Ver: [GITHUB_ACTIONS_QUICK_SETUP.md](GITHUB_ACTIONS_QUICK_SETUP.md)

## 📚 Documentación

| Archivo | Contenido |
|---------|-----------|
| [CASAOS_IMPORT.md](CASAOS_IMPORT.md) | 🏠 Importar en CasaOS (paso a paso) |
| [DOCKER_HUB_INSTRUCTIONS.md](DOCKER_HUB_INSTRUCTIONS.md) | Cómo usar la imagen desde Docker Hub |
| [GITHUB_ACTIONS_QUICK_SETUP.md](GITHUB_ACTIONS_QUICK_SETUP.md) | Setup GitHub Actions en 5 min |
| [GITHUB_ACTIONS_SETUP.md](GITHUB_ACTIONS_SETUP.md) | Documentación completa de workflows |
| [QUICK_START_GITHUB_ACTIONS.md](QUICK_START_GITHUB_ACTIONS.md) | Ejemplos prácticos y casos de uso |
| [DEPLOYMENT_RPI4.md](DEPLOYMENT_RPI4.md) | Deploy en Raspberry Pi 4 |
| [DEVELOPMENT_STATUS.md](DEVELOPMENT_STATUS.md) | Estado del desarrollo |

## 🔍 API Endpoints

### 1. Health Check
```bash
curl http://localhost:8000/health
```

**Response:**
```json
{
  "status": "healthy",
  "model": "yolov5n.pt",
  "model_status": "loaded",
  "model_ready": true,
  "version": "1.0.0",
  "classes": 80
}
```

### 2. Detectar Objetos (JSON)
```bash
curl -X POST -F "file=@imagen.jpg" http://localhost:8000/detect
```

**Response:**
```json
{
  "success": true,
  "count": 2,
  "inference_time_ms": 1677.5,
  "total_time_ms": 1723.6,
  "model": "yolov5n.pt",
  "image_size": [1920, 1255],
  "objects": [
    {
      "class": "chair",
      "confidence": 0.907,
      "bbox": {"x1": 606, "y1": 691, "x2": 896, "y2": 1115}
    }
  ]
}
```

### 3. Detectar Objetos (Imagen Visual) ✨ **NUEVO**
```bash
curl -X POST -F "file=@imagen.jpg" http://localhost:8000/detect-visual -o imagen_detectada.png
```

**Response:** Descarga de imagen PNG con bounding boxes dibujados

**Características:**
- 🟩 Rectángulos alrededor de cada objeto detectado
- 📝 Etiquetas con clase + confianza
- 🎨 Colores diferentes para cada objeto
- ⚡ Mismos resultados que `/detect` pero en formato visual

**Ejemplo de uso en RPi4:**
```bash
# Descargar imagen con detecciones
curl -X POST -F "file=@habitacion.jpg" \
  http://192.168.0.251:8003/detect-visual \
  -o habitacion_con_detecciones.png
```

### 4. Información de la API
```bash
curl http://localhost:8000/
```

**Response:**
```json
{
  "name": "YOLO Light API",
  "version": "1.0.0",
  "description": "Lightweight YOLO object detection API for RPi4",
  "model": "yolov5n.pt",
  "model_classes": 80,
  "endpoints": {
    "POST /detect": "Detectar objetos en imagen → JSON",
    "POST /detect-visual": "Detectar objetos en imagen → Imagen con bounding boxes",
    "GET /health": "Verificar estado de API",
    "GET /": "Información de API"
  }
}
```

## ⚙️ Configuración

| Variable | Default | Descripción |
|----------|---------|-------------|
| `MODEL_NAME` | `yolov5n.pt` | Modelo YOLO a cargar (cualquier modelo de Ultralytics) |
| `PORT` | 8000 | Puerto de la API |

### Modelos Soportados

Puedes usar cualquier modelo de la librería Ultralytics:

**YOLOv5** (Recomendado para RPi4):
```bash
# Ultraligero (7.5MB)
MODEL_NAME=yolov5n.pt

# Pequeño (21MB)
MODEL_NAME=yolov5s.pt

# Mediano (47MB)
MODEL_NAME=yolov5m.pt
```

**YOLOv8**:
```bash
MODEL_NAME=yolov8n.pt      # Nano
MODEL_NAME=yolov8s.pt      # Small
MODEL_NAME=yolov8m.pt      # Medium
```

**YOLOv11**:
```bash
MODEL_NAME=yolov11n.pt     # Nano
MODEL_NAME=yolov11s.pt     # Small
MODEL_NAME=yolov11m.pt     # Medium
```

### Ejemplos de Uso

```bash
# Ejecutar con YOLOv5m (mayor precisión, más lento)
docker run -e MODEL_NAME=yolov5m.pt -d -p 8000:8000 hn8888/yolo-light:arm64

# Ejecutar con YOLOv8n (versión más nueva)
docker run -e MODEL_NAME=yolov8n.pt -d -p 8000:8000 hn8888/yolo-light:arm64

# Verificar modelo cargado
curl http://localhost:8000/health
```
## ⚙️ Configuración

| Variable | Default | Descripción |
|----------|---------|-------------|
| `CONFIDENCE` | 0.4 | Umbral de confianza (0-1) |
| `MODEL_PATH` | `/app/models/yolo11n_float16.tflite` | Ruta del modelo |
| `PORT` | 8000 | Puerto de la API |

```bash
# Compilación nativa más lenta pero compatible
docker build -t yolo-light:latest .
# El build tYOLOv5n | YOLOv5m |
|---------|---------|---------|
| Inference time (RPi4) | 200-300ms | 400-600ms |
| Tamaño modelo | 7.5MB | 47MB |
| Memory footprint | ~800MB | ~1.2GB |
| Throughput | ~3-4 req/seg | ~1-2 req/seg |
| Clases COCO | 80 | 80 |
| Tamaño imagen Docker | 1.5-2GB | 1.5-2GB |

**Recomendación para RPi4**: YOLOv5n (balance velocidad/precisión)ux/arm64 \
  -t yolo-light:arm64 \
  --push \
  .
```

### Verificar inferencia real en RPi4

```bash
# Acceder al contenedor
docker exec -it yolo-api bash

# Verificar que tflite-runtime está disponible
python3 -c "import tflite_runtime.interpreter; print('✓ TFLite listo')"

# Ver tamaño de memoria
free -h
ps aux | grep uvicorn
```  

## 🧪 Testing

```bash
# Instalar dependencias
pip install -r requirements.txt

# Ejecutar API (desarrollo)
uvicorn src.main:app --reload --host 0.0.0.0 --port 8000

# En otra terminal, ejecutar tests
python test_api_complete.py
```

**Output esperado:** All 6 tests passed ✅

## 📊 Rendimiento

| Métrica | Valor |
|---------|-------|
| Inference time | 200-400ms (RPi4) |
| Memory footprint | ~800MB-1.2GB |
| Throughput | ~2-3 req/seg |
| Modelos soportados | COCO (80 clases) |
| Tamaño modelo | 12MB Float16 |
| Tamaño imagen Docker | 1.5-2GB |

## 🐳 Docker Hub

Imagen precompilada disponible:
```bash
docker pull hn8888/yolo-light:arm64        # Para RPi4
docker pull hn8888/yolo-light:amd64        # Para PC/Mac
docker pull hn8888/yolo-light:latest       # Multi-arch
```**.

## 📝 Ejemplos de Deployment

### Cambiar modelo sin recompilar

```bash
# Cambiar a YOLOv5m (más preciso, más lento)
docker stop yolo-api
docker rm yolo-api

docker run -d \
  -e MODEL_NAME=yolov5m.pt \
  -p 8000:8000 \
  --memory=2G \
  --name yolo-api \
  hn8888/yolo-light:arm64

# El modelo se descargará automáticamente en el primer inicio
```

### Verificar el modelo actual
multi-arquitectura
├── requirements.txt                    # Dependencias Python (referencia)
├── src/
│   ├── main.py                        # API FastAPI + parametrización
│   └── yolo11n_float16.tflite         # Archivo de referencia
├── testing/                            # Imágenes de prueba
├── .github/workflows/                  # GitHub Actions CI/CD
│   └── docker-build-multiarch.yml     # Build amd64, arm64 (arm/v7 removido)
  yolo-api:
    image: hn8888/yolo-light:arm64
    ports:
      - "8000:8000"
    environms YOLO parametrizables** (YOLOv5, YOLOv8, YOLOv11)
- ✅ **Detecta 80 clases COCO**
- ✅ **Multi-arquitectura**: amd64, arm64
- ✅ **GitHub Actions CI/CD** automático
- ✅ **Docker Hub** precompilado
- ✅ **Testing completo** (6 tests pasando)
- ✅ **Documentación completa**
- ✅ **Selección de modelo sin recompilación
## 🔧 Troubleshooting

### "Out of memory" en RPi4
```bash
# Aumentar límite de Docker
docker run -m 2G yolo-light:latest
```

### Errores de compilación ARM
Usar GitHub Actions en lugar de compilar localmente. Ver [GITHUB_ACTIONS_QUICK_SETUP.md](GITHUB_ACTIONS_QUICK_SETUP.md)

### Modelo no encontrado
Se descarga automáticamente en la primera ejecución.

## 📁 Estructura

```
yolo-light/
├── Dockerfile                          # Build para x86_64
├── Dockerfile.rpi4                     # Build específico RPi4
├── requirements.txt                    # Dependencias Python
├── src/
│   ├── main.py                        # API FastAPI
│   └── yolo11n_float16.tflite         # Modelo YOLO
├── testing/                            # Imágenes de prueba
├── .github/workflows/                  # GitHub Actions CI/CD
│   ├── docker-build-multiarch.yml     # Build multi-arch
│   └── docker-build-arm64.yml         # Build ARM64 rápido
└── test_api_complete.py               # Tests completos
```

## 🌟 Características

- ✅ **API REST** con FastAPI
- ✅ **Modelo YOLO11n** (ultraligero, 12MB)
- ✅ **Detecta 80 clases COCO**
- ✅ **Multi-arquitectura**: amd64, arm64, arm/v7
- ✅ **GitHub Actions CI/CD** automático
- ✅ **Docker Hub** precompilado
- ✅ **Testing completo** (6 tests pasando)
- ✅ **Documentación completa**

## 📖 Próximos Pasos

1. **Inicio rápido**: Ver [GITHUB_ACTIONS_QUICK_SETUP.md](GITHUB_ACTIONS_QUICK_SETUP.md)
2. **Deploy en RPi4**: Ver [DEPLOYMENT_RPI4.md](DEPLOYMENT_RPI4.md)
3. **Usar desde Docker Hub**: Ver [DOCKER_HUB_INSTRUCTIONS.md](DOCKER_HUB_INSTRUCTIONS.md)

## 📝 Licencia

**Creative Commons Attribution-NonCommercial 4.0 International (CC BY-NC 4.0)**

Este proyecto es de **uso no comercial**. Puedes:
- ✅ Usar con fines educativos y de investigación
- ✅ Usar en organizaciones sin fines de lucro
- ✅ Crear derivados (forks, modificaciones)
- ❌ Usar con fines comerciales
- ❌ Vender o monetizar

Ver [LICENSE](LICENSE) para detalles completos.

---

**Optimized for IoT • Lightweight YOLO11n • RPi4 Ready**
