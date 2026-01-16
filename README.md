# YOLO Light API 🚀

API liviana con YOLO11n para detectar objetos en imágenes. Optimizada para ejecutarse en Raspberry Pi 4 con Docker.

## Requisitos

- **Raspberry Pi 4** con 4GB RAM (mínimo)
- **Docker** instalado
- **Imagen**: ~1.5-2GB (después de compilación)
- **Memoria en runtime**: ~800MB-1.2GB

## Construcción

### En Raspberry Pi 4 (ARM64)

```bash
# Construcción nativa (más rápida en RPi)
docker build -t yolo-light:latest .

# O cross-compilation desde otra máquina (más lenta)
docker buildx build --platform linux/arm64 -t yolo-light:latest .
```

### En PC/Mac (para testing)

```bash
# Construcción para arquitectura local
docker build -t yolo-light:latest .
```

## Ejecución

```bash
# Ejecutar con puerto 8000
docker run -d \
  -p 8000:8000 \
  --name yolo-api \
  --memory=1.5G \
  yolo-light:latest

# Ver logs
docker logs -f yolo-api
```

## API Endpoints

### 1. Health Check
```bash
curl http://localhost:8000/health
```

**Respuesta:**
```json
{
  "status": "healthy",
  "model": "YOLO11n"
}
```

### 2. Detectar Objetos
```bash
curl -X POST -F "file=@foto.jpg" http://localhost:8000/detect
```

**Respuesta:**
```json
{
  "success": true,
  "count": 3,
  "inference_time_ms": 245.5,
  "objects": [
    {
      "id": 1,
      "class": "person",
      "confidence": 0.892,
      "bbox": {
        "x1": 100.5,
        "y1": 50.2,
        "x2": 300.1,
        "y2": 450.8
      },
      "width": 199.6,
      "height": 400.6
    }
  ]
}
```

### 3. Información de la API
```bash
curl http://localhost:8000/
```

## Óptimizaciones para RPi4

✓ **Modelo TFLite Float16** (yolo11n_float16.tflite) - solo ~12MB  
✓ **Confianza = 0.4** - reduce falsos positivos  
✓ **Procesamiento CPU** - sin GPU  
✓ **Caché de modelos** - carga una sola vez  
✓ **Health checks** automáticos  
✓ **Límite de memoria** en Docker  
✓ **tflite-runtime** - librería ligera para inferencia

## Despliegue en RPi4 con TFLite Real

### Opción 1: Usar paquete APT (Recomendado)

```bash
# En RPi4 con Raspberry Pi OS
ssh pi@raspberry.local
cd yolo-light

# Instalar tflite-runtime desde APT
sudo apt-get update
sudo apt-get install -y python3-tflite-runtime

# Copiar archivo del modelo (si no está)
cp yolo11n_float16.tflite /app/models/

# Ejecutar con modelo real (reemplazar main.py con main_tflite.py)
# Nota: En producción, usar main_tflite.py que carga tflite-runtime
docker build -t yolo-light:rpi4-tflite .
docker run -d -p 8000:8000 --name yolo-api yolo-light:rpi4-tflite
```

### Opción 2: Compilar en RPi4

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

## Testing Local

```bash
# Instalar dependencias
pip install -r requirements.txt

# Ejecutar API (desarrollo)
uvicorn src.main:app --reload --host 0.0.0.0 --port 8000

# En otra terminal, ejecutar tests
python test_api.py
```

## Performance

| Métrica | Valor |
|---------|-------|
| Inference time | 200-400ms (RPi4) |
| Memory footprint | ~800MB |
| Throughput | ~2-3 req/seg |
| Modelos soportados | COCO (80 clases) |

## Troubleshooting

### "Out of memory" en RPi4

```bash
# Aumentar swap (temporal)
docker run -m 2G yolo-light:latest

# O ajustar permanentemente en docker daemon.json
```

### Errores de compilación ARM

```bash
# Asegurar que tienes buildx instalado
docker buildx create --name mybuilder
docker buildx use mybuilder
docker buildx build --platform linux/arm64 -t yolo-light:latest .
```

### Modelo no encontrado

El modelo se descargará automáticamente en la primera ejecución (~50MB).

```bash
# Pre-descargar modelo
docker run yolo-light:latest python -c "from ultralytics import YOLO; YOLO('yolo11n.pt')"
```

## Estructura

```
yolo-light/
├── Dockerfile           # Build para RPi4
├── requirements.txt     # Dependencias Python
├── src/
│   └── main.py         # API FastAPI
├── testing/
│   ├── foto.jpg        # Imagen de prueba
│   └── habitacion.jpg  # Imagen de prueba
└── test_api.py         # Script de testing
```

## Licencia

MIT

## Author

YOLO Light API - Optimizado para IoT
