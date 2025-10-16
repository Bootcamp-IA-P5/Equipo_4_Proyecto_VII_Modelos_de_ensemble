# 📊 Información del Dataset

## Descripción General

El dataset contiene datos de clasificación multiclase con las siguientes características:

- **Archivo**: `train.csv`
- **Registros**: 61,880 muestras
- **Características**: 93 features numéricas (feat_1 a feat_93)
- **Variable objetivo**: `target` (categórica multiclase)
- **ID**: Identificador único por registro

## Estructura de Datos

### Características (Features)

- **Nombre**: feat_1, feat_2, ..., feat_93
- **Tipo**: Numéricas (enteros)
- **Rango**: Valores principalmente entre 0 y varios cientos
- **Distribución**: Mayoría de valores bajos, con algunos valores altos (distribución sesgada)

### Variable Objetivo (Target)

- **Nombre**: `target`
- **Tipo**: Categórica
- **Clases**: Múltiples clases (Class_1, Class_2, etc.)
- **Balance**: Verificar en EDA

## Estadísticas Descriptivas

```
Registros totales: 61,880
Features: 93
Valores faltantes: 0 (dataset completo)
```

## Consideraciones Importantes

### 1. Escala de Características
- Las características tienen diferentes escalas
- **Solución**: Aplicar StandardScaler o MinMaxScaler

### 2. Varianza de Características
- Algunas características pueden tener varianza muy baja o ser constantes
- **Solución**: Usar VarianceThreshold para eliminarlas

### 3. Correlaciones
- Posibles correlaciones altas entre características
- **Solución**: Análisis de correlación y selección de características

### 4. Balance de Clases
- Verificar si hay desbalance entre clases
- **Solución**: SMOTE, class_weight, o undersampling si es necesario

### 5. Dimensionalidad
- 93 características es un número alto
- **Solución**: Selección de características (SelectKBest, PCA, etc.)

## Preprocesamiento Recomendado

1. **División de datos**
   ```python
   train_test_split(test_size=0.2, stratify=y)
   ```

2. **Codificación de target**
   ```python
   LabelEncoder()
   ```

3. **Escalado**
   ```python
   StandardScaler()
   ```

4. **Selección de características**
   ```python
   SelectKBest(f_classif, k=50)
   ```

5. **Balance de clases** (si es necesario)
   ```python
   SMOTE()
   ```

## Formato de Datos

### CSV
```csv
id,feat_1,feat_2,...,feat_93,target
1,1,0,...,0,Class_1
2,0,0,...,0,Class_1
...
```

### Después de Preprocesamiento
- **Formato**: NumPy arrays (.npy)
- **Ubicación**: `data/processed/`
- **Archivos**:
  - `X_train_selected.npy`: Features de entrenamiento
  - `X_test_selected.npy`: Features de prueba
  - `y_train_resampled.npy`: Target de entrenamiento
  - `y_test.npy`: Target de prueba

## Uso del Dataset

### Cargar dataset original
```python
import pandas as pd

df = pd.read_csv('datasets/train.csv')
print(df.shape)  # (61880, 95)
print(df.head())
```

### Cargar datos preprocesados
```python
import numpy as np

X_train = np.load('data/processed/X_train_selected.npy')
X_test = np.load('data/processed/X_test_selected.npy')
y_train = np.load('data/processed/y_train_resampled.npy')
y_test = np.load('data/processed/y_test.npy')
```

## Análisis Exploratorio Sugerido

1. **Distribución de clases**
   - Contar instancias por clase
   - Verificar balance

2. **Estadísticas por característica**
   - Media, mediana, desviación estándar
   - Valores mínimos y máximos

3. **Correlaciones**
   - Matriz de correlación
   - Identificar features altamente correlacionadas

4. **Outliers**
   - Detectar valores atípicos
   - Decidir tratamiento

5. **Varianza**
   - Identificar features con baja varianza
   - Considerar eliminarlas

## Métricas de Evaluación Recomendadas

Para clasificación multiclase:

- **Accuracy**: Proporción de predicciones correctas
- **Precision**: Por clase y promedio weighted
- **Recall**: Por clase y promedio weighted
- **F1-Score**: Por clase y promedio weighted
- **Matriz de Confusión**: Análisis detallado de errores
- **Cross-Validation**: Para validar robustez

## Notas Adicionales

- El dataset no contiene valores faltantes (completamente poblado)
- Todas las características son numéricas (no requiere encoding adicional)
- La columna `id` debe ser eliminada antes del modelado (no es feature predictiva)
- Considerar crear features derivadas si tiene sentido en el contexto

---

**Última actualización**: Octubre 2025
