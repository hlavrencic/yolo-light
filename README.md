# YOLO Light API 🚀

**Tiny YOLO11n object detection API** optimizada para **Raspberry Pi 4** con compilación automática via GitHub Actions.

Detecta objetos en imágenes usando el modelo YOLO ultraligero (12MB Float16) con FastAPI en un contenedor Docker.

## 📸 Resultado Visual

**Input → Output con Detecciones**

![Input](docs/examples/input_example.jpg) → ![Output](docs/examples/output_example.jpg)

El endpoint `/detect-visual` retorna imágenes con bounding boxes dibujados automáticamente ✨

## ✨ Características

- ✅ **Ultraligero**: Modelo YOLO parametrizable (default: YOLOv5n)
- ✅ **Multiperfil**: Detecta 80 clases COCO (personas, objetos, animales, etc.)
- ✅ **Multi-arquitectura**: amd64, arm64 con GitHub Actions
- ✅ **API REST**: 4 endpoints + health check dinámico
- ✅ **Docker-native**: Compilación automática y distribución en Docker Hub
- ✅ **Flexible**: Selecciona modelo mediante variable de entorno MODEL_NAME
- ✅ **Eficiente**: ~800MB-1.2GB en runtime en RPi4
- ✅ **Visual Output**: Endpoint para retornar imágenes con bounding boxes

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

| Sección | Contenido |
|---------|-----------|
| **[📖 Docs Principal](docs/)** | Índice de toda la documentación |
| **[🚀 Guía de Instalación](docs/guides/INSTALLATION.md)** | Instalación en RPi4, PC, Docker Compose |
| **[📸 Ejemplos de Uso](docs/EXAMPLES.md)** | Casos prácticos con imágenes de resultado |
| **[📚 API Reference](docs/guides/API_REFERENCE.md)** | Documentación técnica completa de endpoints |
| **[🏠 CasaOS Import](docs/guides/CASAOS.md)** | Instalación con interfaz gráfica |
| **[🐧 RPi4 Deployment](docs/guides/DEPLOYMENT_RPI4.md)** | Deploy en Raspberry Pi 4 |
| **[⚙️ GitHub Actions](docs/guides/GITHUB_ACTIONS.md)** | Setup CI/CD para compilar imágenes |

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

## 🔍 API Endpoints

### 1. Detectar Objetos (JSON)
```bash
curl -X POST -F "file=@imagen.jpg" http://localhost:8000/detect
```

### 2. Detectar Objetos (Imagen Visual) ✨
```bash
curl -X POST -F "file=@imagen.jpg" http://localhost:8000/detect-visual -o detectada.png
```

### 3. Health Check
```bash
curl http://localhost:8000/health
```

📚 **Ver documentación completa:** [docs/guides/API_REFERENCE.md](docs/guides/API_REFERENCE.md)

---

## ⚙️ Configuración Rápida

| Variable | Default | Descripción |
|----------|---------|-------------|
| `MODEL_NAME` | `yolov5n.pt` | Modelo YOLO (yolov5n, yolov5s, yolov5m, yolov11n, etc.) |
| `PORT` | 8000 | Puerto de la API |

**Cambiar modelo:**
```bash
docker run -e MODEL_NAME=yolov5m.pt -d -p 8000:8000 hn8888/yolo-light:arm64
```

---

## 📊 Rendimiento

| Métrica | Valor |
|---------|-------|
| Inference time (RPi4) | 100-300ms |
| Memory footprint | ~800MB-1.2GB |
| Throughput | ~2-3 req/seg |
| Modelos soportados | 80 clases COCO |
| Tamaño imagen Docker | 1.5-2GB |

---

## 🧪 Testing

```bash
pip install -r requirements.txt
python test_api_complete.py
```

---

## 📁 Estructura

```
yolo-light/
├── README.md                           ← Estás aquí
├── Dockerfile                          ← Multi-arquitectura
├── docker-compose.yml                  ← Docker Compose
├── src/
│   └── main.py                         ← API FastAPI
├── docs/                               ← DOCUMENTACIÓN COMPLETA
│   ├── README.md
│   ├── EXAMPLES.md
│   └── guides/
│       ├── INSTALLATION.md
│       ├── API_REFERENCE.md
│       ├── CASAOS.md
│       ├── DEPLOYMENT_RPI4.md
│       └── GITHUB_ACTIONS.md
└── testing/                            ← Imágenes de prueba
```

---

## 📖 Documentación Completa

👉 **[Ver documentación en /docs](docs/)**

- 🚀 [Guía de Instalación](docs/guides/INSTALLATION.md)
- 📸 [Ejemplos de Uso](docs/EXAMPLES.md)
- 📚 [API Reference](docs/guides/API_REFERENCE.md)
- 🏠 [CasaOS](docs/guides/CASAOS.md)
- 🐧 [RPi4 Deployment](docs/guides/DEPLOYMENT_RPI4.md)
- ⚙️ [GitHub Actions](docs/guides/GITHUB_ACTIONS.md)

---

## 🌐 Links Útiles

| Recurso | Link |
|---------|------|
| **Docker Hub** | [hn8888/yolo-light](https://hub.docker.com/r/hn8888/yolo-light) |
| **GitHub Repo** | [hlavrencic/yolo-light](https://github.com/hlavrencic/yolo-light) |
| **Ultralytics YOLO** | [github.com/ultralytics/yolov5](https://github.com/ultralytics/yolov5) |

---

## 📜 Licencia

**CC BY-NC 4.0** - Uso no comercial únicamente

---

**Optimized for RPi4 • Lightweight YOLO • Real-time Detection**
