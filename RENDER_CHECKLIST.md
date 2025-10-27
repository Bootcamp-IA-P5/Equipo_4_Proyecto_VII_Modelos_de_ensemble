# ✅ Checklist de Despliegue en Render

## ⚠️ Importante: Usando la Rama `feat/-Render_deployment`

Este proyecto está configurado para desplegarse desde la rama **`feat/-Render_deployment`**, no desde `main`. El archivo `render.yaml` ya especifica esta rama.

## Pasos a Seguir

### 1️⃣ Preparar el Repositorio

```bash
# Asegúrate de estar en la rama correcta
git checkout feat/-Render_deployment

# Verificar que los modelos estén entrenados
ls models/
# Deberías ver: fetal_health_model.pkl y scaler.pkl

# Añadir modelos al repositorio (ahora permitido por .gitignore)
git add models/fetal_health_model.pkl models/scaler.pkl

# Añadir archivos de configuración
git add render.yaml DEPLOYMENT.md .gitignore

# Añadir cambios en Dockerfiles
git add backend/Dockerfile frontend/Dockerfile

# Añadir cambios en README
git add README.md

# Commit
git commit -m "Prepare for Render deployment from feat/-Render_deployment"

# Push a GitHub (rama feat/-Render_deployment)
git push origin feat/-Render_deployment
```

### 2️⃣ Configurar Render

1. Ve a https://render.com
2. Crea una cuenta gratuita (puedes usar GitHub)
3. **Autoriza acceso a tu organización de GitHub**:
   - Durante la configuración, GitHub te pedirá permisos
   - Asegúrate de autorizar acceso a la organización **`Bootcamp-IA-P5`**
   - Si ya creaste la cuenta antes, ve a: [GitHub Settings → Applications → Render](https://github.com/settings/installations) y autoriza la organización
4. Click en **"New +"** → **"Blueprint"**
5. Selecciona tu organización en el dropdown (si no aparece, revisa paso 3)
6. Selecciona el repositorio: `Bootcamp-IA-P5/Equipo_4_Proyecto_VII_Modelos_de_ensemble`
7. **Importante**: Verifica que la rama sea **`feat/-Render_deployment`** (ya configurado en render.yaml)
8. Render detectará automáticamente `render.yaml`
9. Click en **"Apply"**

> 💡 **Nota**: El archivo `render.yaml` ya especifica `branch: feat/-Render_deployment`, así que Render usará automáticamente esta rama. No necesitas cambiar nada manualmente.

> ⚠️ **Si no ves tu organización**: Ve a [GitHub Settings → Applications](https://github.com/settings/installations), busca "Render", click en "Configure", y autoriza la organización `Bootcamp-IA-P5`.

### 3️⃣ Esperar el Despliegue

- ⏱️ Tiempo estimado: 5-10 minutos
- 📊 Puedes ver los logs de construcción en tiempo real
- ✅ Cuando ambos servicios muestren estado "Live" (verde), están listos

### 4️⃣ Obtener las URLs

En Render Dashboard, verás tus servicios:
- `fetal-health-backend` → Copia la URL (ej: `https://fetal-health-backend.onrender.com`)
- `fetal-health-frontend` → Copia la URL (ej: `https://fetal-health-frontend.onrender.com`)

### 5️⃣ Verificar el Despliegue

```bash
# Verificar backend (desde terminal local)
curl https://fetal-health-backend-jnsr.onrender.com/health

# Debería responder:
# {"status":"healthy","model_loaded":true}

# Verificar documentación API
# Abre en navegador: https://fetal-health-backend-jnsr.onrender.com/docs

# Verificar frontend
# Abre en navegador: https://fetal-health-frontend.onrender.com
```

#### ⚠️ Si el Frontend Muestra "Backend connection error: Invalid URL"

Esto significa que `BACKEND_URL` no tiene el esquema `https://`. Soluciones:

**Opción A: Actualizar Variable de Entorno en Render (Recomendado)**
1. Ve a tu servicio `fetal-health-frontend` en Render Dashboard
2. Click en **"Environment"** en el menú lateral
3. Encuentra la variable `BACKEND_URL`
4. Asegúrate de que tenga el valor completo con `https://`:
   ```
   https://fetal-health-backend-jnsr.onrender.com
   ```
   (Usa tu URL real del backend, visible en el dashboard del servicio backend)
5. Click en **"Save Changes"**
6. Espera a que el servicio se reinicie (~30-60 segundos)

**Opción B: Hacer Push con el Código Actualizado**
El frontend ahora detecta automáticamente URLs de Render y añade `https://`, pero necesitas hacer push:
```bash
git add frontend/app.py render.yaml
git commit -m "Fix BACKEND_URL scheme handling"
git push origin feat/-Render_deployment
# Espera a que Render redesplegue (~5-10 min)
```

### 6️⃣ Probar una Predicción

En el frontend de Streamlit:
1. Ingresa valores de prueba
2. Click en "Predict"
3. Verifica que obtienes una predicción con confianza

### 7️⃣ Actualizar README (Opcional)

Añade las URLs al README:

```markdown
## 🌐 Demo en Vivo

- **🎨 Frontend (Streamlit)**: https://TU-FRONTEND-URL.onrender.com
- **🔌 Backend API**: https://TU-BACKEND-URL.onrender.com
- **📚 Documentación API**: https://TU-BACKEND-URL.onrender.com/docs
```

```bash
git add README.md
git commit -m "Add live demo URLs"
git push origin feat/-Render_deployment
```

## 🔄 Actualizaciones Futuras

Cada vez que hagas cambios y los subas a `feat/-Render_deployment`, Render se desplegará automáticamente:

```bash
# Hacer cambios en tu código
git add .
git commit -m "Update feature X"
git push origin feat/-Render_deployment
# ✅ Render detecta el push y redespliega automáticamente
```

### Cuando Esté Listo para Producción

Si quieres mover los cambios a `main` después de probarlos:

```bash
git checkout main
git merge feat/-Render_deployment
git push origin main

# Opcionalmente, cambia Render para usar main en el futuro
```

## ⚠️ Troubleshooting Rápido

### Problema: "No veo mi organización (Bootcamp-IA-P5) en Render"
**Solución**: Autoriza Render a acceder a la organización:
```
1. Ve a: https://github.com/settings/installations
2. Busca "Render" → Click en "Configure"
3. En "Organization access", autoriza "Bootcamp-IA-P5"
4. Si no eres admin, solicita aprobación al admin de la organización
5. Vuelve a Render y refresca
```

### Problema: "Repository not found" o "Access denied"
**Solución**: 
- Verifica que tienes permisos de escritura en el repositorio
- Contacta al admin de `Bootcamp-IA-P5` para permisos
- El admin debe aprobar la instalación de Render en la organización

### Problema: "Model not loaded"
**Solución**: Verifica que los modelos se subieron a GitHub en la rama correcta:
```bash
git checkout feat/-Render_deployment
git ls-files models/
# Deberías ver: fetal_health_model.pkl y scaler.pkl

# Si no están, añádelos:
git add -f models/fetal_health_model.pkl models/scaler.pkl
git commit -m "Add trained models"
git push origin feat/-Render_deployment
```

### Problema: Frontend no conecta con Backend
**Solución**: Actualiza la variable de entorno en Render:
1. Ve al servicio `fetal-health-frontend`
2. Click en "Environment"
3. Actualiza `BACKEND_URL` con la URL real del backend
4. Guarda (se reiniciará automáticamente)

### Problema: Servicio suspendido (503)
**Solución**: Los servicios gratuitos se suspenden tras 15 min de inactividad
- Simplemente visita la URL
- Espera 30-60 segundos
- El servicio se reactivará automáticamente

### Problema: Build timeout
**Solución**: El Dockerfile ya tiene timeouts extendidos, pero si persiste:
1. Ve a tu servicio en Render
2. Click en "Manual Deploy" → "Clear build cache & deploy"

## 📞 Soporte

Si tienes problemas:
1. Revisa los logs en Render Dashboard → Tu servicio → "Logs"
2. Consulta [DEPLOYMENT.md](DEPLOYMENT.md) para guía detallada
3. Documentación oficial: https://render.com/docs

## 🎉 ¡Éxito!

Una vez desplegado, puedes:
- ✅ Compartir las URLs con tu equipo
- ✅ Usarlo en presentaciones del bootcamp
- ✅ Incluirlo en tu portafolio
- ✅ Cada push a GitHub se desplegará automáticamente

---

**Tiempo total estimado**: 15-20 minutos
