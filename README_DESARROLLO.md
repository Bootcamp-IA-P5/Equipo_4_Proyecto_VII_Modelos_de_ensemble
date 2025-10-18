# 📁 Estructura del Proyecto

## Descripción de Carpetas y su Funcionalidad

### 📊 **data/**
Almacena todos los datos del proyecto, organizados por su estado de procesamiento.

- **`raw/`**: Contiene los datos originales sin modificar. Estos archivos **nunca deben ser editados** directamente para mantener la integridad de la fuente original.
  - Ejemplo: `dataset_original.csv`

- **`processed/`**: Almacena los datos después de aplicar limpieza, transformaciones y feature engineering. Estos datos están listos para ser utilizados en el entrenamiento de modelos.
  - Ejemplo: `dataset_clean.csv`, `X_train.pkl`, `y_test.pkl`

---

### 🤖 **models/**
Guarda los modelos de machine learning entrenados en formato serializado.

- Almacena modelos en formato `.pkl` (pickle) o `.joblib`
- Incluye modelos baseline, avanzados y ensemble
- También puede guardar encoders, scalers y otros transformadores
  - Ejemplo: `random_forest_model.pkl`, `xgboost_model.pkl`, `scaler.pkl`

---

### 📓 **notebooks/**
Contiene los Jupyter Notebooks que documentan todo el proceso de desarrollo del proyecto, desde la exploración inicial hasta la evaluación final.

- **`01_EDA.ipynb`**: Análisis Exploratorio de Datos
  - Exploración inicial del dataset
  - Análisis de distribuciones
  - Identificación de patrones y correlaciones
  - Detección de valores nulos y outliers
  - Visualizaciones iniciales

- **`02_preprocessing.ipynb`**: Preprocesamiento
  - Limpieza de datos
  - Tratamiento de valores nulos
  - Encoding de variables categóricas
  - Escalado de variables numéricas
  - Feature engineering
  - División train/test

- **`03_baseline.ipynb`**: Modelos Baseline
  - Implementación de modelos simples
  - Establecer métricas de referencia
  - Comparación de algoritmos básicos

- **`04_modeling.ipynb`**: Modelado Avanzado
  - Entrenamiento de modelos complejos
  - Optimización de hiperparámetros
  - Técnicas de ensemble
  - Validación cruzada

- **`05_evaluation.ipynb`**: Evaluación Final
  - Comparación de todos los modelos
  - Métricas de rendimiento
  - Matriz de confusión
  - Selección del modelo final
  - Análisis de resultados

---

### 🐍 **src/**
Contiene el código Python modular y reutilizable. Las funciones definidas aquí son importadas y utilizadas en los notebooks.

- **`data_processing.py`**: Funciones de procesamiento de datos
  - Carga de datos
  - Limpieza y transformación
  - Manejo de valores nulos
  - Encoding y escalado
  - Feature engineering

- **`models.py`**: Funciones relacionadas con modelos
  - Entrenamiento de modelos
  - Predicción
  - Guardado y carga de modelos
  - Pipeline de modelado

- **`evaluation.py`**: Funciones de evaluación
  - Cálculo de métricas (accuracy, F1, precision, recall)
  - Matrices de confusión
  - Curvas ROC
  - Reportes de clasificación

- **`visualization.py`**: Funciones de visualización
  - Gráficos personalizados
  - Visualización de resultados
  - Plots de distribuciones
  - Visualización de métricas

---

### 📄 **reports/**
Documentación de resultados, gráficos generados y conclusiones del proyecto.

- **`figures/`**: Almacena todas las visualizaciones y gráficos generados
- **`results.md`**: Resumen de resultados, métricas finales y conclusiones

---

### 📋 **Archivos en la raíz**

- **`README.md`**: Documentación principal del proyecto
- **`requirements.txt`**: Lista de dependencias necesarias para ejecutar el proyecto
- **`.gitignore`**: Archivos y carpetas que no deben ser versionados en Git

---

## 🔄 Flujo de Trabajo

```
1. data/raw/              → Datos originales
2. notebooks/01_EDA       → Exploración
3. notebooks/02_preprocessing → Limpieza (usa src/data_processing.py)
4. data/processed/        → Datos limpios
5. notebooks/03_baseline  → Modelos simples (usa src/models.py)
6. notebooks/04_modeling  → Modelos avanzados
7. models/                → Guardar modelos
8. notebooks/05_evaluation → Evaluación (usa src/evaluation.py)
9. reports/               → Documentar resultados
```

---

## 💡 Relación entre Notebooks y src/

Los notebooks utilizan las funciones definidas en `src/` para mantener el código limpio y reutilizable:

**Ejemplo:**
```python
# En notebooks/02_preprocessing.ipynb
from src.data_processing import handle_missing_values, encode_categorical

df = pd.read_csv('../data/raw/dataset.csv')
df_clean = handle_missing_values(df, strategy='median')
df_encoded = encode_categorical(df_clean, columns=['category'], method='onehot')
```

**Ventajas:**
- ✅ Notebooks más limpios y legibles
- ✅ Código reutilizable en múltiples notebooks
- ✅ Fácil mantenimiento (cambios en un solo lugar)
- ✅ Preparado para producción

---

Esta estructura mantiene el proyecto organizado, reproducible y facilita el trabajo colaborativo.
