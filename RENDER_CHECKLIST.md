# ✅ Checklist de Despliegue en Render

## Pasos a Seguir

### 1️⃣ Preparar el Repositorio

```bash
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
git commit -m "Prepare for Render deployment"

# Push a GitHub
git push origin main
```

### 2️⃣ Configurar Render

1. Ve a https://render.com
2. Crea una cuenta gratuita (puedes usar GitHub)
3. Click en **"New +"** → **"Blueprint"**
4. Autoriza el acceso a GitHub
5. Selecciona el repositorio: `Equipo_4_Proyecto_VII_Modelos_de_ensemble`
6. Render detectará automáticamente `render.yaml`
7. Click en **"Apply"**

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
curl https://TU-BACKEND-URL.onrender.com/health

# Debería responder:
# {"status":"healthy"}

# Verificar documentación API
# Abre en navegador: https://TU-BACKEND-URL.onrender.com/docs

# Verificar frontend
# Abre en navegador: https://TU-FRONTEND-URL.onrender.com
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
git push
```

## ⚠️ Troubleshooting Rápido

### Problema: "Model not loaded"
**Solución**: Verifica que los modelos se subieron a GitHub:
```bash
git ls-files models/
# Deberías ver: fetal_health_model.pkl y scaler.pkl
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
