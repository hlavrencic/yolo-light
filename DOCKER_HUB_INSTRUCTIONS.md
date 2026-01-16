# 🚀 Descargar e Instalar YOLO Light API en Raspberry Pi 4

## Imagen Publicada en Docker Hub

Tu imagen está disponible en:
```
hn8888/yolo-light:latest    (Development - x86_64)
hn8888/yolo-light:v1.0      (Current version)
hn8888/yolo-light:dev       (Alias para latest)
```

**URL**: https://hub.docker.com/r/hn8888/yolo-light

---

## ⚡ Instalación Rápida en RPi4

### 1. Conectar a RPi4

```bash
ssh pi@raspberry.local
# O con IP: ssh pi@192.168.x.x
```

### 2. Instalar Docker (si no está instalado)

```bash
# Actualizar sistema
sudo apt-get update
sudo apt-get upgrade -y

# Instalar Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh

# Permitir usar docker sin sudo
sudo usermod -aG docker pi
newgrp docker

# Verificar
docker --version
```

### 3. Descargar la Imagen

```bash
# Opción A: Desde Docker Hub (RECOMENDADO)
docker pull hn8888/yolo-light:latest

# O versión específica
docker pull hn8888/yolo-light:v1.0

# Verificar que está descargada
docker images | grep yolo-light
```

### 4. Ejecutar Contenedor

```bash
# Crear directorio para datos
mkdir -p ~/yolo-light-data

# Ejecutar contenedor
docker run -d \
  -p 8000:8000 \
  --memory=1.5G \
  --cpus="3" \
  --name yolo-api \
  --restart unless-stopped \
  hn8888/yolo-light:latest

# Ver logs
docker logs -f yolo-api
```

### 5. Verificar que Funciona

```bash
# Health check
curl http://localhost:8000/health

# Ver info de la API
curl http://localhost:8000/

# Probar con imagen de prueba (copiar una imagen primero)
curl -X POST -F "file=@foto.jpg" http://localhost:8000/detect
```

---

## 📋 Comandos Útiles

### Monitoreo

```bash
# Ver recursos en uso
docker stats yolo-api

# Ver logs en vivo
docker logs -f yolo-api

# Ver últimas 50 líneas
docker logs --tail 50 yolo-api
```

### Control del Contenedor

```bash
# Parar
docker stop yolo-api

# Iniciar (después de parar)
docker start yolo-api

# Reiniciar
docker restart yolo-api

# Eliminar
docker stop yolo-api
docker rm yolo-api

# Entrar al shell del contenedor
docker exec -it yolo-api bash
```

### Limpiar Recursos

```bash
# Eliminar imagen
docker rmi hn8888/yolo-light:latest

# Limpiar todo (containers parados, imágenes no usadas, etc)
docker system prune -a

# Ver uso de espacio
docker system df
```

---

## 🔧 Configuración Avanzada

### Aumentar Límite de Memoria

Si RPi4 tiene Out of Memory, aumenta:

```bash
docker run -d \
  -p 8000:8000 \
  --memory=2G \
  --cpus="4" \
  --name yolo-api \
  hn8888/yolo-light:latest
```

### Montaje de Volumen para Guardar Datos

```bash
docker run -d \
  -p 8000:8000 \
  -v ~/yolo-data:/app/models \
  --name yolo-api \
  hn8888/yolo-light:latest
```

### Auto-reinicio

Agregado en el comando anterior: `--restart unless-stopped`

Otras opciones:
- `--restart always` - Reiniciar siempre
- `--restart on-failure:5` - Reiniciar si falla, máx 5 veces
- `--restart unless-stopped` - Reiniciar excepto si fue detenido

### Exponerlo en Red (Acceso desde otras máquinas)

```bash
# Ya lo hace por defecto con -p 8000:8000
# Acceder desde otra máquina en la red:
curl http://raspi-ip:8000/health
```

---

## 🎯 Casos de Uso

### A. API Ligera para Testing

```bash
docker run -d -p 8000:8000 --name yolo-api hn8888/yolo-light:latest
```

### B. Servidor de Producción

```bash
docker run -d \
  -p 8000:8000 \
  --memory=1.5G \
  --cpus="3" \
  --name yolo-api \
  --restart unless-stopped \
  --log-driver json-file \
  --log-opt max-size=10m \
  --log-opt max-file=3 \
  hn8888/yolo-light:latest
```

### C. Con Proxy Reverso (Nginx)

```bash
# Instalar nginx
sudo apt-get install nginx

# Configurar (en /etc/nginx/sites-available/default)
upstream yolo {
    server 127.0.0.1:8000;
}

server {
    listen 80;
    server_name _;
    
    location / {
        proxy_pass http://yolo;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}

# Reiniciar nginx
sudo systemctl restart nginx

# Acceder por puerto 80
curl http://raspi-ip/health
```

---

## 🐛 Troubleshooting

### Error: "No space left on device"

```bash
# Ver espacio
df -h

# Limpiar Docker
docker system prune -a

# Eliminar imágenes viejas
docker image prune -a
```

### Error: "Cannot connect to Docker daemon"

```bash
# Verificar que Docker está corriendo
sudo systemctl status docker

# Iniciar si está parado
sudo systemctl start docker

# Habilitar al boot
sudo systemctl enable docker
```

### Error: "Out of memory"

```bash
# Ver memoria usada
docker stats yolo-api

# Reduce las opciones de memoria
docker stop yolo-api
docker rm yolo-api

# Ejecutar con menos memoria (1GB en lugar de 1.5GB)
docker run -d -p 8000:8000 --memory=1G --name yolo-api hn8888/yolo-light:latest
```

### API responde lentamente

```bash
# Ver si está saturado CPU
docker stats yolo-api

# Reduce concurrent requests o aumenta CPUs
# Para aumentar CPUs:
docker run -d -p 8000:8000 --cpus="4" --name yolo-api hn8888/yolo-light:latest
```

### "Cannot pull image"

```bash
# Verificar conexión a internet
ping docker.io

# Intentar login a Docker Hub
docker login

# Luego pull nuevamente
docker pull hn8888/yolo-light:latest
```

---

## 📊 Monitoreo en Producción

### Ver Métrica en Tiempo Real

```bash
# CPU, Memoria, Red, Disco
watch -n 1 'docker stats yolo-api --no-stream'

# O con formato personalizado
docker stats --no-stream --format "table {{.Container}}\t{{.CPUPerc}}\t{{.MemUsage}}"
```

### Logs Persistentes

```bash
# Ver logs con timestamps
docker logs -t yolo-api

# Ver últimas 100 líneas
docker logs --tail 100 yolo-api

# Seguir logs en vivo
docker logs -f --tail 50 yolo-api
```

### Script de Monitoreo

```bash
#!/bin/bash
# monitor.sh

while true; do
  clear
  echo "=== YOLO Light API Monitor ==="
  echo "Tiempo: $(date)"
  echo ""
  echo "=== Status del Contenedor ==="
  docker ps | grep yolo-api
  echo ""
  echo "=== Recursos ==="
  docker stats yolo-api --no-stream
  echo ""
  echo "=== Health Check ==="
  curl -s http://localhost:8000/health | python3 -m json.tool
  echo ""
  sleep 5
done

# Ejecutar:
# bash monitor.sh
```

---

## 🚀 Versión Mejorada con TFLite Real

Si deseas usar el modelo TFLite real (en lugar de simulación):

### 1. Instalar tflite-runtime

```bash
sudo apt-get install python3-tflite-runtime
```

### 2. Descargar Archivo Mejorado

```bash
# Crear directorio
mkdir -p ~/yolo-light
cd ~/yolo-light

# Copiar archivo (desde tu PC)
scp src/main_tflite_production.py pi@raspberry.local:~/yolo-light/

# O descargarlo desde GitHub (si está disponible)
wget https://raw.githubusercontent.com/tu-usuario/yolo-light/main/src/main_tflite_production.py
```

### 3. Reemplazar main.py

```bash
# Conectar a RPi4
ssh pi@raspberry.local

# Dentro del contenedor (si necesitas)
docker exec -it yolo-api bash

# O si construyes imagen local:
# Reemplazar main.py antes de hacer docker build
```

---

## 📝 Resumen de Comandos

```bash
# Download
docker pull hn8888/yolo-light:latest

# Run
docker run -d -p 8000:8000 --memory=1.5G --name yolo-api hn8888/yolo-light:latest

# Test
curl http://localhost:8000/health

# Logs
docker logs -f yolo-api

# Stats
docker stats yolo-api

# Stop
docker stop yolo-api

# Cleanup
docker system prune -a
```

---

## 📚 Documentación Adicional

- Repositorio GitHub: [tu-repo-aqui]
- Docker Hub: https://hub.docker.com/r/hn8888/yolo-light
- API Docs: http://raspi-ip:8000/docs (Swagger UI)
- FastAPI: https://fastapi.tiangolo.com/
- Docker: https://docs.docker.com/

---

## ✅ Checklist de Instalación

- [ ] SSH conectado a RPi4
- [ ] Docker instalado (`docker --version`)
- [ ] Imagen descargada (`docker pull hn8888/yolo-light:latest`)
- [ ] Contenedor corriendo (`docker ps | grep yolo-api`)
- [ ] Health check responde (`curl http://localhost:8000/health`)
- [ ] Puerta 8000 expuesta (`netstat -tlnp | grep 8000`)
- [ ] Acceso desde red verificado

---

**¡Listo para usar!** 🎉

Si tienes problemas, revisa los logs: `docker logs -f yolo-api`
