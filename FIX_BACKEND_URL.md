# 🔧 Fix: Backend Connection Error en Render

## 🐛 Error

```
Backend connection error: Invalid URL 'fetal-health-backend-jnsr/health': No scheme supplied. 
Perhaps you meant https://fetal-health-backend-jnsr/health?
```

## ❓ Causa

La variable de entorno `BACKEND_URL` en el frontend solo contiene el hostname (`fetal-health-backend-jnsr`) sin el esquema `https://`.

Esto ocurre cuando `render.yaml` usa `property: host` en lugar de especificar la URL completa.

## ✅ Solución Rápida (5 minutos)

### Opción A: Actualizar en Render Dashboard (MÁS RÁPIDO)

1. **Ve a tu servicio frontend en Render**:
   - https://dashboard.render.com
   - Click en tu servicio `fetal-health-frontend`

2. **Actualiza la variable de entorno**:
   - Click en **"Environment"** en el menú lateral izquierdo
   - Busca la variable `BACKEND_URL`
   - Cambia el valor de:
     ```
     fetal-health-backend-jnsr
     ```
     a:
     ```
     https://fetal-health-backend-jnsr.onrender.com
     ```
   - Click en **"Save Changes"**

3. **Espera el reinicio**:
   - Render reiniciará automáticamente el servicio
   - Espera 30-60 segundos
   - Refresca tu aplicación en el navegador

4. **Verifica**:
   - Ve a tu frontend: https://fetal-health-frontend.onrender.com
   - El mensaje de "Backend connection error" debería desaparecer
   - Deberías ver "✅ Backend connected | Model loaded"

### Opción B: Fix en el Código + Push (Más permanente)

Ya he actualizado los archivos necesarios. Solo necesitas hacer push:

```bash
# 1. Verificar los cambios
git status

# 2. Añadir archivos actualizados
git add frontend/app.py render.yaml

# 3. Commit
git commit -m "Fix BACKEND_URL scheme handling for Render deployment"

# 4. Push
git push origin feat/-Render_deployment

# 5. Esperar redespliegue en Render (5-10 minutos)
```

Los cambios incluyen:
- ✅ `frontend/app.py`: Detecta automáticamente URLs sin esquema y añade `https://`
- ✅ `render.yaml`: URL explícita del backend

## 🔍 Verificar que Funcionó

### 1. Backend Health Check

```bash
curl https://fetal-health-backend-jnsr.onrender.com/health
```

Debería responder:
```json
{
  "status": "healthy",
  "model_loaded": true
}
```

### 2. Frontend Status

Abre: https://fetal-health-frontend.onrender.com

Deberías ver:
```
🔌 System Status
✅ Backend connected | Model loaded
```

### 3. Hacer una Predicción

1. Ingresa valores en el formulario
2. Click en "Predict"
3. Deberías recibir una predicción con confianza

## 📋 Prevenir este Error en el Futuro

### En `render.yaml`, usa siempre URL completa:

❌ **EVITA** (causa el error):
```yaml
envVars:
  - key: BACKEND_URL
    fromService:
      type: web
      name: fetal-health-backend
      property: host  # ← Esto solo da hostname
```

✅ **USA** (correcto):
```yaml
envVars:
  - key: BACKEND_URL
    value: https://fetal-health-backend-jnsr.onrender.com
```

### En el código frontend, valida siempre URLs:

```python
BACKEND_URL = os.getenv("BACKEND_URL", "http://backend:8000")

# Asegurar que tiene esquema
if BACKEND_URL and not BACKEND_URL.startswith(('http://', 'https://')):
    if 'onrender.com' in BACKEND_URL:
        BACKEND_URL = f"https://{BACKEND_URL}"
    else:
        BACKEND_URL = f"http://{BACKEND_URL}"
```

## ❓ Troubleshooting

### "Sigo viendo el error después de cambiar la variable"

1. **Verifica que guardaste los cambios** en Render
2. **Espera al menos 60 segundos** para el reinicio
3. **Limpia caché del navegador**: Ctrl + Shift + R (Windows) o Cmd + Shift + R (Mac)
4. **Verifica los logs** del frontend en Render Dashboard → Logs

### "El backend responde 503"

El servicio gratuito se suspende tras 15 minutos de inactividad:
1. Visita la URL del backend directamente
2. Espera 30-60 segundos
3. Refresca el frontend

### "Cambié render.yaml pero sigue igual"

Si editaste `render.yaml`, necesitas:
1. Hacer **push** a GitHub
2. En Render → Settings → **Manual Deploy** → "Deploy latest commit"
3. O esperar a que Render detecte el cambio automáticamente

## 🎉 Resultado Esperado

Después de aplicar el fix, tu frontend debería mostrar:

```
🏥 Fetal Health Classification System

🔌 System Status
✅ Backend connected | Model loaded

📊 System Information
Total Samples: 2126
Features: 21
Classes: 3 (Normal, Suspect, Pathological)
```

---

**Tiempo de solución**: 2-5 minutos con Opción A, 10-15 minutos con Opción B
