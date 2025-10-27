# 🚀 Guía de Despliegue en Render.com

Esta guía te ayudará a desplegar el proyecto de Clasificación de Salud Fetal en Render.com.

## 📋 Requisitos Previos

1. ✅ Cuenta de GitHub (gratuita)
2. ✅ Cuenta de Render.com (gratuita) - [Registrarse aquí](https://render.com)
3. ✅ Modelos entrenados en la carpeta `models/`
4. ✅ Código subido a GitHub

## 🎯 Opción 1: Despliegue Automático con Blueprint (Recomendado)

### Paso 1: Preparar el Repositorio

```bash
# Asegúrate de que los modelos estén incluidos
git add models/fetal_health_model.pkl models/scaler.pkl
git add data/raw/fetal_health.csv
git add render.yaml
git commit -m "Add models and Render configuration"
git push origin main
```

### Paso 2: Crear Servicios en Render

1. Ve a [Render Dashboard](https://dashboard.render.com)
2. Haz clic en **"New +"** → **"Blueprint"**
3. Conecta tu repositorio de GitHub
4. Selecciona el repositorio `Equipo_4_Proyecto_VII_Modelos_de_ensemble`
5. Render detectará automáticamente el archivo `render.yaml`
6. Haz clic en **"Apply"**

Render creará automáticamente dos servicios:
- `fetal-health-backend` (FastAPI)
- `fetal-health-frontend` (Streamlit)

### Paso 3: Esperar el Despliegue

- El proceso puede tardar 5-10 minutos
- Verás los logs de construcción en tiempo real
- Una vez completado, obtendrás URLs como:
  - Backend: `https://fetal-health-backend.onrender.com`
  - Frontend: `https://fetal-health-frontend.onrender.com`

### Paso 4: Verificar el Despliegue

```bash
# Verificar backend
curl https://fetal-health-backend.onrender.com/health

# Acceder al frontend
# Abre en el navegador: https://fetal-health-frontend.onrender.com
```

## 🛠 Opción 2: Despliegue Manual (Servicio por Servicio)

### Backend

1. En Render Dashboard → **"New +"** → **"Web Service"**
2. Conecta tu repositorio
3. Configura:
   - **Name**: `fetal-health-backend`
   - **Environment**: `Docker`
   - **Dockerfile Path**: `./backend/Dockerfile`
   - **Docker Context**: `.` (raíz del proyecto)
   - **Plan**: `Free`
4. Variables de entorno:
   ```
   PORT=8000
   PYTHONUNBUFFERED=1
   ```
5. Haz clic en **"Create Web Service"**

### Frontend

1. En Render Dashboard → **"New +"** → **"Web Service"**
2. Conecta tu repositorio
3. Configura:
   - **Name**: `fetal-health-frontend`
   - **Environment**: `Docker`
   - **Dockerfile Path**: `./frontend/Dockerfile`
   - **Docker Context**: `.` (raíz del proyecto)
   - **Plan**: `Free`
4. Variables de entorno:
   ```
   PORT=8501
   BACKEND_URL=https://fetal-health-backend.onrender.com
   ```
   ⚠️ **Importante**: Reemplaza `fetal-health-backend` con el nombre exacto de tu servicio backend
5. Haz clic en **"Create Web Service"**

## ⚙️ Configuración Adicional

### Actualizar BACKEND_URL en Frontend

Después de crear el backend, necesitas actualizar la variable de entorno del frontend:

1. Ve a tu servicio `fetal-health-frontend` en Render
2. Click en **"Environment"**
3. Actualiza `BACKEND_URL` con la URL real del backend:
   ```
   https://tu-backend-real.onrender.com
   ```
4. Guarda los cambios (el servicio se reiniciará automáticamente)

### Health Checks

Render configurará automáticamente health checks para el backend usando `/health`.

## 🔄 Despliegue Continuo

Una vez configurado, cada vez que hagas `git push` a tu rama principal:
- Render detectará los cambios
- Reconstruirá y redespliegará automáticamente
- Los servicios se actualizarán sin intervención manual

```bash
# Workflow típico
git add .
git commit -m "Update model or code"
git push origin main
# Render desplegará automáticamente
```

## ⚠️ Limitaciones del Plan Gratuito

- **Suspensión por Inactividad**: Los servicios gratuitos se suspenden después de 15 minutos de inactividad
- **Inicio en Frío**: Primera petición después de suspensión puede tardar 30-60 segundos
- **750 horas/mes**: Tiempo de ejecución gratuito compartido entre todos tus servicios
- **Ancho de Banda**: 100 GB/mes

**Solución para demos**:
- Activar el servicio 2-3 minutos antes de presentar
- Hacer una petición de prueba para "despertar" los servicios

## 🐛 Solución de Problemas

### Error: "Model not loaded"

**Causa**: Los archivos de modelos no se incluyeron en el repositorio

**Solución**:
```bash
# Verifica que .gitignore NO excluya los modelos
git add -f models/*.pkl
git commit -m "Add trained models"
git push
```

### Error: "BACKEND_URL not reachable"

**Causa**: Frontend no puede conectarse al backend

**Solución**:
1. Verifica que la URL del backend sea correcta (con `https://`)
2. Asegúrate de que el backend esté corriendo (verde en Render)
3. Revisa los logs del frontend para detalles

### Error de Construcción de Docker

**Causa**: Timeouts al instalar dependencias pesadas

**Solución**: El `Dockerfile` actual ya tiene timeouts extendidos y cache optimizado. Si persiste:
```dockerfile
# En backend/Dockerfile, aumenta timeout
RUN pip install --no-cache-dir --default-timeout=2000 ...
```

### Logs de Depuración

Accede a logs en tiempo real:
1. Ve a tu servicio en Render Dashboard
2. Click en **"Logs"** en el menú lateral
3. Verás output en tiempo real de tu aplicación

## 📊 Monitoreo

### Métricas Disponibles

En Render Dashboard puedes ver:
- **CPU y Memoria**: Uso de recursos
- **Tiempo de Respuesta**: Latencia de peticiones
- **Solicitudes**: Número de peticiones por minuto
- **Uptime**: Tiempo activo del servicio

### Alertas

Render enviará notificaciones por email si:
- El servicio falla al iniciarse
- El health check falla repetidamente
- El servicio se suspende por límites

## 💰 Costos

### Plan Gratuito
- ✅ 2 servicios web gratuitos
- ✅ 750 horas/mes por servicio
- ✅ Ideal para proyectos de bootcamp y demos

### Si Necesitas Actualizar (Opcional)
- **Starter Plan**: $7/mes por servicio
  - Sin suspensión por inactividad
  - Métricas avanzadas
  - Más recursos

## 🔗 URLs del Proyecto Desplegado

Después del despliegue, actualiza el README.md con:

```markdown
## 🌐 Demo en Vivo

- **Frontend**: https://fetal-health-frontend.onrender.com
- **Backend API**: https://fetal-health-backend.onrender.com
- **API Docs**: https://fetal-health-backend.onrender.com/docs
```

## 📚 Recursos Adicionales

- [Documentación Oficial de Render](https://render.com/docs)
- [Render Blueprint Spec](https://render.com/docs/blueprint-spec)
- [Docker en Render](https://render.com/docs/docker)
- [Variables de Entorno](https://render.com/docs/environment-variables)

## ✅ Checklist de Despliegue

Antes de desplegar, verifica:

- [ ] Modelos entrenados en `models/` y commiteados
- [ ] Dataset en `data/raw/fetal_health.csv`
- [ ] `render.yaml` configurado correctamente
- [ ] Dockerfiles tienen CMD descomentado
- [ ] Código subido a GitHub
- [ ] Cuenta de Render.com creada
- [ ] Repositorio conectado a Render

Después del despliegue:
- [ ] Backend responde en `/health`
- [ ] Frontend carga correctamente
- [ ] Predicciones funcionan end-to-end
- [ ] URLs añadidas al README

---

¡Buena suerte con tu despliegue! 🚀
