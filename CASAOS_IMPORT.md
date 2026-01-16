# 🏠 YOLO Light en CasaOS

Guía completa para importar y ejecutar YOLO Light API en CasaOS (Raspberry Pi 4).

## 📋 Requisitos Previos

- ✅ CasaOS instalado en RPi4
- ✅ Acceso a internet (descargar imagen desde Docker Hub)
- ✅ Al menos 1.5GB de RAM disponible
- ✅ Al menos 2GB de espacio en disco

## 🚀 Opción 1: Importar desde docker-compose.yml (Recomendado)

### Paso 1: Descargar el archivo

Opción A - Desde terminal:
```bash
# SSH a tu RPi4
ssh pi@casaos.local

# Descargar el archivo
cd /home/pi
wget https://raw.githubusercontent.com/tuusuario/yolo-light/main/docker-compose.yml

# O copiar desde tu PC
scp docker-compose.yml pi@casaos.local:/home/pi/
```

Opción B - Crear manualmente en CasaOS:
1. Abre CasaOS en tu navegador: `http://casaos.local:81`
2. Ve a **App Management** → **Compose**
3. Copia y pega el contenido del `docker-compose.yml`

### Paso 2: Ejecutar en CasaOS

```bash
# En la terminal de tu RPi4
docker-compose -f docker-compose.yml up -d
```

O desde la interfaz CasaOS:
1. **App Management** → **Compose**
2. Pega el YAML
3. Click en **Deploy** o **Run**

### Paso 3: Verificar que está corriendo

```bash
# Ver logs
docker logs -f yolo-light-api

# Verificar salud
curl http://casaos.local:8000/health

# Response esperado:
# {"status":"healthy","model":"YOLO11n"}
```

---

## 🎯 Opción 2: Importar desde GUI CasaOS

### Método A: App Store (Si está disponible)

1. Abre CasaOS: `http://casaos.local:81`
2. **App Store** → Buscar "YOLO" o "yolo-light"
3. Click en **Install**
4. Espera 2-3 minutos a que descargue

### Método B: Compose desde GUI

1. **App Management** → **Compose**
2. Click en **New**
3. Pega este YAML:

```yaml
version: '3.8'

services:
  yolo-light:
    image: hn8888/yolo-light:arm64
    container_name: yolo-light-api
    ports:
      - "8000:8000"
    deploy:
      resources:
        limits:
          memory: 1.5G
        reservations:
          memory: 1G
    environment:
      - CONFIDENCE=0.4
      - PORT=8000
    restart: unless-stopped
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8000/health"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 10s
    logging:
      driver: "json-file"
      options:
        max-size: "10m"
        max-file: "3"
```

4. Click en **Deploy** → Espera 1-2 minutos

---

## ✅ Verificación Rápida

Después de importar, verifica que todo funciona:

### 1. Verificar contenedor
```bash
docker ps | grep yolo-light
# Debe mostrar: yolo-light-api con status "Up"
```

### 2. Health Check
```bash
curl http://casaos.local:8000/health

# Response esperado:
{
  "status": "healthy",
  "model": "YOLO11n"
}
```

### 3. Probar detección
```bash
# Descargar imagen de prueba
wget https://raw.githubusercontent.com/tuusuario/yolo-light/main/testing/foto.jpg

# Enviar para detección
curl -X POST -F "file=@foto.jpg" http://casaos.local:8000/detect

# Response esperado:
{
  "success": true,
  "count": N,
  "inference_time_ms": XXX,
  "objects": [...]
}
```

---

## 🔧 Configuración en CasaOS

### Puertos
- **Puerto 8000** → API REST
  - Acceso: `http://casaos.local:8000`
  - Endpoints: `/health`, `/detect`, `/`

### Recursos (Preconfigurados)
- **Límite de RAM**: 1.5GB
- **Reserva de RAM**: 1GB
- **CPU**: Sin límite (usa lo que necesita)

### Reinicio Automático
- ✅ **Habilitado**: El contenedor se reinicia si cae
- Configuración: `restart: unless-stopped`

### Health Check
- ✅ **Habilitado**: Verifica cada 30 segundos
- URL: `http://localhost:8000/health`
- Automáticamente marca como "Unhealthy" si falla

### Logs
- 📊 Guardados localmente
- Tamaño máximo: 10MB por archivo
- Archivos guardados: 3 (rotación automática)

---

## 🎛️ Controlar desde CasaOS

### Ver logs en vivo
```bash
docker logs -f yolo-light-api
```

### Detener contenedor
```bash
docker stop yolo-light-api
```

### Reiniciar contenedor
```bash
docker restart yolo-light-api
```

### Remover (eliminar)
```bash
docker stop yolo-light-api
docker rm yolo-light-api
```

---

## 🌐 Acceso a la API desde otros dispositivos

Una vez en CasaOS, puedes acceder desde cualquier dispositivo en tu red:

### Desde PC/Mac
```bash
curl http://192.168.1.X:8000/health
# Reemplaza 192.168.1.X con la IP de tu RPi4
```

### Desde Navegador
```
http://casaos.local:8000/
http://192.168.1.X:8000/
```

### Desde tu teléfono
Instala una app para enviar POST requests (Postman, REST Client, etc.):
- URL: `http://192.168.1.X:8000/detect`
- Method: POST
- Body: multipart/form-data con `file=` (imagen)

---

## 🆘 Troubleshooting

### Error: "No space left on device"
```bash
# Limpiar espacio
docker system prune -a --volumes
# Requiere 2GB mínimo
```

### Error: "Out of memory"
```bash
# Aumentar límite en docker-compose.yml
# Cambiar:
# memory: 1.5G  →  memory: 2G
# memory: 1G    →  memory: 1.5G

docker-compose -f docker-compose.yml up -d
```

### API responde lentamente
```bash
# Verificar recursos disponibles
free -h
df -h

# Reiniciar contenedor
docker restart yolo-light-api

# Ver si hay muchos procesos
ps aux | grep python
```

### No se conecta a `casaos.local`
- Verificar que el DNS está funcionando
- Usar IP directa: `http://192.168.1.X:8000`
- Reiniciar router y RPi4

### Imagen no descarga
```bash
# Descargar manualmente
docker pull hn8888/yolo-light:arm64

# Luego ejecutar el compose
docker-compose -f docker-compose.yml up -d
```

---

## 📊 Monitoreo en CasaOS

### Dashboard de CasaOS
1. Abre `http://casaos.local:81`
2. **Containers** → Busca "yolo-light-api"
3. Ver:
   - Status (Running/Stopped)
   - CPU usage
   - Memory usage
   - Logs en tiempo real

### Comando para monitoreo continuo
```bash
docker stats yolo-light-api --no-stream
```

---

## 🚀 Actualizar a nueva versión

Cuando saques una nueva versión en GitHub Actions:

### Opción 1: Terminal
```bash
# Detener antiguo
docker stop yolo-light-api

# Descargar nueva imagen
docker pull hn8888/yolo-light:arm64

# Ejecutar nueva
docker-compose -f docker-compose.yml up -d
```

### Opción 2: CasaOS GUI
1. **App Management** → Busca "yolo-light-api"
2. Click en **Update** o **Redeploy**
3. Espera 1-2 minutos

---

## 📚 Recursos Adicionales

| Recurso | Link |
|---------|------|
| GitHub repo | [yolo-light](https://github.com/tuusuario/yolo-light) |
| Docker Hub | [hn8888/yolo-light](https://hub.docker.com/r/hn8888/yolo-light) |
| CasaOS Docs | [docs.casaos.io](https://docs.casaos.io) |
| API Docs | Ver `/` endpoint |

---

## 💡 Tips y Trucos

### Ejecutar en background
```bash
# Ya está configurado en docker-compose.yml
# Pero si quieres hacerlo manualmente:
docker run -d --name yolo-light-api \
  -p 8000:8000 \
  --memory=1.5G \
  hn8888/yolo-light:arm64
```

### Acceder a archivos del contenedor
```bash
docker exec -it yolo-light-api bash
# Ya estás adentro del contenedor
ls -la
```

### Ver puertos abiertos
```bash
docker port yolo-light-api
# Output: 8000/tcp -> 0.0.0.0:8000
```

### Hacer backup de configuración
```bash
docker inspect yolo-light-api > yolo-light-backup.json
```

---

## ✨ Siguiente Paso

Después de importar en CasaOS:

1. ✅ Accede a `http://casaos.local:8000`
2. ✅ Prueba `/health` endpoint
3. ✅ Prueba `/detect` con una imagen
4. ✅ Verifica logs: `docker logs -f yolo-light-api`
5. ✅ Configura automatización (opcional)

¡Ya tienes YOLO Light corriendo en tu CasaOS! 🎉
