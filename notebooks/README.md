# 📓 Notebooks - Workflow de Machine Learning

Este directorio contiene los notebooks del proyecto de clasificación de salud fetal, organizados en un flujo de trabajo profesional y modular.

## 📋 Estructura de Notebooks

### 1️⃣ **EDA.ipynb** - Exploratory Data Analysis
**Propósito:** Análisis exploratorio inicial del dataset

**Contenido:**
- Carga y overview del dataset
- Análisis de calidad de datos (valores nulos, duplicados)
- Análisis de la variable objetivo (fetal_health)
- Distribución de clases y balance
- Análisis univariado y bivariado
- Limpieza y preparación de datos

**Output:**
- `data/processed/fetal_health_clean.csv` - Dataset limpio

**Ejecución:**
```bash
# Ejecutar todas las celdas en orden
```

---

### 2️⃣ **baseline.ipynb** - Baseline Models
**Propósito:** Establecer performance de referencia con modelos simples

**Contenido:**
- Carga de dataset limpio
- Train/Test split (80/20, random_state=25)
- Entrenamiento de modelos baseline:
  - Logistic Regression
  - Decision Tree
  - KNN
- Evaluación con múltiples métricas
- Identificación del mejor baseline
- Matriz de confusión

**Output:**
- `data/processed/baseline_results.csv` - Resultados de baseline models

**Ejecución:**
```bash
# Ejecutar DESPUÉS de EDA.ipynb
# Asegúrate de descomentar la última celda para guardar resultados
```

---

### 3️⃣ **ensemble_models.ipynb** - Ensemble Models
**Propósito:** Mejorar performance con modelos de ensemble más avanzados

**Contenido:**
- Carga de dataset limpio
- Train/Test split (idéntico a baseline para comparación justa)
- Entrenamiento de modelos ensemble:
  - Random Forest
  - Gradient Boosting
  - AdaBoost
- Evaluación con múltiples métricas
- Identificación del mejor ensemble
- Matriz de confusión

**Output:**
- `data/processed/ensemble_results.csv` - Resultados de ensemble models
- (Opcional) `models/best_ensemble_model.pkl` - Mejor modelo guardado

**Ejecución:**
```bash
# Ejecutar DESPUÉS de baseline.ipynb
# Asegúrate de descomentar la última celda para guardar resultados
```

---

### 4️⃣ **model_comparison.ipynb** - Baseline vs Ensemble Comparison
**Propósito:** Comparación final y selección del mejor modelo global

**Contenido:**
- Carga de resultados de baseline y ensemble
- Comparación de todas las métricas
- Visualizaciones comparativas (barras por métrica)
- Análisis de mejora de ensemble sobre baseline
- Resumen estadístico por tipo de modelo
- Identificación del mejor modelo global

**Output:**
- `data/processed/all_models_comparison.csv` - Comparación completa
- `data/processed/best_model_info.csv` - Metadata del mejor modelo

**Ejecución:**
```bash
# Ejecutar DESPUÉS de baseline.ipynb Y ensemble_models.ipynb
# Requiere que ambos notebooks hayan guardado sus resultados
```

---

## 🔄 Workflow Completo

```
┌─────────────────┐
│   EDA.ipynb     │  → Análisis exploratorio
└────────┬────────┘
         │ output: fetal_health_clean.csv
         ↓
┌─────────────────┐
│ baseline.ipynb  │  → Modelos simples (referencia)
└────────┬────────┘
         │ output: baseline_results.csv
         ↓
┌─────────────────┐
│ ensemble_       │  → Modelos avanzados
│ models.ipynb    │
└────────┬────────┘
         │ output: ensemble_results.csv
         ↓
┌─────────────────┐
│ model_          │  → Comparación y selección final
│ comparison.ipynb│
└────────┬────────┘
         │ output: all_models_comparison.csv
         │         best_model_info.csv
         ↓
    Best Model
```

## 📊 Outputs Generados

| Archivo | Generado por | Descripción |
|---------|--------------|-------------|
| `fetal_health_clean.csv` | EDA.ipynb | Dataset limpio sin duplicados |
| `baseline_results.csv` | baseline.ipynb | Métricas de modelos baseline |
| `ensemble_results.csv` | ensemble_models.ipynb | Métricas de modelos ensemble |
| `all_models_comparison.csv` | model_comparison.ipynb | Comparación completa |
| `best_model_info.csv` | model_comparison.ipynb | Info del mejor modelo |

## 🎯 Beneficios de esta Estructura

✅ **Separación de responsabilidades:** Cada notebook tiene un propósito único
✅ **Reproducibilidad:** Train/test split idéntico en baseline y ensemble (random_state=25)
✅ **Modularidad:** Puedes ejecutar baseline sin ensemble, y viceversa
✅ **Profesionalismo:** Sigue mejores prácticas de MLOps
✅ **Escalabilidad:** Fácil añadir nuevos modelos sin romper el flujo
✅ **Claridad:** Workflow claro y fácil de seguir

## 🚀 Ejecución Rápida

```bash
# 1. Análisis exploratorio
# Ejecutar EDA.ipynb → genera fetal_health_clean.csv

# 2. Baseline models
# Ejecutar baseline.ipynb → genera baseline_results.csv

# 3. Ensemble models
# Ejecutar ensemble_models.ipynb → genera ensemble_results.csv

# 4. Comparación final
# Ejecutar model_comparison.ipynb → identifica mejor modelo
```

## 📝 Notas Importantes

- **Random State:** Todos los notebooks usan `random_state=25` para reproducibilidad
- **Guardado de resultados:** Debes ejecutar las celdas de guardado (algunas están comentadas)
- **Dependencias:** `model_comparison.ipynb` requiere que baseline y ensemble hayan ejecutado primero
- **Orden:** Respetar el orden de ejecución es crítico para el workflow

## 🔧 Próximos Pasos (después de comparación)

1. **Hyperparameter Tuning:** GridSearchCV o RandomizedSearchCV del mejor modelo
2. **Cross-Validation:** Validar robustez con K-Fold CV
3. **Feature Importance:** Análisis de importancia de features
4. **Model Deployment:** Crear notebook de inference/deployment
5. **Model Saving:** Guardar modelo final con pickle/joblib

---

**Proyecto:** Clasificación de Salud Fetal (Multiclass Classification)  
**Dataset:** fetal_health.csv (2113 muestras, 22 features)  
**Target:** 3 clases (Normal, Suspect, Pathological)  
**Métricas:** Accuracy, F1-Score (weighted), Recall (weighted)
