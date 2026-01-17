# 📚 YOLO Light API Reference

Documentación técnica completa de todos los endpoints disponibles.

---

## 🌐 Base URL

```
http://localhost:8000
http://192.168.x.x:8000  (RPi4 en la red)
```

---

## 1️⃣ GET `/`

**Descripción:** Información de la API y endpoints disponibles

**Request:**
```bash
curl http://localhost:8000/
```

**Response (200 OK):**
```json
{
  "title": "YOLO Light API",
  "version": "1.0.0",
  "description": "Lightweight object detection API for Raspberry Pi 4",
  "endpoints": {
    "health": "GET /health",
    "info": "GET /",
    "detect_json": "POST /detect",
    "detect_visual": "POST /detect-visual"
  }
}
```

---

## 2️⃣ GET `/health`

**Descripción:** Health check - Estado del modelo y API

**Request:**
```bash
curl http://localhost:8000/health
```

**Response (200 OK):**
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

**Status Codes:**
- `200` - API healthy, modelo cargado
- `500` - Error en el modelo

---

## 3️⃣ POST `/detect`

**Descripción:** Detectar objetos y retornar JSON con coordenadas

**Request:**
```bash
curl -X POST \
  -F "file=@image.jpg" \
  http://localhost:8000/detect
```

**Parameters:**
- `file` (multipart/form-data, requerido): Archivo de imagen (JPG, PNG, etc)

**Tipos MIME aceptados:**
- image/jpeg
- image/png
- image/gif
- image/webp

**Response (200 OK):**
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
      "class": "chair",
      "confidence": 0.74,
      "x1": 800,
      "y1": 600,
      "x2": 950,
      "y2": 800
    }
  ]
}
```

**Response (400 Bad Request):**
```json
{
  "success": false,
  "error": "El archivo debe ser una imagen (JPG, PNG, etc)"
}
```

**Response (500 Internal Server Error):**
```json
{
  "success": false,
  "error": "Error en detección: <detalles del error>"
}
```

---

## 4️⃣ POST `/detect-visual`

**Descripción:** Detectar objetos y retornar PNG con bounding boxes dibujados

**Request:**
```bash
curl -X POST \
  -F "file=@image.jpg" \
  http://localhost:8000/detect-visual \
  -o detected.png
```

**Parameters:**
- `file` (multipart/form-data, requerido): Archivo de imagen

**Response (200 OK):**
- Content-Type: `image/png`
- Body: Archivo PNG binario
- Headers: `Content-Disposition: attachment; filename=detected_<original_name>`

**Características del PNG:**
- ✅ Bounding boxes de colores
- ✅ Etiquetas con clase y confianza
- ✅ Resolución original preservada
- ✅ Formato PNG comprimido

**Response (400 Bad Request):**
```json
{
  "success": false,
  "error": "El archivo debe ser una imagen (JPG, PNG, etc)"
}
```

---

## 📊 Modelos Disponibles

Puedes usar cualquier modelo YOLO especificando `MODEL_NAME`:

### YOLOv5 Series
- `yolov5n.pt` (7.5MB) ⭐ **Recomendado para RPi4**
- `yolov5s.pt` (16MB)
- `yolov5m.pt` (40MB)
- `yolov5l.pt` (90MB)
- `yolov5x.pt` (168MB)

### YOLOv11 Series
- `yolov11n.pt` (8MB)
- `yolov11s.pt` (20MB)
- `yolov11m.pt` (50MB)
- `yolov11l.pt` (110MB)
- `yolov11x.pt` (210MB)

**Cambiar modelo:**
```bash
docker run -d -e MODEL_NAME=yolov5s.pt -p 8000:8000 hn8888/yolo-light:arm64
```

---

## 🔢 Clases Detectadas (COCO Dataset)

El modelo detecta 80 clases COCO:

### Personas y Animales (10)
person, bicycle, car, motorcycle, airplane, bus, train, truck, boat, traffic light

### Animales (10)
dog, cat, horse, sheep, cow, elephant, bear, zebra, giraffe, backpack

### Objetos Deportivos (10)
frisbee, skis, snowboard, sports ball, kite, baseball bat, baseball glove, skateboard, surfboard, tennis racket

### Muebles y Hogar (20)
bottle, wine glass, cup, fork, knife, spoon, bowl, banana, apple, sandwich, orange, broccoli, carrot, hot dog, pizza, donut, cake, chair, couch, potted plant

### Objetos Tecnológicos (10)
bed, dining table, toilet, tv, laptop, mouse, remote, keyboard, microwave, oven

[Ver lista completa →](https://cocodataset.org/#explore)

---

## ⏱️ Timeouts y Límites

| Límite | Valor | Notas |
|--------|-------|-------|
| Request timeout | 60s | Aumentar en --request-timeout si es necesario |
| Max image size | Unlimited | Limitado por RAM disponible |
| Batch processing | 1 imagen por request | Para múltiples: enviar requests secuencialmente |

---

## 🔐 Seguridad

- ✅ No hay autenticación (localhost/red local)
- ✅ No hay CORS habilitado (API local)
- ⚠️ Para exponer públicamente: usar proxy reverso con SSL

---

## 📈 Rendimiento

### Tiempos Típicos

| Plataforma | Modelo | Resolución | Inferencia | Total |
|-----------|--------|-----------|-----------|-------|
| RPi4 arm64 | yolov5n | 640x640 | 150-200ms | 200-250ms |
| RPi4 arm64 | yolov5n | 1920x1255 | 100-150ms | 150-200ms |
| PC amd64 | yolov5n | 1920x1255 | 50-80ms | 80-120ms |
| PC amd64 | yolov5m | 1920x1255 | 100-150ms | 150-200ms |

---

## 🔧 Ejemplos de Uso

### Python
```python
import requests

# Detección JSON
with open('image.jpg', 'rb') as f:
    files = {'file': f}
    response = requests.post('http://localhost:8000/detect', files=files)
    print(response.json())

# Detección Visual
with open('image.jpg', 'rb') as f:
    files = {'file': f}
    response = requests.post('http://localhost:8000/detect-visual', files=files)
    with open('detected.png', 'wb') as out:
        out.write(response.content)
```

### JavaScript/Node.js
```javascript
const FormData = require('form-data');
const fs = require('fs');

const form = new FormData();
form.append('file', fs.createReadStream('image.jpg'));

fetch('http://localhost:8000/detect', {
  method: 'POST',
  body: form
})
  .then(r => r.json())
  .then(data => console.log(data));
```

### Bash
```bash
# JSON
curl -X POST -F "file=@image.jpg" http://localhost:8000/detect | jq

# PNG
curl -X POST -F "file=@image.jpg" http://localhost:8000/detect-visual -o result.png
```

---

## ❌ Códigos de Error

| Código | Descripción | Solución |
|--------|-------------|----------|
| 400 | Bad Request - Archivo no es imagen | Verificar formato y MIME type |
| 500 | Internal Server Error | Ver logs: `docker logs yolo-api` |
| 503 | Service Unavailable | Modelo aún cargando, reintentar |

---

**¡API lista para detectar objetos!** 🎉
