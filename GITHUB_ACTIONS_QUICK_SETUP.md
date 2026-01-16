# ✅ GitHub Actions - Setup Completo (5 minutos)

## 📋 Resumen

Tu YOLO Light API ahora usa **GitHub Actions** para compilar automáticamente la imagen **ARM64** para RPi4.

**Antes**: Compilar en RPi4 (~45 min, consume recursos)  
**Ahora**: Compilar en GitHub (~15-20 min, sin tocar RPi4)

---

## ⚡ Setup (Una sola vez)

### Paso 1: Configurar Docker Hub Token

1. Ve a https://hub.docker.com/settings/security
2. Click **New Access Token**
3. Nombre: `github-actions`
4. Copia el token (ej: `dckr_pat_ABC123...`)

### Paso 2: Agregar Secretos en GitHub

En tu repo:
1. Settings → Secrets and variables → Actions
2. New repository secret

Crea dos:

```
Secret 1:
  Name: DOCKER_USERNAME
  Value: hn8888

Secret 2:
  Name: DOCKER_PASSWORD
  Value: (pega el token del Paso 1)
```

### Paso 3: Verificar Workflows

Los archivos ya están en tu repo:
```
.github/workflows/
├── docker-build-multiarch.yml
└── docker-build-arm64.yml
```

¡Listo! 🎉

---

## 🚀 Usar

### Método 1: Push Automático

```bash
# Haz un cambio cualquiera
git add .
git commit -m "Update"
git push origin main

# → GitHub Actions compila automáticamente
# → 15-20 minutos después, imagen lista en Docker Hub
```

### Método 2: Manual Trigger

En GitHub:
1. Actions tab
2. "Docker Build (ARM64 Only)"
3. "Run workflow"
4. Espera 15-20 minutos

### Método 3: Release (Tag)

```bash
git tag v1.1.0
git push origin v1.1.0

# → Compila multi-arquitectura
# → Tags: v1.1.0, 1.1, 1, latest
```

---

## 📥 En RPi4

Después de compilar (~15-20 min):

```bash
# Descargar imagen ARM64
docker pull hn8888/yolo-light:arm64

# Ejecutar
docker run -d -p 8000:8000 --memory=1.5G --name yolo-api hn8888/yolo-light:arm64

# Verificar
curl http://localhost:8000/health
```

---

## 📊 Ver Progreso

### En GitHub
Actions tab → Workflow en progreso

Muestra:
- ✓ Compilando amd64
- ✓ Compilando arm64 ← Lo que necesitas para RPi4
- ✓ Compilando arm/v7
- ✓ Pusheando a Docker Hub

### En Docker Hub
https://hub.docker.com/r/hn8888/yolo-light/tags

Verás nuevos tags apareciendo.

---

## 🎯 Tags Disponibles

Después de compilar:

```
hn8888/yolo-light:arm64    ← Úsalo en RPi4
hn8888/yolo-light:latest   ← Multi-arquitectura
hn8888/yolo-light:main     ← Desde rama main
```

---

## ✨ Ventajas

✅ No consumes recursos de RPi4 compilando  
✅ Compilación más rápida (GitHub tiene servidores potentes)  
✅ Multi-arquitectura automática  
✅ Caché inteligente (siguientes builds más rápidos)  
✅ Completamente automático (con cada push)  

---

## 📝 Documentación

- [Guía Completa](GITHUB_ACTIONS_SETUP.md) - Detalles técnicos
- [Quick Start](QUICK_START_GITHUB_ACTIONS.md) - Ejemplos prácticos
- [Docker Hub](DOCKER_HUB_INSTRUCTIONS.md) - Cómo usar en RPi4

---

## ❓ Preguntas Frecuentes

**P: ¿Cuánto tarda compilar?**  
A: 15-20 minutos en GitHub Actions (primera vez 30-40 con caché frío)

**P: ¿Necesito hacer algo en RPi4?**  
A: No. Solo `docker pull hn8888/yolo-light:arm64`

**P: ¿Puedo compilar solo ARM64?**  
A: Sí, usa el workflow `docker-build-arm64.yml` (más rápido)

**P: ¿Qué pasa si cometo un error?**  
A: GitHub Actions lo detiene. Arregla, commit, push de nuevo.

**P: ¿Cómo veo los errores?**  
A: Actions tab → workflow → job → revisa los logs

---

## 🎉 Listo

Ahora cada push a GitHub:
1. ✅ Compila automáticamente
2. ✅ Genera imagen ARM64
3. ✅ Pushea a Docker Hub
4. ✅ En RPi4: `docker pull hn8888/yolo-light:arm64`

**¡Sin tocar RPi4!** 🚀

---

*Documentación actualizada: Enero 16, 2026*
