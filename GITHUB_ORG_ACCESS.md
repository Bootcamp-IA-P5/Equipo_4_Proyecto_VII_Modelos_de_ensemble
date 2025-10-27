# 🔐 Guía Rápida: Autorizar Organización de GitHub en Render

## ¿Por qué necesito esto?

Tu proyecto está en una **organización de GitHub** (`Bootcamp-IA-P5`), no en tu perfil personal. Render necesita permiso explícito para acceder a repositorios de organizaciones.

## 📝 Pasos para Autorizar

### Opción A: Durante la Primera Configuración de Render

1. **Crea cuenta en Render** usando GitHub
2. Cuando Render pida autorización, verás una pantalla de GitHub
3. **Importante**: Busca la sección **"Organization access"**
4. Junto a `Bootcamp-IA-P5`, verás un botón:
   - **"Grant"** (si eres admin) → Click aquí
   - **"Request"** (si no eres admin) → Click y espera aprobación
5. Continúa con la configuración

### Opción B: Si Ya Creaste tu Cuenta en Render

1. Ve a: **https://github.com/settings/installations**
2. Busca **"Render"** en la lista de "Installed GitHub Apps"
3. Click en **"Configure"** junto a Render
4. Verás dos secciones:

   **Repository access:**
   - Selecciona "Only select repositories"
   - Busca y selecciona: `Bootcamp-IA-P5/Equipo_4_Proyecto_VII_Modelos_de_ensemble`
   - O selecciona "All repositories" si prefieres

   **Organization access:**
   - Busca `Bootcamp-IA-P5` en la lista
   - Click en **"Grant"** (si eres admin) o **"Request"** (si no lo eres)

5. **Guarda los cambios**
6. Vuelve a Render y refresca la página

### Opción C: Si NO Eres Administrador de la Organización

1. Sigue los pasos de **Opción B**
2. Click en **"Request"** junto a `Bootcamp-IA-P5`
3. **Contacta al administrador** de la organización (puede ser tu instructor)
4. El admin recibirá una notificación en GitHub
5. Una vez aprobado, podrás continuar con el despliegue

## 🔍 Verificar que Funcionó

Después de autorizar:

1. Ve a **Render Dashboard** → **"New +"** → **"Blueprint"**
2. En el selector de repositorios, deberías ver un dropdown con organizaciones
3. Selecciona **"Bootcamp-IA-P5"**
4. Deberías ver el repositorio: `Equipo_4_Proyecto_VII_Modelos_de_ensemble`

## ⚠️ Problemas Comunes

### "No veo mi organización en el dropdown"
- Espera 1-2 minutos y refresca Render
- Verifica que el admin haya aprobado la solicitud
- Cierra sesión en Render y vuelve a entrar

### "Access denied al seleccionar el repositorio"
- Verifica que tengas permisos de **write** o **admin** en el repositorio
- Pide al admin de la organización que te otorgue permisos

### "Request pending"
- La solicitud está pendiente de aprobación del admin
- Contacta al admin de `Bootcamp-IA-P5`
- Proporciona el enlace: https://github.com/organizations/Bootcamp-IA-P5/settings/installations

## 👥 Para Administradores de la Organización

Si recibes una solicitud de acceso de Render:

1. Ve a: **https://github.com/organizations/Bootcamp-IA-P5/settings/installations**
2. Busca las solicitudes pendientes
3. Revisa la solicitud de tu compañero
4. Click en **"Review request"**
5. Autoriza el acceso
6. Notifica a tu compañero que ya puede continuar

## 🚀 Siguiente Paso

Una vez autorizado el acceso, continúa con **RENDER_CHECKLIST.md** desde el Paso 2.

---

**Tiempo estimado**: 2-5 minutos (o espera de aprobación si no eres admin)
