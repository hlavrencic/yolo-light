# 🚀 Guía Completa de Instalación

Instrucciones detalladas para instalar YOLO Light en diferentes plataformas.

## 📋 Requisitos Previos

### Hardware Mínimo
- Raspberry Pi 4 (2GB RAM)
- O: Máquina amd64 con Docker

### Software Requerido
- Docker 20.10+
- Docker Compose (opcional)
- 1.5-2GB de espacio en disco

---

## 💻 Instalación en Raspberry Pi 4

### Opción 1: Con Docker (Recomendado)

**Paso 1: Verificar Docker**
```bash
docker --version
```

Si no está instalado:
```bash
curl -sSL https://get.docker.com | sh
sudo usermod -aG docker $USER
```

**Paso 2: Descargar imagen**
```bash
docker pull hn8888/yolo-light:arm64
```

**Paso 3: Ejecutar contenedor**
```bash
docker run -d \
  -p 8000:8000 \
  --name yolo-api \
  --memory=1.5G \
  hn8888/yolo-light:arm64
```

**Paso 4: Verificar**
```bash
curl http://localhost:8000/health
```

---

### Opción 2: Con Docker Compose

**1. Crear `docker-compose.yml`:**
```yaml
version: '3.8'

services:
  yolo-api:
    image: hn8888/yolo-light:arm64
    container_name: yolo-api
    ports:
      - "8000:8000"
    environment:
      - MODEL_NAME=yolov5n.pt
    memory: 1.5G
    restart: unless-stopped
```

**2. Ejecutar:**
```bash
docker-compose up -d
```

**3. Verificar:**
```bash
docker-compose logs -f yolo-api
```

---

### Opción 3: Con CasaOS (GUI)

**Paso 1:** Abre http://casaos.local:81

**Paso 2:** App Management → App Store

**Paso 3:** Busca "yolo-light" o importa manualmente

**Paso 4:** Click Deploy

Ver: [CASAOS_IMPORT.md](../CASAOS_IMPORT.md)

---

## 🖥️ Instalación en PC/Servidor (amd64)

### Opción 1: Imagen Docker Hub

```bash
docker pull hn8888/yolo-light:latest

docker run -d \
  -p 8000:8000 \
  --name yolo-api \
  --memory=2G \
  hn8888/yolo-light:latest
```

### Opción 2: Compilar Localmente

```bash
git clone https://github.com/hlavrencic/yolo-light.git
cd yolo-light

docker build -t yolo-light:local .

docker run -d -p 8000:8000 --memory=2G yolo-light:local
```

---

## 🔧 Configuración Avanzada

### Cambiar Modelo

```bash
docker run -d \
  -e MODEL_NAME=yolov5m.pt \
  -p 8000:8000 \
  --memory=2G \
  hn8888/yolo-light:latest
```

### Puerto Personalizado

```bash
docker run -d \
  -p 9000:8000 \
  --name yolo-api \
  hn8888/yolo-light:latest

# Acceder en http://localhost:9000
```

### Limitar CPU

```bash
docker run -d \
  -p 8000:8000 \
  --cpus=1.5 \
  --memory=1.5G \
  hn8888/yolo-light:latest
```

### Volumen Persistente (para modelos)

```bash
docker volume create yolo-models

docker run -d \
  -p 8000:8000 \
  -v yolo-models:/root/.cache \
  hn8888/yolo-light:latest
```

---

## 📊 Monitoreo

### Ver Logs en Tiempo Real

```bash
docker logs -f yolo-api
```

### Ver Estadísticas

```bash
docker stats yolo-api
```

### Verificar Estado

```bash
curl http://localhost:8000/health
```

---

## 🛑 Parar y Eliminar

```bash
# Parar contenedor
docker stop yolo-api

# Reiniciar
docker restart yolo-api

# Eliminar
docker rm yolo-api

# Eliminar imagen
docker rmi hn8888/yolo-light:arm64
```

---

## ❌ Troubleshooting

### "Port 8000 already in use"
```bash
docker stop <container_name>
# O usar puerto diferente: -p 8001:8000
```

### "Insufficient memory"
Aumentar memoria en docker run:
```bash
--memory=2G  # o más
```

### "Model download failed"
Verificar internet y reintentar:
```bash
docker restart yolo-api
docker logs yolo-api
```

### "Detections are very slow"
Usar modelo más ligero:
```bash
-e MODEL_NAME=yolov5n.pt
```

---

## ✅ Verificación de Instalación

```bash
# 1. Contenedor corriendo
docker ps | grep yolo-api

# 2. Health check
curl http://localhost:8000/health

# 3. Información API
curl http://localhost:8000/

# 4. Probar detección
curl -X POST -F "file=@test.jpg" http://localhost:8000/detect
```

---

**¡Ya está listo para usar!** 🎉
