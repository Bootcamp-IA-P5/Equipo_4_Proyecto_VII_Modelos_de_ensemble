# 🚀 Estructura del Backend - Guía de Desarrollo

## Descripción de Carpetas y Archivos

### 📂 **app/**
Contiene toda la lógica de la aplicación backend (API).

---

#### 📄 **`__init__.py`**
Archivo de inicialización del paquete Python. Puede estar vacío o contener configuraciones iniciales.

---

#### 📄 **`main.py`**
Punto de entrada principal de la aplicación.

**Funcionalidad:**
- Inicializa la aplicación FastAPI/Flask
- Configura CORS y middleware
- Registra las rutas (routes)
- Define configuración del servidor

**Ejemplo de contenido:**
```python
from fastapi import FastAPI
from app.api.routes import router

app = FastAPI(title="ML Prediction API")

# Registrar rutas
app.include_router(router)

# Health check
@app.get("/")
def root():
    return {"status": "API is running"}
```

---

#### 📂 **`api/`**
Contiene los endpoints de la API (rutas).

**Estructura:**
```
api/
├── __init__.py
├── routes.py           # Definición de endpoints
└── dependencies.py     # Dependencias comunes (opcional)
```

**`routes.py` - Funcionalidad:**
- Define los endpoints HTTP (GET, POST, etc.)
- Recibe las peticiones del cliente
- Llama a los servicios correspondientes
- Devuelve las respuestas

**Ejemplo:**
```python
from fastapi import APIRouter
from app.services.prediction_service import predict

router = APIRouter()

@router.post("/predict")
def make_prediction(data: dict):
    result = predict(data)
    return {"prediction": result}
```

---

#### 📂 **`models/`**
Define los esquemas de datos (Pydantic models) para validación de requests y responses.

**Funcionalidad:**
- Validación de datos de entrada
- Estructura de respuestas
- Documentación automática de la API

**Ejemplo:**
```python
from pydantic import BaseModel

class PredictionInput(BaseModel):
    feature1: float
    feature2: str
    feature3: int

class PredictionOutput(BaseModel):
    prediction: str
    probability: float
```

---

#### 📂 **`services/`**
Contiene la lógica de negocio de la aplicación.

**Estructura:**
```
services/
├── __init__.py
├── prediction_service.py    # Lógica de predicción
└── model_loader.py          # Carga del modelo ML
```

**`prediction_service.py` - Funcionalidad:**
- Carga el modelo de ML entrenado
- Preprocesa los datos de entrada
- Realiza predicciones
- Postprocesa resultados

**`model_loader.py` - Funcionalidad:**
- Carga el modelo desde disco (pickle, joblib)
- Carga encoders, scalers si son necesarios
- Gestiona la caché del modelo en memoria

**Ejemplo:**
```python
import joblib

class ModelLoader:
    def __init__(self):
        self.model = joblib.load('../models/final_model.pkl')
        self.scaler = joblib.load('../models/scaler.pkl')
    
    def predict(self, data):
        scaled_data = self.scaler.transform(data)
        return self.model.predict(scaled_data)
```

---

#### 📂 **`utils/`**
Funciones auxiliares y utilidades generales.

**Funcionalidad:**
- Funciones de preprocesamiento
- Validaciones personalizadas
- Helpers reutilizables
- Logging y manejo de errores

**Ejemplo:**
```python
def preprocess_input(data):
    """Limpia y transforma datos de entrada"""
    pass

def format_response(prediction, probability):
    """Formatea la respuesta de la API"""
    pass
```

---

### 📂 **tests/**
Tests unitarios y de integración del backend.

**Estructura:**
```
tests/
├── __init__.py
├── test_routes.py          # Tests de endpoints
├── test_services.py        # Tests de lógica de negocio
└── test_models.py          # Tests de schemas
```

**Funcionalidad:**
- Verificar que los endpoints funcionan correctamente
- Validar la lógica de predicción
- Asegurar que el modelo carga correctamente
- Tests de validación de datos

---

### 📄 **requirements.txt**
Lista de dependencias específicas del backend.

**Contenido típico:**
```
fastapi==0.104.1
uvicorn==0.24.0
pydantic==2.5.0
scikit-learn==1.3.2
pandas==2.1.3
joblib==1.3.2
```

---

### 📄 **README.md** (futuro)
Documentación general del backend:
- Instalación
- Cómo ejecutar el servidor
- Endpoints disponibles
- Ejemplos de uso

---

## 🔄 Flujo de una Petición

```
1. Cliente envía POST /predict
   ↓
2. api/routes.py recibe la petición
   ↓
3. models/ valida los datos de entrada
   ↓
4. services/prediction_service.py procesa
   ↓
5. services/model_loader.py carga modelo y predice
   ↓
6. utils/ formatea la respuesta
   ↓
7. api/routes.py devuelve respuesta al cliente
```

---

## 📦 Relación con el resto del proyecto

El backend **utiliza** el modelo entrenado que se encuentra en:
```
../models/final_model.pkl      # Modelo final entrenado
../models/scaler.pkl           # Scaler guardado
../models/encoder.pkl          # Encoder guardado
```

**Importante:** 
- El backend NO entrena modelos
- El backend SOLO sirve predicciones usando modelos ya entrenados
- Los modelos se desarrollan en `notebooks/` y se guardan en `models/`
- El backend los carga desde `models/` para hacer predicciones

---

## 🎯 Buenas Prácticas

1. **Separación de responsabilidades:**
   - `routes` → Solo manejo de HTTP
   - `services` → Lógica de negocio
   - `models` → Validación de datos
   - `utils` → Funciones auxiliares

2. **Código reutilizable:**
   - Funciones en `services` y `utils`
   - Evitar lógica en `routes`

3. **Validación:**
   - Usar Pydantic models para validar entrada/salida
   - Manejo de errores apropiado

4. **Testing:**
   - Tests para cada endpoint
   - Tests para servicios críticos

---

Esta estructura mantiene el backend organizado, escalable y fácil de mantener.
