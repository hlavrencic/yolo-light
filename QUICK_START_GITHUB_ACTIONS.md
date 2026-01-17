# 🚀 YOLO Light API - GitHub Actions para ARM64

## ¿Qué es esto?

**Sistema automático de compilación** de la imagen Docker ARM64 usando GitHub Actions.

Antes: Compilar en RPi4 (~30-45 minutos)  
Ahora: Compilar en GitHub (~15-20 minutos) ✨

---

## ✨ Ventajas

✅ **No consume recursos de RPi4**  
✅ **Compilación automática** en cada push  
✅ **Multi-arquitectura** (amd64, arm64, arm/v7)  
✅ **Resultados en Docker Hub** inmediatamente  
✅ **Caché inteligente** para builds más rápidos  

---

## 🎯 Flujo de Trabajo

```
Tu PC/Mac
  ↓
git push
  ↓
GitHub Actions (compilar)
  ↓
Docker Hub (publicar)
  ↓
RPi4 (docker pull)
```

---

## ⚡ Primer Setup (Una sola vez)

### 1. Agregar Secretos en GitHub

En tu repo de GitHub:
- Settings → Secrets and variables → Actions
- New repository secret

Agrega dos secretos:

```
Name: DOCKER_USERNAME
Value: hn8888

Name: DOCKER_PASSWORD
Value: (tu Docker Hub token)
```

Para obtener el token:
1. https://hub.docker.com/settings/security
2. New Access Token
3. Copia y pégalo

### 2. Push de Archivos de Workflow

Los archivos ya están en `.github/workflows/`:
- `docker-build-multiarch.yml` - Compila todo (amd64, arm64, arm/v7)
- `docker-build-arm64.yml` - Solo ARM64 (más rápido)

---

## 📝 Usos Diarios

### Uso 1: Cambio en el Modelo

```bash
# Cambiar el modelo seleccionado
vi Dockerfile  # O usar sed para cambiar MODEL_NAME

# Edita (si necesario)
vi src/main.py

# Commit y push
git add Dockerfile src/main.py
git commit -m "Change default model to yolov5m.pt"
git push origin main

# → GitHub Actions compila automáticamente
# → En RPi4: docker pull hn8888/yolo-light:arm64
```

**Nota**: Los usuarios pueden cambiar el modelo sin recompilar usando `-e MODEL_NAME=...`

### Uso 2: Cambio Simple en la Lógica

```bash
# Edita
vi src/main.py

# Commit y push
git add src/main.py
git commit -m "Fix bug in confidence filtering"
git push origin main

# → GitHub Actions compila automáticamente
# → En RPi4: docker pull hn8888/yolo-light:arm64
```

### Uso 2: Nueva Versión (Release)

```bash
# Versión final
git tag v1.1.0
git push origin v1.1.0

# → GitHub Actions compila multi-arquitectura
# → Tags creados: v1.1.0, 1.1, 1, latest
# → En RPi4: docker pull hn8888/yolo-light:v1.1.0
```

### Uso 3: Permitir que Usuarios Cambien Modelo

Los usuarios pueden cambiar el modelo sin recompilar:

```bash
# En RPi4
docker run -e MODEL_NAME=yolov5m.pt -d -p 8000:8000 hn8888/yolo-light:arm64
```

### Uso 4: Build Manual (GUI)

En GitHub:
1. Actions tab
2. Selecciona "Docker Build (Multi-arch)"
3. Click "Run workflow"
4. Espera ~20 minutos

---

## 📊 Tags Generados

Después de push a `main`:
```
hn8888/yolo-light:latest     ← Recomendado
hn8888/yolo-light:arm64      ← RPi4 específicamente
hn8888/yolo-light:amd64      ← Desarrollo
```

Después de tag `v1.1.0`:
```
hn8888/yolo-light:v1.1.0     ← Exacta
hn8888/yolo-light:1.1        ← Minor
hn8888/yolo-light:1          ← Major
hn8888/yolo-light:latest     ← Más reciente
```

---

## 🚀 En RPi4

```bash
# Después de push en GitHub (15-20 min después):

# Descargar
docker pull hn8888/yolo-light:arm64

# Ejecutar
docker run -d \
  -p 8000:8000 \
  --memory=1.5G \
  --name yolo-api \
  hn8888/yolo-light:arm64

# Verificar
curl http://localhost:8000/health
```

---

## 📈 Monitoreo

### Ver builds en progreso

GitHub → Actions → workflow name

Verás:
- Compilando amd64 (~5 min)
- Compilando arm64 (~8 min)
- Compilando arm/v7 (~5 min)
- Pusheando a Docker Hub (~2 min)

### Ver resultados

Docker Hub → https://hub.docker.com/r/hn8888/yolo-light/tags

Verás nuevos tags apareciendo en tiempo real.

---

## 🐛 Troubleshooting

**Problema**: "Cannot authenticate with Docker Hub"
```
Solución: Verifica que DOCKER_USERNAME y DOCKER_PASSWORD están correctos en GitHub Secrets
```

**Problema**: "Build fails"
```
Solución: Revisa el log en GitHub Actions para ver el error específico
```

**Problema**: "Build tarda demasiado"
```
Normal:
- Primera vez: 30-40 minutos (sin caché)
- Siguientes: 15-20 minutos (con caché)

Para acelerar: Usa docker-build-arm64.yml en lugar de multiarch
```

**Problema**: "No veo la imagen en Docker Hub"
```
Espera 5-10 minutos después de que GitHub Actions termine.
Refresca la página.
```

---

## 📋 Archivos Incluidos

```
.github/workflows/
├── docker-build-multiarch.yml   # Compila amd64, arm64, arm/v7
└── docker-build-arm64.yml       # Solo ARM64 (rápido)
```

---

## 🎓 Ejemplos Completos

### Ejemplo 1: Desarrollo Diario

```bash
# En tu PC
$ git clone https://github.com/hn8888/yolo-light.git
$ cd yolo-light

# Edita
$ vi src/main.py

# Test local
$ docker build -t local:test .
$ docker run -p 8000:8000 local:test

# Satisfecho? Push
$ git add src/main.py
$ git commit -m "Improve accuracy"
$ git push origin main

# → GitHub Actions compila automáticamente
# → 15-20 minutos después...

# En RPi4
$ docker pull hn8888/yolo-light:arm64
$ docker run -d -p 8000:8000 hn8888/yolo-light:arm64
```

### Ejemplo 2: Release de Versión

```bash
# En tu PC
$ git tag v1.5.0
$ git push origin main v1.5.0

# GitHub Actions dispara automáticamente
# Compila multi-arquitectura
# Tags creados:
#   hn8888/yolo-light:v1.5.0    (multi)
#   hn8888/yolo-light:1.5       (multi)
#   hn8888/yolo-light:1         (multi)
#   hn8888/yolo-light:latest    (multi)

# En RPi4
$ docker pull hn8888/yolo-light:v1.5.0
$ docker run -d -p 8000:8000 hn8888/yolo-light:v1.5.0
```

---

## ✅ Checklist

- [ ] GitHub Secrets configurados (DOCKER_USERNAME, DOCKER_PASSWORD)
- [ ] Archivos `.github/workflows/*.yml` en el repo
- [ ] Primer push/tag hecho
- [ ] GitHub Actions ejecutándose
- [ ] Imagen aparece en Docker Hub
- [ ] En RPi4: `docker pull hn8888/yolo-light:arm64` funciona

---

## 🔗 Links

- [Documentación Completa](GITHUB_ACTIONS_SETUP.md)
- [Docker Hub](https://hub.docker.com/r/hn8888/yolo-light)
- [GitHub Repo](https://github.com/hn8888/yolo-light)

---

**¡Ahora tu imagen ARM64 se genera automáticamente!** 🎉

No necesitas compilar en RPi4. Solo:

```bash
docker pull hn8888/yolo-light:arm64
docker run -d -p 8000:8000 hn8888/yolo-light:arm64
```
