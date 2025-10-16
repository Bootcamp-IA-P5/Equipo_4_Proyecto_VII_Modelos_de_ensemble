# 🎯 Proyecto VII - Clasificación Multiclase con Modelos de Ensemble

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/)
[![Scikit-learn](https://img.shields.io/badge/Scikit--learn-1.0+-orange.svg)](https://scikit-learn.org/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

[Enlace a gestión del Proyecto](https://github.com/orgs/Factoria-F5-madrid/projects/49/views/1)

## 📋 Descripción del Proyecto

Este proyecto implementa una solución completa de **Machine Learning** para resolver un problema de **clasificación multiclase** utilizando técnicas de ensemble. El objetivo es desarrollar modelos robustos que puedan clasificar instancias en múltiples categorías mutuamente excluyentes, aplicando las mejores prácticas en análisis de datos, preprocesamiento, modelado y evaluación.

### 🎯 Objetivos

1. Realizar un análisis exploratorio exhaustivo del dataset
2. Implementar pipeline de preprocesamiento robusto
3. Entrenar y evaluar múltiples modelos de clasificación
4. Comparar modelos base vs. modelos de ensemble
5. Optimizar hiperparámetros del mejor modelo
6. Documentar resultados y conclusiones

## 🗂️ Estructura del Proyecto

```
Equipo_4_Proyecto_VII_Modelos_de_ensemble/
│
├── datasets/                       # Datos originales
│   └── train.csv                   # Dataset de entrenamiento
│
├── data/                           # Datos procesados
│   └── processed/                  # Datos preprocesados
│       ├── X_train_scaled.npy
│       ├── X_test_scaled.npy
│       ├── X_train_selected.npy
│       ├── X_test_selected.npy
│       ├── y_train.npy
│       ├── y_test.npy
│       └── selected_features.json
│
├── notebooks/                      # Jupyter Notebooks
│   ├── 01_exploratory_data_analysis.ipynb
│   ├── 02_preprocessing.ipynb
│   ├── 03_baseline_models.ipynb
│   └── 04_ensemble_models.ipynb
│
├── src/                            # Código fuente
│   └── utils.py                    # Funciones de utilidad
│
├── models/                         # Modelos entrenados
│   ├── label_encoder.pkl
│   ├── scaler.pkl
│   ├── *_model.pkl                 # Modelos base
│   └── *_ensemble.pkl              # Modelos ensemble
│
├── results/                        # Resultados y visualizaciones
│   ├── eda_summary.json
│   ├── preprocessing_summary.json
│   ├── base_models_comparison.csv
│   ├── ensemble_models_comparison.csv
│   └── *.png                       # Gráficos y visualizaciones
│
├── requirements.txt                # Dependencias del proyecto
├── .gitignore                      # Archivos ignorados por Git
└── README.md                       # Este archivo
```

## 🚀 Instalación y Configuración

### Prerrequisitos

- Python 3.8 o superior
- pip (gestor de paquetes de Python)
- Git

### Instalación

1. **Clonar el repositorio**
```bash
git clone https://github.com/Factoria-F5-madrid/Equipo_4_Proyecto_VII_Modelos_de_ensemble.git
cd Equipo_4_Proyecto_VII_Modelos_de_ensemble
```

2. **Crear entorno virtual (recomendado)**
```bash
python -m venv venv
```

3. **Activar el entorno virtual**
- Windows:
```bash
venv\Scripts\activate
```
- macOS/Linux:
```bash
source venv/bin/activate
```

4. **Instalar dependencias**
```bash
pip install -r requirements.txt
```

## 📊 Dataset

El dataset contiene:
- **61,880 registros** de entrenamiento
- **93 características numéricas** (feat_1 a feat_93)
- **1 variable objetivo** (target) con múltiples clases
- **Sin valores faltantes**

## 🔄 Pipeline del Proyecto

### 1️⃣ Análisis Exploratorio de Datos (EDA)
- Análisis de distribución de clases
- Detección de valores faltantes
- Estadísticas descriptivas
- Análisis de correlaciones
- Visualizaciones clave

**Notebook:** `01_exploratory_data_analysis.ipynb`

### 2️⃣ Preprocesamiento
- División de datos (train/test: 80/20)
- Codificación de variables
- Escalado de características (StandardScaler)
- Eliminación de características con baja varianza
- Selección de características (ANOVA F-value, Mutual Information)
- Manejo de desbalance de clases (SMOTE si es necesario)

**Notebook:** `02_preprocessing.ipynb`

### 3️⃣ Modelos Base
Implementación y evaluación de modelos base:
- ✅ Logistic Regression
- ✅ K-Nearest Neighbors (KNN)
- ✅ Support Vector Machine (SVM)
- ✅ Decision Tree
- ✅ Random Forest
- ✅ Naive Bayes

**Notebook:** `03_baseline_models.ipynb`

### 4️⃣ Modelos de Ensemble
Implementación de técnicas avanzadas de ensemble:
- ✅ **Bagging**: BaggingClassifier, Extra Trees
- ✅ **Boosting**: AdaBoost, Gradient Boosting, XGBoost, LightGBM
- ✅ **Voting**: Soft Voting Classifier
- ✅ **Stacking**: Stacking Classifier

**Notebook:** `04_ensemble_models.ipynb`

## 📈 Métricas de Evaluación

Para cada modelo se calculan:
- **Accuracy**: Precisión general del modelo
- **Precision**: Precisión por clase (weighted)
- **Recall**: Recall por clase (weighted)
- **F1-Score**: Media armónica de precision y recall
- **Matriz de Confusión**: Análisis detallado de errores
- **Cross-Validation**: Validación cruzada (5-fold)
- **Tiempo de entrenamiento**: Eficiencia computacional

## 🛠️ Uso

### Ejecutar el análisis completo

1. **Análisis Exploratorio:**
```bash
jupyter notebook notebooks/01_exploratory_data_analysis.ipynb
```

2. **Preprocesamiento:**
```bash
jupyter notebook notebooks/02_preprocessing.ipynb
```

3. **Modelos Base:**
```bash
jupyter notebook notebooks/03_baseline_models.ipynb
```

4. **Modelos Ensemble:**
```bash
jupyter notebook notebooks/04_ensemble_models.ipynb
```

### Usar las utilidades

```python
from src.utils import load_preprocessed_data, evaluate_model, plot_confusion_matrix

# Cargar datos
X_train, X_test, y_train, y_test = load_preprocessed_data()

# Cargar modelo
model = load_model('models/xgboost_ensemble.pkl')

# Evaluar
results = evaluate_model(model, X_test, y_test)
```

## 📊 Resultados Esperados

Los resultados se guardarán en la carpeta `results/`:
- Comparación de modelos (CSV)
- Matrices de confusión (PNG)
- Gráficos comparativos (PNG)
- Resúmenes en formato JSON

## 🧪 Tecnologías Utilizadas

- **Python 3.8+**: Lenguaje de programación
- **NumPy & Pandas**: Manipulación de datos
- **Matplotlib & Seaborn**: Visualización
- **Scikit-learn**: Modelos de ML y preprocesamiento
- **XGBoost**: Gradient Boosting optimizado
- **LightGBM**: Gradient Boosting eficiente
- **Imbalanced-learn**: Manejo de desbalance
- **Jupyter**: Notebooks interactivos

## 👥 Equipo

**Equipo 4** - Factoría F5 Madrid

## 📝 Licencia

Este proyecto está bajo la Licencia MIT.

## 🤝 Contribuciones

Las contribuciones son bienvenidas. Por favor:
1. Fork el proyecto
2. Crea una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

## 📞 Contacto

Para preguntas o sugerencias, por favor abre un issue en el repositorio.

---

⭐ **¡No olvides dar una estrella al proyecto si te ha sido útil!** ⭐
