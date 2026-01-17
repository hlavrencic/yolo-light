# 🚀 GitHub Actions - Compilación Automática para ARM64

## ¿Por qué GitHub Actions?

✅ Compila la imagen **ARM64** sin consumir recursos de RPi4  
✅ Compilación **automática** en cada push o release  
✅ Resultado **disponible en Docker Hub** inmediatamente  
✅ **Caché de compilación** para builds más rápidos  
✅ Multi-arquitectura: **amd64**, **arm64**, **arm/v7**  

---

## 🔧 Configuración

### 1. Agregar Secretos en GitHub

Ve a: **Settings → Secrets and variables → Actions**

Agrega estos secretos:

```
DOCKER_USERNAME = hn8888
DOCKER_PASSWORD = (tu token de Docker Hub)
```

Para obtener el token de Docker Hub:
1. Ve a https://hub.docker.com/settings/security
2. Click "New Access Token"
3. Copia el token
4. Pégalo en GitHub Secrets como `DOCKER_PASSWORD`

### 2. Workflows Incluidos

#### A. `docker-build-multiarch.yml` (Recomendado)
- Compila para **amd64**, **arm64** y **arm/v7**
- Se ejecuta automáticamente en cada push a `main`
- Se ejecuta en cada nuevo tag (`v1.0`, `v1.1`, etc)
- Genera tags automáticos

**Tags generados:**
- `latest` (desde main)
- `arm64` (desde main)
- `v1.0`, `v1.1`, etc (desde tags)

#### B. `docker-build-arm64.yml` (ARM64 solo)
- Compila SOLO para **ARM64**
- Más rápido que compilar todo
- Ideal para testing rápido
- Se puede ejecutar manualmente desde GitHub

**Tags generados:**
- `arm64`
- `rpi4`

---

## 📋 Cómo Usar

### Opción 1: Compilación Automática

Simplemente haz push a GitHub:

```bash
git add .
git commit -m "Update YOLO Light"
git push origin main
```

GitHub Actions compilará automáticamente para amd64, arm64 y arm/v7, y subirá a Docker Hub.

### Opción 2: Ejecución Manual

En GitHub, ve a:
**Actions → Docker Build (ARM64 Only) → Run workflow**

Esto compilará solo ARM64 en ~10-15 minutos.

### Opción 3: Crear Release

```bash
git tag v1.1.0
git push origin v1.1.0
```

Esto dispara la compilación automática y crea tags `v1.1.0` en Docker Hub.

---

## 📊 Workflow: `docker-build-multiarch.yml`

### Se ejecuta en:
- Push a `main` o `master`
- Cualquier nuevo tag (`v*`)
- Pull requests (solo test, sin push)

### Características:
- ✅ Compila 3 arquitecturas: amd64, arm64, arm/v7
- ✅ Usa GitHub Actions cache para builds más rápidos
- ✅ Genera tags automáticos
- ✅ Pushea a Docker Hub automáticamente

### Ejemplo de tags generados:

**Para push a main:**
```
hn8888/yolo-light:latest
hn8888/yolo-light:arm64
hn8888/yolo-light:main
```

**Para tag v1.0.0:**
```
hn8888/yolo-light:v1.0.0
hn8888/yolo-light:1.0
hn8888/yolo-light:1
hn8888/yolo-light:sha-abc123
```

---

## 📊 Workflow: `docker-build-arm64.yml`

### Se ejecuta en:
- Cambios en `src/`, `Dockerfile`, `requirements.txt`
- Ejecución manual desde GitHub Actions
- O con `workflow_dispatch`

### Características:
- ⚡ Compila solo ARM64 (más rápido)
- 📌 Tags: `arm64`, `rpi4`
- 🎯 Ideal para testing y desarrollo

---

## 🎯 Casos de Uso

### Desarrollo Rápido

```bash
# Edita el código
vi src/main.py

# Push
git add src/main.py
git commit -m "Fix bug"
git push origin main

# GitHub Actions compila automáticamente
# En 10-15 minutos, tienes imagen ARM64 en Docker Hub
# En RPi4: docker pull hn8888/yolo-light:arm64
```

### Release Oficial

```bash
# Versión final
git tag v1.1.0
git push origin v1.1.0

# GitHub Actions compila multi-arquitectura
# Tags creados:
#   hn8888/yolo-light:v1.1.0    (multi-arch)
#   hn8888/yolo-light:1.1       (multi-arch)
#   hn8888/yolo-light:1         (multi-arch)
```

### Compilación Manual Rápida (ARM64)

En GitHub:
1. Actions → Docker Build (ARM64 Only)
2. Run workflow
3. Espera ~10 minutos
4. Pull en RPi4: `docker pull hn8888/yolo-light:arm64`

---

## 📈 Monitoreo de Builds

### En GitHub:

1. Ve a **Actions** tab
2. Haz click en el workflow
3. Ve el progreso en tiempo real
4. Descarga logs si hay errores

### En Docker Hub:

1. Ve a https://hub.docker.com/r/hn8888/yolo-light/tags
2. Verás los nuevos tags con fecha/hora
3. Clickea en un tag para ver detalles

---

## 🐛 Troubleshooting

### Error: "Cannot log in to Docker Hub"

```bash
# Verifica que los secretos están configurados:
# GitHub → Settings → Secrets and variables → Actions
# Debe haber: DOCKER_USERNAME y DOCKER_PASSWORD
```

### Error: "Failed to build image"

```bash
# Revisa los logs en GitHub Actions
# Actions → workflow → job → paso específico
# Busca el error (ej: missing dependency)
```

### Build tarda demasiado

```bash
# Es normal la primera vez (~30-40 min)
# Las siguientes serán más rápidas gracias al caché (~10-15 min)
# Para builds más rápidos, usa docker-build-arm64.yml (solo ARM64)
```

### Tags no se están creando

```bash
# Verifica que estás pusheando correctamente:
git tag v1.0.0
git push origin v1.0.0

# No hagas:
git tag v1.0.0
git push origin main  # ← Esto no incluye el tag

# El tag debe aparecer en el push
```

---

## 🔐 Seguridad

✅ Usa **GitHub Secrets** para credenciales  
✅ No commits credenciales en git  
✅ El token de Docker Hub está encriptado  
✅ Los logs no muestran credenciales  

---

## 📝 Ejemplo Completo de Workflow

```bash
# 1. Haz un cambio
$ vi src/main.py

# 2. Commit y push
$ git add src/main.py
$ git commit -m "Improve detection accuracy"
$ git push origin main

# 3. GitHub Actions automáticamente:
#    - Compila amd64
#    - Compila arm64 (para RPi4)
#    - Compila arm/v7
#    - Pushea a Docker Hub con tags

# 4. En RPi4:
$ docker pull hn8888/yolo-light:arm64
$ docker run -d -p 8000:8000 hn8888/yolo-light:arm64
```

---

## 📚 Tags Disponibles Después de Compilar

### Después de push a main:
```
hn8888/yolo-light:latest     ← Multi-arch (recomendado)
hn8888/yolo-light:arm64      ← ARM64 solo (RPi4)
hn8888/yolo-light:amd64      ← AMD64 solo (desarrollo)
hn8888/yolo-light:main       ← Referencia a rama
```

### Después de crear tag v1.1.0:
```
hn8888/yolo-light:v1.1.0     ← Multi-arch
hn8888/yolo-light:1.1        ← Multi-arch (minor)
hn8888/yolo-light:1          ← Multi-arch (major)
hn8888/yolo-light:latest     ← Multi-arch (si es la release más reciente)
```

---

## 🎓 Cómo Construir Localmente (sin GitHub Actions)

Si necesitas compilar sin usar GitHub Actions:

```bash
# Compilar multi-arquitectura localmente
docker buildx build \
  --platform linux/amd64,linux/arm64,linux/arm/v7 \
  -t hn8888/yolo-light:multiarch \
  --push .

# O solo ARM64
docker buildx build \
  --platform linux/arm64 \
  -t hn8888/yolo-light:arm64 \
  --push .
```

---

## ✅ Checklist de Configuración

- [ ] Repositorio en GitHub
- [ ] Archivos `.github/workflows/*.yml` agregados
- [ ] Secretos configurados en GitHub (DOCKER_USERNAME, DOCKER_PASSWORD)
- [ ] Primer push/tag hecho
- [ ] GitHub Actions ejecutándose (ir a Actions tab)
- [ ] Imagen aparece en Docker Hub (~15-30 minutos después)
- [ ] En RPi4: `docker pull hn8888/yolo-light:arm64`

---

## 🚀 Flujo Recomendado

1. **Desarrollo**: Edita código en tu rama
2. **Testing Local**: Compila y prueba en tu máquina
3. **Push**: Haz push a GitHub
4. **Auto-build**: GitHub Actions compila automáticamente
5. **Deploy**: Pull en RPi4 desde Docker Hub

```bash
# Desarrollo
$ git checkout -b feature/new-feature
$ vi src/main.py
$ docker build -t test:latest .
$ docker run ... test:latest
$ # Testing

# Release
$ git checkout main
$ git merge feature/new-feature
$ git tag v1.1.0
$ git push origin main v1.1.0

# ← GitHub Actions compila automáticamente
# ← Docker Hub actualizado
# ← RPi4 puede hacer pull de la nueva imagen
```

---

## 📞 Soporte

Si GitHub Actions falla:

1. Ve a **Actions** en GitHub
2. Haz click en el workflow fallido
3. Revisa el log del paso específico que falló
4. Busca el error (ej: "no such file or directory")
5. Arregla localmente, commit, y push de nuevo

---

**¡Tu imagen ARM64 se compilará automáticamente en GitHub Actions!** 🎉

No necesitas ejecutar nada en RPi4. Solo:

```bash
docker pull hn8888/yolo-light:arm64
docker run -d -p 8000:8000 hn8888/yolo-light:arm64
```

¡Listo!
