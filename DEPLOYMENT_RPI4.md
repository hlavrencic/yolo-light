# YOLO Light - Guía de Migración a Raspberry Pi 4

## Estado Actual (Desarrollo)

✅ **API funcionando** con modo TFLite simulado  
✅ **Docker buildable** para x86_64  
✅ **Endpoints validados** (/health, /, /detect)  
✅ **Respuestas JSON** con formato correcto  

## Pasos para RPi4 Producción

### 1. Preparar el Modelo TFLite en RPi4

```bash
# Opción A: Descargarlo en RPi4
scp yolo11n_float16.tflite pi@raspberry.local:/home/pi/yolo-light/

# Opción B: Pre-incluirlo en Docker (si tienes el archivo)
# Coloca yolo11n_float16.tflite en src/ antes de construir
cp yolo11n_float16.tflite src/
git add src/yolo11n_float16.tflite
```

### 2. Instalar tflite-runtime en RPi4

#### Opción A: Paquete APT (RECOMENDADO)

```bash
# En RPi4 con Raspberry Pi OS
ssh pi@raspberry.local

# Instalar desde repositorio oficial
sudo apt-get update
sudo apt-get install -y python3-tflite-runtime

# Verificar instalación
python3 -c "import tflite_runtime.interpreter; print('✓ TFLite ready')"
```

#### Opción B: Compilar desde fuente

```bash
# En RPi4 (toma 30-45 minutos)
git clone https://github.com/tensorflow/tensorflow.git
cd tensorflow
./tensorflow/lite/tools/pip_package/build_pip_package_with_cmake.sh

pip install /tmp/tensorflow_lite_*.whl
```

#### Opción C: Usar pip (Python 3.9 solamente)

```bash
# Solo funciona en Python 3.9
python3.9 -m pip install tflite-runtime

# Si tienes Python 3.11, instala primero 3.9
sudo apt-get install python3.9 python3.9-venv
```

### 3. Actualizar main.py

**Opción A: Usar main_tflite_production.py** (RECOMENDADO)

```bash
# Reemplazar con la versión de producción
cp src/main.py src/main_demo.py
cp src/main_tflite_production.py src/main.py
```

**Opción B: Editar manualmente**

En `src/main.py`, reemplaza la función `simulate_tflite_detections()` con la implementación real de `main_tflite_production.py`:
- Importar `tflite_runtime.interpreter`
- Cargar modelo en `startup()`
- Ejecutar `run_tflite_inference()` en lugar de `simulate_tflite_detections()`

### 4. Ajustar requirements.txt para RPi4

```txt
fastapi==0.104.1
uvicorn==0.24.0
pillow==10.1.0
numpy==1.24.3
python-multipart==0.0.6
# tflite-runtime==2.14.0  # Instalar vía APT en RPi4, NO por pip
```

### 5. Construir imagen Docker ARM64

```bash
# EN RPi4 (construcción nativa - más rápida)
cd ~/yolo-light
docker build -t yolo-light:arm64 .

# DESDE otra máquina con Docker BuildX (cross-compile)
docker buildx create --name mybuilder
docker buildx use mybuilder
docker buildx build --platform linux/arm64 -t yolo-light:arm64 .
```

### 6. Ejecutar con límites de memoria

```bash
# Parar contenedor anterior
docker stop yolo-api
docker rm yolo-api

# Ejecutar con memoria limitada
docker run -d \
  -p 8000:8000 \
  --memory=1.5G \
  --cpus="3" \
  --name yolo-api \
  yolo-light:arm64

# Ver logs
docker logs -f yolo-api

# Monitorear recursos
docker stats yolo-api
```

### 7. Verificar inferencia real

```bash
# Test health check
curl http://localhost:8000/health | python3 -m json.tool

# Test inferencia (compara con modo demo)
curl -X POST -F "file=@foto.jpg" http://localhost:8000/detect | python3 -m json.tool

# Monitorear tiempo de inferencia
watch -n 1 'curl -s -X POST -F "file=@foto.jpg" http://localhost:8000/detect | grep inference_time'
```

## Comparación: Demo vs Producción

| Métrica | Demo (Simulado) | Producción (TFLite) |
|---------|-----------------|-------------------|
| Tiempo inferencia | ~180-350ms | ~200-400ms |
| CPU | Bajo | Alto (4 threads) |
| RAM | ~300MB | ~800-1200MB |
| Precisión | Falso (simulado) | Real (YOLO11n) |
| Modo activación | Siempre | Con tflite-runtime |

## Troubleshooting

### Error: "No module named 'tflite_runtime'"

```bash
# Verificar instalación
python3 -c "import tflite_runtime; print(tflite_runtime.__version__)"

# Si falla, reinstalar
sudo apt-get install --reinstall python3-tflite-runtime

# O compilar desde fuente (ver arriba)
```

### Error: "Out of memory"

```bash
# Reducir memoria de Docker
docker stop yolo-api
docker run ... --memory=1G yolo-light:arm64

# O aumentar swap del RPi4
sudo dphys-swapfile swapoff
sudo nano /etc/dphys-swapfile  # Cambiar CONF_SWAPSIZE a 2048
sudo dphys-swapfile setup
sudo dphys-swapfile swapon
```

### Error: "Cannot open shared object file"

```bash
# Instalar librerías de sistema faltantes
sudo apt-get install -y \
  libopenblas-dev \
  libjasper-dev \
  libtiff-dev \
  libwebp6 \
  libjasper1 \
  libharfbuzz0b \
  libwebp6
```

### Inferencia muy lenta (>1s)

```bash
# Ajustar threads (por defecto 4 en RPi4)
# En main_tflite_production.py, línea ~80:
interpreter = tflite.Interpreter(
    model_path=model_path,
    num_threads=2  # Reducir de 4 a 2 para mejor latencia
)

# También reducir imagen de entrada si no necesitas precisión máxima
# En parse_yolo_output: aumentar conf_threshold de 0.4 a 0.5
```

## Monitoreo en Producción

```bash
# Script para monitoring continuo
while true; do
  echo "=== $(date) ==="
  docker stats yolo-api --no-stream
  curl -s http://localhost:8000/health | python3 -m json.tool | grep -E "status|inference"
  sleep 10
done
```

## Métricas Esperadas en RPi4

- **Memoria**: 800-1200 MB en tiempo de ejecución
- **CPU**: ~80-95% de un core durante inferencia
- **Latencia**: 200-400ms por imagen (CPU-only)
- **Throughput**: 2-5 imágenes/segundo
- **Uptime**: Días sin reinicio si memoria se monitorea

## Backup: Volver a Demo

Si tflite-runtime da problemas:

```bash
# Usar versión demo
cp src/main_demo.py src/main.py

# Rebuild
docker build -t yolo-light:demo .
docker run -d -p 8000:8000 --name yolo-api yolo-light:demo

# Seguirá respondiendo con detecciones simuladas
```

## Próximos Pasos

1. ✅ Validar en desarrollo (completado)
2. ⏳ Instalar tflite-runtime en RPi4
3. ⏳ Copiar modelo TFLite a RPi4
4. ⏳ Reemplazar main.py con versión producción
5. ⏳ Construir imagen ARM64
6. ⏳ Ejecutar y validar inferencia real
7. ⏳ Monitorear métricas en producción
8. ⏳ Ajustar parámetros según carga

---

**Nota**: El proceso completo toma ~2-3 horas incluyendo instalación de dependencias y compilación en RPi4. Para cross-compilation desde otra máquina, el tiempo se reduce a ~30 minutos.
