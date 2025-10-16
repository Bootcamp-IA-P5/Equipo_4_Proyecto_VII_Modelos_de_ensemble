# 📚 Guía de Uso del Proyecto

## 🎯 Introducción

Esta guía te ayudará a utilizar el proyecto de clasificación multiclase paso a paso.

## 📋 Requisitos Previos

1. Python 3.8 o superior instalado
2. Git instalado
3. Al menos 4GB de RAM disponible
4. Espacio en disco: ~500MB

## 🚀 Inicio Rápido

### 1. Configuración Inicial

```bash
# Clonar el repositorio
git clone https://github.com/Factoria-F5-madrid/Equipo_4_Proyecto_VII_Modelos_de_ensemble.git
cd Equipo_4_Proyecto_VII_Modelos_de_ensemble

# Crear entorno virtual
python -m venv venv

# Activar entorno virtual (Windows)
venv\Scripts\activate

# Instalar dependencias
pip install -r requirements.txt
```

### 2. Verificar la Instalación

```python
# Ejecutar en Python
import sklearn
import pandas as pd
import numpy as np
import xgboost
import lightgbm

print("✓ Todas las librerías instaladas correctamente")
```

## 📊 Flujo de Trabajo

### Paso 1: Análisis Exploratorio

```bash
jupyter notebook notebooks/01_exploratory_data_analysis.ipynb
```

**¿Qué hace?**
- Carga el dataset desde `datasets/train.csv`
- Analiza distribución de clases
- Detecta valores faltantes
- Genera visualizaciones
- Guarda resumen en `results/eda_summary.json`

**Outputs:**
- `results/eda_summary.json`
- Gráficos de distribución
- Matriz de correlación

### Paso 2: Preprocesamiento

```bash
jupyter notebook notebooks/02_preprocessing.ipynb
```

**¿Qué hace?**
- Divide datos en train/test (80/20)
- Codifica variables categóricas
- Escala características
- Selecciona características relevantes
- Aplica SMOTE si hay desbalance

**Outputs:**
- `data/processed/X_train_selected.npy`
- `data/processed/X_test_selected.npy`
- `data/processed/y_train_resampled.npy`
- `data/processed/y_test.npy`
- `models/scaler.pkl`
- `models/label_encoder.pkl`

### Paso 3: Modelos Base

```bash
jupyter notebook notebooks/03_baseline_models.ipynb
```

**¿Qué hace?**
- Entrena 6 modelos base
- Evalúa cada modelo con múltiples métricas
- Genera matrices de confusión
- Compara rendimiento

**Outputs:**
- `models/*_model.pkl` (6 modelos)
- `results/base_models_comparison.csv`
- `results/confusion_matrix_*.png`

### Paso 4: Modelos Ensemble

```bash
jupyter notebook notebooks/04_ensemble_models.ipynb
```

**¿Qué hace?**
- Implementa 8 modelos de ensemble
- Compara Bagging vs Boosting vs Stacking
- Identifica el mejor modelo

**Outputs:**
- `models/*_ensemble.pkl` (8 modelos)
- `results/ensemble_models_comparison.csv`
- Gráficos comparativos

## 🔍 Interpretación de Resultados

### Métricas Clave

- **Accuracy**: Porcentaje de predicciones correctas
  - > 0.90: Excelente
  - 0.80-0.90: Bueno
  - < 0.80: Necesita mejora

- **Precision**: De las predicciones positivas, cuántas fueron correctas
- **Recall**: De los casos positivos reales, cuántos detectamos
- **F1-Score**: Balance entre precision y recall

### Ejemplo de Análisis

```python
# Cargar resultados
import pandas as pd

results = pd.read_csv('results/ensemble_models_comparison.csv')
print(results.sort_values('test_accuracy', ascending=False))
```

## 🛠️ Casos de Uso Comunes

### 1. Entrenar un Nuevo Modelo

```python
from sklearn.ensemble import RandomForestClassifier
from src.utils import load_preprocessed_data, evaluate_model, save_model

# Cargar datos
X_train, X_test, y_train, y_test = load_preprocessed_data()

# Crear y entrenar modelo
model = RandomForestClassifier(n_estimators=200, random_state=42)
model.fit(X_train, y_train)

# Evaluar
results = evaluate_model(model, X_test, y_test)

# Guardar
save_model(model, 'models/my_custom_model.pkl')
```

### 2. Hacer Predicciones

```python
from src.utils import load_model
import numpy as np

# Cargar modelo
model = load_model('models/xgboost_ensemble.pkl')

# Cargar preprocesadores
import pickle
with open('models/scaler.pkl', 'rb') as f:
    scaler = pickle.load(f)
with open('models/label_encoder.pkl', 'rb') as f:
    label_encoder = pickle.load(f)

# Preparar nuevos datos
new_data = # ... tus datos
new_data_scaled = scaler.transform(new_data)

# Predecir
predictions = model.predict(new_data_scaled)
predictions_original = label_encoder.inverse_transform(predictions)

print("Predicciones:", predictions_original)
```

### 3. Comparar Dos Modelos

```python
from src.utils import load_model, evaluate_model, load_preprocessed_data

X_train, X_test, y_train, y_test = load_preprocessed_data()

# Cargar modelos
model1 = load_model('models/random_forest_model.pkl')
model2 = load_model('models/xgboost_ensemble.pkl')

# Evaluar
results1 = evaluate_model(model1, X_test, y_test)
results2 = evaluate_model(model2, X_test, y_test)

# Comparar
print(f"Random Forest Accuracy: {results1['accuracy']:.4f}")
print(f"XGBoost Accuracy: {results2['accuracy']:.4f}")
```

## 🔧 Personalización

### Cambiar Parámetros de Preprocesamiento

Edita `notebooks/02_preprocessing.ipynb`:

```python
# Cambiar el umbral de varianza
variance_selector = VarianceThreshold(threshold=0.05)  # Aumentar de 0.01 a 0.05

# Cambiar número de características seleccionadas
k_best = 30  # Reducir de 50 a 30

# Cambiar proporción train/test
X_train, X_test, y_train, y_test = train_test_split(
    X, y_encoded, 
    test_size=0.3,  # Cambiar de 0.2 a 0.3
    random_state=42
)
```

### Añadir un Nuevo Modelo

```python
# En notebooks/04_ensemble_models.ipynb
from catboost import CatBoostClassifier

catboost_model = CatBoostClassifier(
    iterations=100,
    learning_rate=0.1,
    random_state=42,
    verbose=False
)

catboost_model, catboost_results, catboost_cm = evaluate_ensemble(
    catboost_model, X_train, X_test, y_train, y_test, "CatBoost"
)
```

## 📈 Optimización de Hiperparámetros

```python
from sklearn.model_selection import GridSearchCV
from xgboost import XGBClassifier

# Definir grid de parámetros
param_grid = {
    'n_estimators': [50, 100, 200],
    'max_depth': [3, 5, 7],
    'learning_rate': [0.01, 0.1, 0.3]
}

# Grid Search
xgb = XGBClassifier(random_state=42)
grid_search = GridSearchCV(
    xgb, 
    param_grid, 
    cv=5, 
    scoring='accuracy',
    n_jobs=-1
)

grid_search.fit(X_train, y_train)

print("Mejores parámetros:", grid_search.best_params_)
print("Mejor score:", grid_search.best_score_)
```

## 🐛 Solución de Problemas

### Error: "ModuleNotFoundError"

```bash
# Verificar que el entorno virtual está activado
# Reinstalar dependencias
pip install -r requirements.txt --upgrade
```

### Error: "MemoryError"

```python
# Reducir tamaño del dataset o número de características
k_best = 20  # En lugar de 50

# O usar modelos más ligeros
from sklearn.linear_model import LogisticRegression
model = LogisticRegression()  # Más ligero que XGBoost
```

### Notebooks muy lentos

```python
# Reducir cross-validation folds
cv_scores = cross_val_score(model, X_train, y_train, cv=3)  # 3 en lugar de 5

# Reducir número de estimadores
model = RandomForestClassifier(n_estimators=50)  # 50 en lugar de 100
```

## 📚 Recursos Adicionales

- [Documentación de Scikit-learn](https://scikit-learn.org/)
- [XGBoost Documentation](https://xgboost.readthedocs.io/)
- [Imbalanced-learn](https://imbalanced-learn.org/)

## 🆘 Soporte

Si encuentras problemas:
1. Revisa la sección de solución de problemas
2. Consulta los issues en GitHub
3. Crea un nuevo issue con detalles del problema

---

**¡Feliz modelado!** 🚀
