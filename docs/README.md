# 📖 Documentación YOLO Light

Bienvenido a la documentación completa de YOLO Light API.

---

## � Guías Disponibles

| Sección | Descripción |
|---------|-------------|
| **[🚀 Instalación](guides/INSTALLATION.md)** | Paso a paso: Docker, Docker Compose, RPi4 |
| **[📸 Ejemplos Prácticos](EXAMPLES.md)** | Casos reales con imágenes de resultado |
| **[📚 API Reference](guides/API_REFERENCE.md)** | Todos los endpoints documentados |
| **[🏠 CasaOS](guides/CASAOS.md)** | Instalación con interfaz gráfica |
| **[🐧 RPi4 Deployment](guides/DEPLOYMENT_RPI4.md)** | Deploy específico para Raspberry Pi 4 |
| **[⚙️ GitHub Actions](guides/GITHUB_ACTIONS.md)** | Setup CI/CD para compilaciones automáticas |

---

## 📸 Ejemplos Visuales

### Detección en Acción

**Entrada:**
![Input](./examples/input_example.jpg)

**Salida (con bounding boxes):**
![Output](./examples/output_example.jpg)

**Características:**
- ✅ Rectángulos de colores para cada objeto
- ✅ Etiquetas con clase y confianza
- ✅ Colores variados por objeto
- ✅ Mantiene resolución original

Ver más: [Ejemplos de Uso](EXAMPLES.md)

---

## 🎯 Guías por Caso de Uso

### 👤 Para Principiantes
1. Lee: [Inicio Rápido](guides/INSTALLATION.md)
2. Instala: Docker + imagen hn8888/yolo-light
3. Prueba: `curl http://localhost:8000/health`
4. Detecta: Envía una imagen al endpoint `/detect`

### 🏢 Para Producción
1. Lee: [Guía de Instalación](guides/INSTALLATION.md)
2. Configura: Docker Compose con recursos limitados
3. Monitoring: Setup health checks
4. Seguridad: Proxy reverso con SSL
5. Escalado: Múltiples contenedores

### 🔧 Para Desarrolladores
1. Lee: [API Reference](guides/API_REFERENCE.md)
2. Estudia: Estructura de requests/responses
3. Integra: Usa Python, Node.js, Bash, etc.
4. Optimiza: Ajusta modelos y parámetros

### 📊 Para Data Scientists
1. Lee: [Clases COCO](guides/API_REFERENCE.md#-clases-detectadas-coco-dataset)
2. Experimenta: Prueba diferentes modelos (yolov5n, yolov5m, yolov11n, etc.)
3. Analiza: JSON responses con coordenadas exactas
4. Entrena: Fine-tune modelos personalizados

---

## 🔍 Búsqueda Rápida

### ¿Cómo...?

- **¿Instalar en RPi4?** → [Instalación RPi4](guides/INSTALLATION.md)
- **¿Usar modelo diferente?** → [Cambiar Modelo](EXAMPLES.md#configuración-de-modelos)
- **¿Obtener JSON con detecciones?** → [POST /detect](guides/API_REFERENCE.md#3️⃣-post-detect)
- **¿Obtener imagen con boxes?** → [POST /detect-visual](guides/API_REFERENCE.md#4️⃣-post-detect-visual)
- **¿Ver todas las clases?** → [COCO Classes](guides/API_REFERENCE.md#-clases-detectadas-coco-dataset)
- **¿Resolver problemas?** → [Troubleshooting](guides/INSTALLATION.md#-troubleshooting)
- **¿Monitorear rendimiento?** → [Monitoreo](guides/INSTALLATION.md#-monitoreo)

---

## 📋 Requisitos Mínimos

```
Hardware: Raspberry Pi 4 (2GB+ RAM)
Software: Docker 20.10+
Espacio: 1.5-2GB en disco
Red: Conexión para descargar imagen (~1.5-2GB)
```

---

## 🎓 Estructura de Carpetas

```
docs/
├── README.md                    ← Estás aquí
├── EXAMPLES.md                  ← Ejemplos prácticos con imágenes
├── guides/
│   ├── INSTALLATION.md          ← Guía de instalación detallada
│   └── API_REFERENCE.md         ← Referencia técnica de endpoints
└── examples/
    ├── input_example.jpg        ← Imagen de entrada de ejemplo
    └── output_example.jpg       ← Imagen con detecciones (output)
```

---

## 🔗 Enlaces Útiles

- **GitHub:** https://github.com/hlavrencic/yolo-light
- **Docker Hub:** https://hub.docker.com/r/hn8888/yolo-light
- **Ultralytics YOLO:** https://github.com/ultralytics/yolov5
- **COCO Dataset:** https://cocodataset.org/
- **FastAPI Docs:** https://fastapi.tiangolo.com/

---

## 🆘 Soporte

- **Issues:** [GitHub Issues](https://github.com/hlavrencic/yolo-light/issues)
- **Documentación:** Esta carpeta (`/docs`)
- **Logs:** `docker logs yolo-api`
- **Health Check:** `curl http://localhost:8000/health`

---

## 📜 Licencia

CC BY-NC 4.0 (Non-Commercial Use Only)

---

**¡Feliz detección de objetos!** 🎉
