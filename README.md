# YOLO Light API 🚀

**Tiny YOLO11n object detection API** optimizada para **Raspberry Pi 4** con compilación automática via GitHub Actions.

Detecta objetos en imágenes usando el modelo YOLO ultraligero (12MB Float16) con FastAPI en un contenedor Docker.

## ✨ Características

- ✅ **Ultraligero**: Modelo YOLO11n Float16 (12MB)
- ✅ **Multiperfil**: Detecta 80 clases COCO (personas, objetos, animales, etc.)
- ✅ **Multi-arquitectura**: amd64, arm64, arm/v7 con GitHub Actions
- ✅ **API REST**: 3 endpoints + health check
- ✅ **Docker-native**: Compilación automática y distribución en Docker Hub
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

### Opción 1: Desde Docker Hub (Recomendado)

```bash
# RPi4 - Descargar imagen compilada
docker pull hn8888/yolo-light:arm64

# Ejecutar
docker run -d \
  -p 8000:8000 \
  --name yolo-api \
  --memory=1.5G \
  hn8888/yolo-light:arm64

# Verificar
curl http://localhost:8000/health
```

### Opción 2: Compilar Localmente

```bash
# Clonar repo
git clone https://github.com/tuusuario/yolo-light.git
cd yolo-light

# Compilar para tu arquitectura
docker build -t yolo-light:latest .

# Ejecutar
docker run -d -p 8000:8000 --memory=1.5G yolo-light:latest
```

### Opción 3: GitHub Actions (Multi-arquitectura)

El proyecto compila automáticamente para **amd64, arm64, arm/v7** en cada push.

📖 Ver: [GITHUB_ACTIONS_QUICK_SETUP.md](GITHUB_ACTIONS_QUICK_SETUP.md)

## 📚 Documentación

| Archivo | Contenido |
|---------|-----------|
| [DOCKER_HUB_INSTRUCTIONS.md](DOCKER_HUB_INSTRUCTIONS.md) | Cómo usar la imagen desde Docker Hub |
| [GITHUB_ACTIONS_QUICK_SETUP.md](GITHUB_ACTIONS_QUICK_SETUP.md) | Setup GitHub Actions en 5 min |
| [GITHUB_ACTIONS_SETUP.md](GITHUB_ACTIONS_SETUP.md) | Documentación completa de workflows |
| [QUICK_START_GITHUB_ACTIONS.md](QUICK_START_GITHUB_ACTIONS.md) | Ejemplos prácticos y casos de uso |
| [DEPLOYMENT_RPI4.md](DEPLOYMENT_RPI4.md) | Deploy en Raspberry Pi 4 |
| [DEVELOPMENT_STATUS.md](DEVELOPMENT_STATUS.md) | Estado del desarrollo |

## 🔍 API Endpoints

### Health Check
```bash
curl http://localhost:8000/health
# Response: { "status": "healthy", "model": "YOLO11n" }
```

### Detectar Objetos
```bash
curl -X POST -F "file=@imagen.jpg" http://localhost:8000/detect
```

**Response:**
```json
{
  "success": true,
  "count": 3,
  "inference_time_ms": 245.5,
  "objects": [
    {
      "class": "person",
      "confidence": 0.892,
      "bbox": { "x1": 100.5, "y1": 50.2, "x2": 300.1, "y2": 450.8 }
    }
  ]
}
```

### Info de la API
```bash
curl http://localhost:8000/
# Response: { "name": "YOLO Light API", "version": "1.0" }
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
# El build toma ~5-10 min pero genera imagen optimizada para ARM64
```

### Opción 3: Cross-compile desde otra máquina

```bash
# Desde PC/Mac con Docker BuildX
docker buildx build --platform linux/arm64 \
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
```

Compilada automáticamente via GitHub Actions para **amd64, arm64, arm/v7**.

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

MIT

---

**Optimized for IoT • Lightweight YOLO11n • RPi4 Ready**
