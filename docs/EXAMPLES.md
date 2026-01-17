# 📸 YOLO Light API - Ejemplos de Uso

Documentación completa con ejemplos prácticos y resultados visuales.

## 🎯 Endpoints en Acción

### 1️⃣ Endpoint `/detect` - JSON Response

Retorna detecciones en formato JSON con coordenadas y confianza.

**Request:**
```bash
curl -X POST -F "file=@input.jpg" http://localhost:8000/detect
```

**Response:**
```json
{
  "success": true,
  "count": 2,
  "inference_time_ms": 145.3,
  "total_time_ms": 205.2,
  "model": "yolov5n.pt",
  "image_size": [1920, 1255],
  "objects": [
    {
      "class": "person",
      "confidence": 0.87,
      "x1": 512,
      "y1": 340,
      "x2": 680,
      "y2": 890
    },
    {
      "class": "person",
      "confidence": 0.82,
      "x1": 1240,
      "y1": 380,
      "x2": 1450,
      "y2": 920
    }
  ]
}
```

---

### 2️⃣ Endpoint `/detect-visual` - Imagen con Bounding Boxes

Retorna PNG con bounding boxes, colores y etiquetas dibujadas.

**Request:**
```bash
curl -X POST -F "file=@input.jpg" http://localhost:8000/detect-visual -o output.png
```

**Imagen de Entrada:**
![Input Example](./examples/input_example.jpg)

**Imagen de Salida (con detecciones):**
![Output Example](./examples/output_example.jpg)

**Características del output:**
- ✅ Rectángulos de colores para cada objeto detectado
- ✅ Etiquetas con clase y confianza
- ✅ Colores variados para mejor visualización
- ✅ Mantiene resolución original de la imagen

---

## 🔧 Configuración de Modelos

### Cambiar Modelo en Runtime

```bash
# YOLOv5 Small (16MB) - Más preciso
docker run -d -e MODEL_NAME=yolov5s.pt -p 8000:8000 hn8888/yolo-light:arm64

# YOLOv5 Medium (40MB) - Balance
docker run -d -e MODEL_NAME=yolov5m.pt -p 8000:8000 hn8888/yolo-light:arm64

# YOLOv11 Nano (8MB) - Más ligero
docker run -d -e MODEL_NAME=yolov11n.pt -p 8000:8000 hn8888/yolo-light:arm64
```

### Comparativa de Modelos

| Modelo | Tamaño | Velocidad | Precisión | RPi4 |
|--------|--------|-----------|-----------|------|
| yolov5n | 7.5MB | ⚡⚡⚡ | ⭐⭐ | ✅ |
| yolov5s | 16MB | ⚡⚡ | ⭐⭐⭐ | ✅ |
| yolov5m | 40MB | ⚡ | ⭐⭐⭐⭐ | ⚠️ |
| yolov11n | 8MB | ⚡⚡⚡ | ⭐⭐⭐ | ✅ |

---

## 📊 Pruebas de Rendimiento

### RPi4 (4GB RAM, arm64)

**Imagen 640x640px:**
- Tiempo de inferencia: ~150-200ms
- Tiempo total: ~200-250ms
- Modelo: yolov5n.pt

**Imagen 1920x1255px:**
- Tiempo de inferencia: ~100-150ms
- Tiempo total: ~150-200ms
- Modelo: yolov5n.pt

### Máquina Local (amd64)

**Imagen 1920x1255px:**
- Tiempo de inferencia: ~50-80ms
- Tiempo total: ~80-120ms
- Modelo: yolov5n.pt

---

## 🚀 Casos de Uso

### 1. Monitoreo de Habitaciones
```bash
# Detectar personas en tiempo real
curl -X POST -F "file=@living_room.jpg" http://localhost:8000/detect-visual -o detected.png
```

### 2. Análisis de Objetos
```bash
# Obtener coordenadas exactas de objetos
curl -X POST -F "file=@warehouse.jpg" http://localhost:8000/detect | python3 -m json.tool
```

### 3. Procesamiento por Lotes
```bash
for img in *.jpg; do
  curl -X POST -F "file=@$img" http://localhost:8000/detect-visual -o "detected_$img"
done
```

---

## ⚙️ Variables de Entorno Avanzadas

```bash
# Ejecutar con múltiples variables
docker run -d \
  -e MODEL_NAME=yolov5m.pt \
  -p 8000:8000 \
  --memory=2G \
  --cpus=1.5 \
  hn8888/yolo-light:arm64
```

---

## 📈 Health Check

```bash
curl http://localhost:8000/health | python3 -m json.tool

# Response:
{
  "status": "healthy",
  "model": "yolov5n.pt",
  "model_status": "loaded",
  "model_ready": true,
  "version": "1.0.0",
  "classes": 80
}
```

---

## 🐛 Troubleshooting

### Error: "Insufficient memory"
→ Aumentar `--memory` en docker run a 2G o 2.5G

### Error: "Model download failed"
→ Verificar conexión a internet, el modelo se descarga automáticamente

### Detecciones lenta
→ Usar modelo más ligero (yolov5n) o reducir resolución de imagen

---

## 📚 Clases Detectadas (COCO Dataset)

El modelo detecta **80 clases COCO** incluyendo:

**Personas y Animales:**
person, dog, cat, horse, cow, bear, zebra, giraffe, bird, dog, ...

**Vehículos:**
car, truck, bus, train, motorcycle, bicycle, airplane, boat, ...

**Objetos del Hogar:**
chair, couch, potted plant, bed, dining table, toilet, desk, ...

**Electrónica:**
laptop, mouse, remote, keyboard, microwave, oven, toaster, ...

**Deportes:**
tennis racket, baseball bat, skateboard, surfboard, ...

Ver lista completa: [COCO Dataset Classes](https://cocodataset.org/)

---

**¡Listo para detectar objetos en tiempo real!** 🎉
