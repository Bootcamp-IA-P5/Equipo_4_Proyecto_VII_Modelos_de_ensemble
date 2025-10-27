# Clasificación de Salud Fetal - Proyecto de Modelos de Ensemble

![Python](https://img.shields.io/badge/Python-3.11-blue.svg)
![FastAPI](https://img.shields.io/badge/FastAPI-0.111+-green.svg)
![Streamlit](https://img.shields.io/badge/Streamlit-Latest-red.svg)
![Docker](https://img.shields.io/badge/Docker-Compose-blue.svg)
![scikit-learn](https://img.shields.io/badge/scikit--learn-1.6.1-orange.svg)

Un proyecto de Machine Learning para clasificación de salud fetal utilizando modelos de ensemble, con optimización automática de hiperparámetros, despliegue containerizado e interfaces web interactivas.

**[📋 Gestión del Proyecto](https://github.com/orgs/Bootcamp-IA-P5/projects/5)** | **[📊 Dataset en Kaggle](https://www.kaggle.com/datasets/andrewmvd/fetal-health-classification/data)**

## 📋 Tabla de Contenidos

- [Descripción General](#descripción-general)
- [Características](#características)
- [Estructura del Proyecto](#estructura-del-proyecto)
- [Tecnologías](#tecnologías)
- [Inicio Rápido](#inicio-rápido)
- [Uso](#uso)
- [Entrenamiento del Modelo](#entrenamiento-del-modelo)
- [Documentación de la API](#documentación-de-la-api)
- [Desarrollo](#desarrollo)
- [Resultados](#resultados)
- [Equipo](#equipo)

## 🎯 Descripción General

Este proyecto implementa un sistema de clasificación multiclase para predecir el estado de salud fetal a partir de datos de cardiotocografía (CTG). El sistema utiliza modelos de Machine Learning de tipo ensemble con optimización automática de hiperparámetros para clasificar la salud fetal en tres categorías:

1. **Normal** (Clase 1)
2. **Sospechoso** (Clase 2)
3. **Patológico** (Clase 3)

El proyecto incluye:
- EDA automatizado (Análisis Exploratorio de Datos)
- Entrenamiento de modelos con optimización GridSearchCV
- API RESTful para predicciones
- Dashboard interactivo con Streamlit
- Despliegue completamente containerizado con Docker

## ✨ Características

### Machine Learning
- **Modelos Ensemble**: Random Forest, Gradient Boosting, AdaBoost, Bagging, XGBoost
- **Modelos Baseline**: Regresión Logística, Árbol de Decisión, KNN, Naive Bayes, SVM
- **Optimización Automática**: GridSearchCV para ajuste de hiperparámetros
- **Manejo de Desbalanceo**: Sobremuestreo con SMOTE
- **Validación Cruzada**: Validación estratificada K-Fold

### Aplicación
- **Backend FastAPI**: API RESTful con documentación automática
- **Frontend Streamlit**: Interfaz web interactiva para predicciones
- **Despliegue Docker**: Orquestación multi-contenedor
- **Persistencia de Modelos**: Modelos serializados con joblib
- **Registro Completo**: Métricas de entrenamiento e informes

## 📁 Estructura del Proyecto

```
Equipo_4_Proyecto_VII_Modelos_de_ensemble/
├── backend/                    # Servicio backend FastAPI
│   ├── app/
│   │   ├── main.py            # Endpoints de la API
│   │   ├── routes/            # Manejadores de rutas (estructura modular)
│   │   └── services/          # Servicios de lógica de negocio
│   ├── configure.py           # Configuración de rutas
│   ├── eda.py                 # Script de Análisis Exploratorio
│   ├── setup.py               # Configuración del paquete
│   ├── requirements.txt       # Dependencias Python
│   └── Dockerfile             # Definición del contenedor backend
├── frontend/                   # Servicio frontend Streamlit
│   ├── app.py                 # Dashboard Streamlit
│   ├── requirements.txt       # Dependencias frontend
│   └── Dockerfile             # Definición del contenedor frontend
├── src/                        # Código fuente
│   ├── train_model.py         # Pipeline de entrenamiento
│   └── load_data.py           # Utilidades de carga de datos
├── data/                       # Directorio de datos (volumen montado)
│   ├── raw/                   # Dataset original
│   └── processed/             # Datos limpios/procesados
├── models/                     # Modelos entrenados (volumen montado)
│   ├── fetal_health_model.pkl
│   └── scaler.pkl
├── reports/                    # Informes y métricas (volumen montado)
│   ├── metrics_*.json
│   ├── model_comparison_*.csv
│   └── best_model_report_*.txt
├── notebooks/                  # Notebooks Jupyter para análisis
├── docker-compose.yml          # Orquestación multi-contenedor
└── README.md                   # Este archivo
```

## 🛠 Tecnologías

### Backend
- **FastAPI** - Framework web moderno y rápido para construir APIs
- **Uvicorn** - Servidor ASGI para FastAPI
- **Pydantic** - Validación de datos usando anotaciones de tipo Python
- **scikit-learn** - Biblioteca de Machine Learning
- **XGBoost** - Framework de gradient boosting
- **imbalanced-learn** - SMOTE para manejo de desbalanceo de clases
- **SHAP** - Explicabilidad de modelos

### Frontend
- **Streamlit** - Framework para aplicaciones web de ciencia de datos
- **Pandas** - Manipulación de datos
- **Matplotlib/Seaborn** - Visualización de datos

### Infraestructura
- **Docker** - Containerización
- **Docker Compose** - Orquestación multi-contenedor
- **Python 3.11** - Lenguaje de programación

## 🚀 Inicio Rápido

### Requisitos Previos

- Docker Desktop instalado y en ejecución
- Git (para clonar el repositorio)
- Al menos 4GB de RAM disponible

### Instalación

1. **Clonar el repositorio**
   ```bash
   git clone https://github.com/Bootcamp-IA-P5/Equipo_4_Proyecto_VII_Modelos_de_ensemble.git
   cd Equipo_4_Proyecto_VII_Modelos_de_ensemble
   ```

2. **Asegurar que el dataset esté en su lugar**
   ```bash
   # El dataset debe estar en:
   data/raw/fetal_health.csv
   ```

3. **Entrenar el modelo (PRIMER USO)**
   
   ⚠️ **Importante**: La primera vez que clonas el proyecto, los modelos no están entrenados. Debes ejecutar el pipeline de entrenamiento antes de usar la aplicación:
   
   ```bash
   docker compose --profile training up train-model
   ```
   
   Este proceso puede tardar varios minutos y generará:
   - Modelos entrenados en `models/`
   - Reportes de métricas en `reports/`
   - Dataset procesado en `data/processed/`
   
   Para más detalles, consulta la sección [Entrenamiento del Modelo](#entrenamiento-del-modelo).

4. **Construir e iniciar los servicios**
   ```bash
   docker compose up --build
   ```

5. **Acceder a las aplicaciones**
   - **Frontend (Streamlit)**: http://localhost:8501
   - **Backend API**: http://localhost:8000
   - **Documentación API**: http://localhost:8000/docs

## 📊 Uso

### Usando la Interfaz Web (Streamlit)

1. Navegar a http://localhost:8501
2. Ingresar los parámetros CTG en los campos de entrada
3. Hacer clic en "Predict" para obtener el resultado de clasificación
4. Ver la confianza de la predicción y la etiqueta de clase

### Usando la API

#### Verificación de Estado
```bash
curl http://localhost:8000/health
```

#### Hacer una Predicción
```bash
curl -X POST http://localhost:8000/predict \
  -H "Content-Type: application/json" \
  -d '{
    "baseline_value": 120.0,
    "accelerations": 0.0,
    "fetal_movement": 0.0,
    "uterine_contractions": 0.0,
    "light_decelerations": 0.0,
    "severe_decelerations": 0.0,
    "prolongued_decelerations": 0.0,
    ...
  }'
```

#### Obtener Información del Dataset
```bash
curl http://localhost:8000/dataset/info
```

## 🎓 Entrenamiento del Modelo

### Ejecutar el Pipeline Completo de Entrenamiento

El pipeline de entrenamiento incluye EDA, preprocesamiento de datos, entrenamiento con optimización de hiperparámetros y evaluación:

```bash
docker compose --profile training up train-model
```

Esto realizará:
1. **Instalar dependencias** en modo editable
2. **Ejecutar script EDA** (`backend/eda.py`)
   - Analizar calidad de datos
   - Generar estadísticas
   - Guardar dataset limpio en `data/processed/`
3. **Entrenar modelos** (`src/train_model.py`)
   - Entrenar modelos baseline
   - Optimizar modelos ensemble con GridSearchCV
   - Evaluar y comparar todos los modelos
   - Guardar mejor modelo en `models/`
   - Generar informes en `reports/`

### Configuración de Entrenamiento

El pipeline de entrenamiento utiliza:
- **División Test**: 20% de los datos
- **Validación Cruzada**: 5-fold K-Fold Estratificado
- **SMOTE**: Aplicado para balancear clases de entrenamiento
- **Optimización**: GridSearchCV para modelos ensemble
- **Métricas**: Accuracy, Precision, Recall, F1-Score

### Modelos Entrenados

**Modelos Baseline** (hiperparámetros por defecto):
- Regresión Logística
- Árbol de Decisión
- K-Vecinos Más Cercanos
- Naive Bayes
- Máquina de Vectores de Soporte

**Modelos Ensemble** (con optimización GridSearchCV):
- Random Forest
- Gradient Boosting
- AdaBoost
- Clasificador Bagging
- Clasificador Voting (ensemble de ensembles)
- Clasificador Stacking

### Archivos de Salida

Después del entrenamiento, encontrarás:
- `models/fetal_health_model.pkl` - Mejor modelo entrenado
- `models/scaler.pkl` - StandardScaler ajustado
- `reports/metrics_*.json` - Todas las métricas de los modelos
- `reports/model_comparison_*.csv` - Tabla de comparación de modelos
- `reports/best_model_report_*.txt` - Informe detallado del mejor modelo
- `data/processed/fetal_health_clean.csv` - Dataset limpio
- `data/processed/eda_summary.txt` - Resumen del EDA

## 📖 Documentación de la API

### Documentación Interactiva

FastAPI proporciona documentación interactiva automática:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

### Endpoints

#### `GET /`
Endpoint raíz con información de la API.

#### `GET /health`
Endpoint de verificación de estado.

#### `POST /predict`
Realizar una predicción de salud fetal.

**Cuerpo de la Solicitud**: 21 características CTG incluyendo valor basal, aceleraciones, deceleraciones, variabilidad y características del histograma.

**Respuesta**:
```json
{
  "prediction": 1,
  "prediction_label": "Normal",
  "confidence": 0.95
}
```

#### `GET /dataset/info`
Obtener información sobre el dataset incluyendo total de muestras, características, distribución de clases y valores faltantes.

## 🔧 Desarrollo

### Ejecutar Servicios Individuales

**Solo Backend:**
```bash
docker compose up backend
```

**Solo Frontend:**
```bash
docker compose up frontend
```

**Solo Entrenamiento:**
```bash
docker compose --profile training up train-model
```

### Reconstruir Después de Cambios

```bash
docker compose up --build
```

### Ver Logs

```bash
# Todos los servicios
docker compose logs -f

# Servicio específico
docker compose logs -f backend
docker compose logs -f frontend
docker compose logs -f train-model
```

### Detener Servicios

```bash
# Detener y remover contenedores
docker compose down

# Detener, remover contenedores y volúmenes
docker compose down -v
```

### Desarrollo Local (Sin Docker)

1. **Instalar dependencias**
   ```bash
   pip install -r backend/requirements.txt
   pip install -r frontend/requirements.txt
   ```

2. **Ejecutar backend**
   ```bash
   cd backend
   uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
   ```

3. **Ejecutar frontend** (en otra terminal)
   ```bash
   streamlit run frontend/app.py --server.port 8501
   ```

4. **Ejecutar entrenamiento**
   ```bash
   python src/train_model.py
   ```

## 📈 Resultados

### Rendimiento del Modelo

El mejor modelo (típicamente AdaBoost o Random Forest) alcanza:
- **Accuracy Test**: ~95%
- **Score Validación Cruzada**: ~98%
- **Precisión**: ~95%
- **Recall**: ~95%
- **F1-Score**: ~95%

Los resultados detallados están disponibles en:
- `reports/model_comparison_*.csv` - Comparación de todos los modelos
- `reports/best_model_report_*.txt` - Métricas detalladas del mejor modelo

### Distribución de Clases

El dataset muestra desbalanceo de clases:
- **Normal (Clase 1)**: ~78% (1655 muestras)
- **Sospechoso (Clase 2)**: ~14% (295 muestras)
- **Patológico (Clase 3)**: ~8% (176 muestras)

SMOTE se aplica durante el entrenamiento para manejar este desbalanceo.

## 👥 Equipo

**Equipo 4** - Bootcamp IA P5

## 📝 Licencia

Este proyecto es parte de un bootcamp educativo y está destinado para fines de aprendizaje.

## 🙏 Agradecimientos

- Dataset: [Clasificación de Salud Fetal a partir de datos CTG](https://www.kaggle.com/datasets/andrewmvd/fetal-health-classification/data)
- Instructores y mentores del Bootcamp IA P5
- Comunidades de scikit-learn y FastAPI

---

**Nota**: Este es un proyecto de Machine Learning para fines educativos. Las decisiones médicas siempre deben ser tomadas por profesionales de la salud cualificados.

