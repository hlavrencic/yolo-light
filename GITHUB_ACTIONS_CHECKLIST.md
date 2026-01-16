# ✅ GitHub Actions Setup - Checklist Final

## 📋 Configuración (Una sola vez)

- [ ] Tienes cuenta en GitHub con el repo `yolo-light`
- [ ] Tienes cuenta en Docker Hub con usuario `hn8888`
- [ ] Accedes a https://hub.docker.com/settings/security
- [ ] Creas "New Access Token" y copias el token
- [ ] Vas a GitHub repo → Settings → Secrets and variables → Actions
- [ ] Creas secret `DOCKER_USERNAME` = `hn8888`
- [ ] Creas secret `DOCKER_PASSWORD` = (tu token)
- [ ] Verificas que `.github/workflows/docker-build-multiarch.yml` existe
- [ ] Verificas que `.github/workflows/docker-build-arm64.yml` existe

## 📤 Primer Push

- [ ] `git add .`
- [ ] `git commit -m "Add GitHub Actions"`
- [ ] `git push origin main`

## 🚀 Monitoreo

- [ ] Vas a GitHub Actions tab
- [ ] Ves el workflow ejecutándose
- [ ] Esperas 15-20 minutos a que termine
- [ ] Ves checkmark verde ✅ en todas las tareas

## 📦 Verificación en Docker Hub

- [ ] Vas a https://hub.docker.com/r/hn8888/yolo-light/tags
- [ ] Ves nuevo tag `arm64` aparecer
- [ ] Ves nuevo tag `latest` actualizado
- [ ] Clickeas en `arm64` para ver detalles

## 📥 En RPi4

- [ ] Descargas: `docker pull hn8888/yolo-light:arm64`
- [ ] Ejecutas: `docker run -d -p 8000:8000 --memory=1.5G --name yolo-api hn8888/yolo-light:arm64`
- [ ] Verificas: `curl http://localhost:8000/health`
- [ ] Ves respuesta JSON válida ✅

## 🎉 Finalización

- [ ] API está corriendo en RPi4
- [ ] Health check responde correctamente
- [ ] Puedes detectar objetos: `curl -X POST -F "file=@foto.jpg" http://localhost:8000/detect`
- [ ] Documentación actualizada
- [ ] GitHub repo con workflows
- [ ] Docker Hub imagen lista

---

## 🔄 Próximos Cambios (Ciclo Repetitivo)

Para cada cambio futuro:

```bash
# 1. Edita código
vi src/main.py

# 2. Test local
docker build -t local:test .
docker run -p 8000:8000 local:test

# 3. Push (activa GitHub Actions automáticamente)
git add src/main.py
git commit -m "Mejora en detección"
git push origin main

# 4. Monitorea en GitHub Actions (15-20 min)
# Go to: GitHub → Actions → ver el workflow

# 5. En RPi4 (después de compilar)
docker pull hn8888/yolo-light:arm64
docker stop yolo-api
docker rm yolo-api
docker run -d -p 8000:8000 hn8888/yolo-light:arm64

# 6. Verifica
curl http://localhost:8000/health
```

---

## 📝 Notas Importantes

- ✅ Los workflows están en `.github/workflows/`
- ✅ Se ejecutan automáticamente con cada `git push` a `main`
- ✅ Puedes monitorizarlos en GitHub → Actions
- ✅ Los secretos NO aparecen en los logs
- ✅ La compilación es completamente automática
- ✅ No necesitas hacer nada después del push

---

## 🆘 Si Algo Falla

**Workflow no se ejecuta:**
- Verifica que los archivos `.yml` están en `.github/workflows/`
- Verifica que los secrets están configurados
- Intenta hacer push de nuevo

**Error de autenticación Docker Hub:**
- Verifica que `DOCKER_USERNAME` = `hn8888` (sin espacios)
- Verifica que `DOCKER_PASSWORD` = token válido (generado hace poco)
- Prueba crear un nuevo token

**Build falla:**
- Ve a GitHub Actions → workflow → job que falló
- Lee los logs para ver el error específico
- Arregla el código localmente
- Commit y push de nuevo

**Imagen no aparece en Docker Hub:**
- Espera 5-10 minutos más
- Refresca la página
- Verifica que el workflow en GitHub terminó exitosamente (checkmark verde)

---

## 🎯 Workflow Esperado

```
Day 1: Setup
  ├─ Creas cuenta GitHub + Docker Hub
  ├─ Configuras secrets (5 min)
  ├─ Haces push (activa GitHub Actions)
  ├─ Esperas compilación (15-20 min)
  ├─ Pull en RPi4
  └─ API corriendo ✅

Day 2+: Cambios Normales
  ├─ Edita código
  ├─ git push (automático)
  ├─ Espera 15-20 min
  ├─ Pull nuevo tag
  └─ API actualizada ✅
```

---

## 📞 Preguntas Frecuentes

**P: ¿Qué pasa si no configuro los secrets?**  
A: El workflow falla al intentar pushear a Docker Hub. Ve a Settings y añade los secrets.

**P: ¿Puedo pausar GitHub Actions?**  
A: Sí, pero es recomendable mantenerlo activo. Solo desactívalo si no planeas hacer cambios.

**P: ¿Se cobran los GitHub Actions?**  
A: No, la compilación para públicos es gratis. GitHub te da minutos gratis cada mes.

**P: ¿Qué pasa con las builds antiguas?**  
A: Permanecen en Docker Hub. Puedes eliminarlas manualmente si quieres limpiar.

**P: ¿Cómo creo un release?**  
A: `git tag v1.0.0` y `git push origin v1.0.0`. Genera tags: v1.0.0, 1.0, 1, latest

---

## ✅ Status: COMPLETADO

Todo está configurado. Solo necesitas:

1. Agregar secrets en GitHub (5 min, una sola vez)
2. Hacer push cada vez que quieras actualizar
3. Esperar 15-20 minutos
4. Pull en RPi4

¡Eso es! 🚀

---

*Última actualización: Enero 16, 2026*
