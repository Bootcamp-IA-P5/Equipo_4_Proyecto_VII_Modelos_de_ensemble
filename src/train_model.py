"""
Script de entrenamiento de modelos baseline y ensemble para clasificación de salud fetal
Incluye optimización automática de hiperparámetros usando GridSearchCV
Diseñado para ejecutarse dentro del contenedor Docker backend
"""
import pandas as pd
import numpy as np
import joblib
import json
from pathlib import Path
from datetime import datetime
from sklearn.model_selection import (
    train_test_split, cross_val_score, StratifiedKFold, GridSearchCV
)
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import (
    accuracy_score, precision_score, recall_score, f1_score,
    classification_report, confusion_matrix
)

# Modelos baseline
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.svm import SVC

# Modelos ensemble
from sklearn.ensemble import (
    RandomForestClassifier,
    GradientBoostingClassifier,
    AdaBoostClassifier,
    BaggingClassifier,
    VotingClassifier,
    StackingClassifier
)
from xgboost import XGBClassifier

# Para manejo de desbalanceo
from imblearn.over_sampling import SMOTE
from collections import Counter

import warnings
warnings.filterwarnings('ignore')


class FetalHealthModelTrainer:
    """Clase para entrenar y evaluar modelos de clasificación de salud fetal"""
    
    def __init__(self, data_path, random_state=42):
        """
        Inicializar el trainer
        
        Args:
            data_path: Ruta al archivo CSV con los datos
            random_state: Semilla para reproducibilidad
        """
        self.data_path = Path(data_path)
        self.random_state = random_state
        self.models = {}
        self.results = {}
        self.best_model = None
        self.best_model_name = None
        self.scaler = StandardScaler()
        
        # Directorios (en el contenedor Docker)
        self.models_dir = Path("/app/models")
        self.reports_dir = Path("/app/reports")
        self.models_dir.mkdir(exist_ok=True, parents=True)
        self.reports_dir.mkdir(exist_ok=True, parents=True)
        
    def load_and_explore_data(self):
        """Cargar y explorar el dataset"""
        print("=" * 80)
        print("CARGANDO Y EXPLORANDO DATOS")
        print("=" * 80)
        
        # Cargar datos
        self.df = pd.read_csv(self.data_path)
        print(f"\n✓ Dataset cargado: {self.df.shape[0]} filas, {self.df.shape[1]} columnas")
        
        # Información básica
        print(f"\n📊 Columnas del dataset:")
        for col in self.df.columns:
            print(f"   - {col}")
        
        # Valores faltantes
        missing = self.df.isnull().sum()
        if missing.sum() > 0:
            print(f"\n⚠️  Valores faltantes encontrados:")
            print(missing[missing > 0])
        else:
            print(f"\n✓ No hay valores faltantes")
        
        # Distribución de clases
        print(f"\n📊 Distribución de clases (fetal_health):")
        class_dist = self.df['fetal_health'].value_counts().sort_index()
        for cls, count in class_dist.items():
            percentage = (count / len(self.df)) * 100
            class_name = {1.0: 'Normal', 2.0: 'Suspect', 3.0: 'Pathological'}.get(cls, cls)
            print(f"   Clase {int(cls)} ({class_name}): {count} ({percentage:.2f}%)")
        
        return self.df
    
    def preprocess_data(self, test_size=0.2, apply_smote=True):
        """
        Preprocesar datos: separar features/target, normalizar, dividir train/test
        
        Args:
            test_size: Proporción de datos para test
            apply_smote: Si aplicar SMOTE para balancear clases
        """
        print("\n" + "=" * 80)
        print("PREPROCESANDO DATOS")
        print("=" * 80)
        
        # Separar features y target
        X = self.df.drop('fetal_health', axis=1)
        y = self.df['fetal_health']
        
        print(f"\n✓ Features: {X.shape[1]} columnas")
        print(f"✓ Target: {y.name}")
        
        # Dividir en train y test
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=test_size, random_state=self.random_state, stratify=y
        )
        
        print(f"\n✓ Train set: {X_train.shape[0]} muestras")
        print(f"✓ Test set: {X_test.shape[0]} muestras")
        
        # Normalizar datos
        X_train_scaled = self.scaler.fit_transform(X_train)
        X_test_scaled = self.scaler.transform(X_test)
        
        print(f"\n✓ Datos normalizados con StandardScaler")
        
        # Aplicar SMOTE si está habilitado
        if apply_smote:
            print(f"\n📊 Distribución antes de SMOTE:")
            print(f"   {dict(Counter(y_train))}")
            
            smote = SMOTE(random_state=self.random_state)
            X_train_scaled, y_train = smote.fit_resample(X_train_scaled, y_train)
            
            print(f"\n✓ SMOTE aplicado")
            print(f"📊 Distribución después de SMOTE:")
            print(f"   {dict(Counter(y_train))}")
        
        self.X_train = X_train_scaled
        self.X_test = X_test_scaled
        self.y_train = y_train
        self.y_test = y_test
        self.feature_names = X.columns.tolist()
        
        return self.X_train, self.X_test, self.y_train, self.y_test
    
    def initialize_models(self):
        """Inicializar modelos baseline y ensemble con optimización de hiperparámetros"""
        print("\n" + "=" * 80)
        print("INICIALIZANDO MODELOS CON OPTIMIZACIÓN DE HIPERPARÁMETROS")
        print("=" * 80)
        
        # Configuración de validación cruzada para GridSearch
        cv_strategy = StratifiedKFold(n_splits=5, shuffle=True, random_state=self.random_state)
        
        # Modelos Baseline (sin optimización para comparación rápida)
        baseline_models = {
            'Logistic Regression': LogisticRegression(
                max_iter=1000, random_state=self.random_state, class_weight='balanced'
            ),
            'Decision Tree': DecisionTreeClassifier(
                max_depth=10, random_state=self.random_state, class_weight='balanced'
            ),
            'K-Nearest Neighbors': KNeighborsClassifier(n_neighbors=5),
            'Naive Bayes': GaussianNB(),
            'Support Vector Machine': SVC(
                kernel='rbf', probability=True, random_state=self.random_state, class_weight='balanced'
            )
        }
        
        # Modelos Ensemble CON optimización de hiperparámetros
        print("\n🔍 Configurando GridSearchCV para modelos ensemble...")
        print("   Nota: La optimización puede tardar varios minutos")
        
        # AdaBoost con GridSearchCV
        print("\n📊 AdaBoost: Optimizando hiperparámetros...")
        ada_param_grid = {
            'n_estimators': [50, 100, 150, 200],
            'learning_rate': [0.5, 0.8, 1.0, 1.2],
            'estimator__max_depth': [2, 3, 4]
        }
        ada_base = AdaBoostClassifier(
            estimator=DecisionTreeClassifier(random_state=self.random_state),
            random_state=self.random_state
        )
        ada_grid = GridSearchCV(
            ada_base, ada_param_grid, cv=cv_strategy, 
            scoring='accuracy', n_jobs=-1, verbose=1
        )
        
        # Random Forest con GridSearchCV
        print("\n📊 Random Forest: Optimizando hiperparámetros...")
        rf_param_grid = {
            'n_estimators': [50, 100, 150],
            'max_depth': [10, 15, 20, None],
            'min_samples_split': [2, 5],
            'max_features': ['sqrt', 'log2']
        }
        rf_base = RandomForestClassifier(
            random_state=self.random_state,
            class_weight='balanced',
            n_jobs=1  # GridSearch ya paraleliza
        )
        rf_grid = GridSearchCV(
            rf_base, rf_param_grid, cv=cv_strategy,
            scoring='accuracy', n_jobs=-1, verbose=1
        )
        
        # Gradient Boosting con GridSearchCV
        print("\n📊 Gradient Boosting: Optimizando hiperparámetros...")
        gb_param_grid = {
            'n_estimators': [50, 100, 150],
            'learning_rate': [0.05, 0.1, 0.2],
            'max_depth': [3, 4, 5],
            'subsample': [0.8, 1.0]
        }
        gb_base = GradientBoostingClassifier(random_state=self.random_state)
        gb_grid = GridSearchCV(
            gb_base, gb_param_grid, cv=cv_strategy,
            scoring='accuracy', n_jobs=-1, verbose=1
        )
        
        # Bagging con GridSearchCV (optimización ligera)
        print("\n📊 Bagging: Optimizando hiperparámetros...")
        bagging_param_grid = {
            'n_estimators': [30, 50, 70],
            'max_samples': [0.7, 0.8, 1.0],
            'max_features': [0.7, 0.8, 1.0]
        }
        bagging_base = BaggingClassifier(random_state=self.random_state, n_jobs=1)
        bagging_grid = GridSearchCV(
            bagging_base, bagging_param_grid, cv=cv_strategy,
            scoring='accuracy', n_jobs=-1, verbose=1
        )
        
        ensemble_models = {
            'Random Forest': rf_grid,
            'Gradient Boosting': gb_grid,
            'AdaBoost': ada_grid,
            'Bagging': bagging_grid,
        }
        
        # XGBoost (deshabilitado por problemas de compatibilidad con sklearn)
        # try:
        #     ensemble_models['XGBoost'] = XGBClassifier(
        #         n_estimators=100, learning_rate=0.1, max_depth=5,
        #         random_state=self.random_state, eval_metric='mlogloss'
        #     )
        # except Exception as e:
        #     print(f"⚠️ XGBoost no disponible: {e}")
        
        # Voting y Stacking (sin GridSearch para evitar complejidad excesiva)
        try:
            ensemble_models['Voting Classifier'] = VotingClassifier(
                estimators=[
                    ('rf', RandomForestClassifier(n_estimators=50, random_state=self.random_state)),
                    ('gb', GradientBoostingClassifier(n_estimators=50, random_state=self.random_state)),
                ],
                voting='soft'
            )
        except Exception as e:
            print(f"⚠️ Voting Classifier no disponible: {e}")
        
        try:
            ensemble_models['Stacking Classifier'] = StackingClassifier(
                estimators=[
                    ('rf', RandomForestClassifier(n_estimators=50, random_state=self.random_state)),
                    ('gb', GradientBoostingClassifier(n_estimators=50, random_state=self.random_state)),
                ],
                final_estimator=LogisticRegression(random_state=self.random_state),
                cv=5
            )
        except Exception as e:
            print(f"⚠️ Stacking Classifier no disponible: {e}")
        
        self.models = {**baseline_models, **ensemble_models}
        
        print(f"\n✓ {len(baseline_models)} modelos baseline inicializados")
        print(f"✓ {len(ensemble_models)} modelos ensemble configurados con GridSearchCV")
        print(f"\n⏱️  Tiempo estimado total: 10-20 minutos")
        
        return self.models
    
    def train_and_evaluate(self):
        """Entrenar y evaluar todos los modelos (con optimización automática para GridSearchCV)"""
        print("\n" + "=" * 80)
        print("ENTRENANDO Y EVALUANDO MODELOS CON OPTIMIZACIÓN")
        print("=" * 80)
        
        for name, model in self.models.items():
            print(f"\n{'─' * 80}")
            print(f"Entrenando: {name}")
            print(f"{'─' * 80}")
            
            try:
                # Verificar si es un GridSearchCV
                is_grid_search = hasattr(model, 'best_estimator_')
                
                # Ajustar etiquetas para XGBoost (requiere clases 0-indexed)
                if 'XGBoost' in name:
                    y_train_adjusted = self.y_train - 1
                    y_test_adjusted = self.y_test - 1
                else:
                    y_train_adjusted = self.y_train
                    y_test_adjusted = self.y_test
                
                # Entrenar modelo (GridSearchCV hará la optimización automáticamente)
                model.fit(self.X_train, y_train_adjusted)
                
                # Si es GridSearchCV, usar el mejor estimador encontrado
                if isinstance(model, GridSearchCV):
                    print(f"\n🎯 Mejores hiperparámetros encontrados:")
                    for param, value in model.best_params_.items():
                        print(f"   {param}: {value}")
                    print(f"   Mejor CV Score: {model.best_score_:.4f}")
                    best_model = model.best_estimator_
                else:
                    best_model = model
                
                # Predicciones usando el mejor modelo
                y_pred_train = best_model.predict(self.X_train)
                y_pred_test = best_model.predict(self.X_test)
                
                # Ajustar predicciones de XGBoost (convertir de 0-indexed a 1-indexed)
                if 'XGBoost' in name:
                    y_pred_train = y_pred_train + 1
                    y_pred_test = y_pred_test + 1
                
                # Predicciones de probabilidad (si están disponibles)
                try:
                    y_pred_proba = best_model.predict_proba(self.X_test)
                except:
                    y_pred_proba = None
                
                # Métricas
                train_accuracy = accuracy_score(self.y_train, y_pred_train)
                test_accuracy = accuracy_score(self.y_test, y_pred_test)
                precision = precision_score(self.y_test, y_pred_test, average='weighted', zero_division=0)
                recall = recall_score(self.y_test, y_pred_test, average='weighted', zero_division=0)
                f1 = f1_score(self.y_test, y_pred_test, average='weighted', zero_division=0)
                
                # Cross-validation (usar el modelo optimizado si es GridSearchCV)
                cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=self.random_state)
                if isinstance(model, GridSearchCV):
                    # Para GridSearchCV, usar el best_score_ directamente
                    cv_mean = model.best_score_
                    cv_std = model.cv_results_['std_test_score'][model.best_index_]
                else:
                    # Para XGBoost usar etiquetas ajustadas
                    if 'XGBoost' in name:
                        cv_scores = cross_val_score(best_model, self.X_train, y_train_adjusted, cv=cv, scoring='accuracy')
                    else:
                        cv_scores = cross_val_score(best_model, self.X_train, self.y_train, cv=cv, scoring='accuracy')
                    cv_mean = cv_scores.mean()
                    cv_std = cv_scores.std()
                
                # Guardar resultados (guardar best_estimator para GridSearchCV)
                result_data = {
                    'model': best_model,  # Guardar el mejor modelo, no el GridSearchCV
                    'train_accuracy': train_accuracy,
                    'test_accuracy': test_accuracy,
                    'precision': precision,
                    'recall': recall,
                    'f1_score': f1,
                    'cv_mean': cv_mean,
                    'cv_std': cv_std,
                    'y_pred': y_pred_test,
                    'y_pred_proba': y_pred_proba,
                    'confusion_matrix': confusion_matrix(self.y_test, y_pred_test),
                    'classification_report': classification_report(self.y_test, y_pred_test, zero_division=0)
                }
                
                # Agregar hiperparámetros optimizados si es GridSearchCV
                if isinstance(model, GridSearchCV):
                    result_data['best_params'] = model.best_params_
                    result_data['grid_search_cv_score'] = model.best_score_
                
                self.results[name] = result_data
                
                # Imprimir resultados
                print(f"✓ Train Accuracy: {train_accuracy:.4f}")
                print(f"✓ Test Accuracy:  {test_accuracy:.4f}")
                print(f"✓ Precision:      {precision:.4f}")
                print(f"✓ Recall:         {recall:.4f}")
                print(f"✓ F1-Score:       {f1:.4f}")
                print(f"✓ CV Score:       {cv_mean:.4f} (+/- {cv_std:.4f})")
                
            except Exception as e:
                print(f"❌ Error entrenando {name}: {str(e)}")
                continue
        
        return self.results
    
    def get_best_model(self):
        """Obtener el mejor modelo basado en test accuracy"""
        print("\n" + "=" * 80)
        print("SELECCIONANDO MEJOR MODELO")
        print("=" * 80)
        
        # Crear tabla de comparación
        comparison = []
        for name, result in self.results.items():
            comparison.append({
                'Model': name,
                'Train Acc': result['train_accuracy'],
                'Test Acc': result['test_accuracy'],
                'Precision': result['precision'],
                'Recall': result['recall'],
                'F1-Score': result['f1_score'],
                'CV Mean': result['cv_mean'],
                'CV Std': result['cv_std']
            })
        
        df_comparison = pd.DataFrame(comparison)
        df_comparison = df_comparison.sort_values('Test Acc', ascending=False)
        
        print("\n📊 TABLA DE COMPARACIÓN DE MODELOS:")
        print(df_comparison.to_string(index=False))
        
        # Mejor modelo
        best_model_name = df_comparison.iloc[0]['Model']
        self.best_model_name = best_model_name
        self.best_model = self.results[best_model_name]['model']
        
        print(f"\n🏆 MEJOR MODELO: {best_model_name}")
        print(f"   Test Accuracy: {df_comparison.iloc[0]['Test Acc']:.4f}")
        print(f"   F1-Score: {df_comparison.iloc[0]['F1-Score']:.4f}")
        
        return self.best_model, self.best_model_name, df_comparison
    
    def save_results(self):
        """Guardar modelo y reportes"""
        print("\n" + "=" * 80)
        print("GUARDANDO RESULTADOS")
        print("=" * 80)
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # Guardar mejor modelo
        model_path = self.models_dir / "fetal_health_model.pkl"
        model_data = {
            'model': self.best_model,
            'scaler': self.scaler,
            'feature_names': self.feature_names,
            'model_name': self.best_model_name
        }
        
        # Agregar hiperparámetros optimizados si existen
        if 'best_params' in self.results[self.best_model_name]:
            model_data['best_params'] = self.results[self.best_model_name]['best_params']
            model_data['optimized'] = True
        else:
            model_data['optimized'] = False
        
        joblib.dump(model_data, model_path)
        print(f"\n✓ Modelo guardado en: {model_path}")
        
        # Guardar scaler por separado
        scaler_path = self.models_dir / "scaler.pkl"
        joblib.dump(self.scaler, scaler_path)
        print(f"✓ Scaler guardado en: {scaler_path}")
        
        # Guardar tabla de comparación
        comparison_path = self.reports_dir / f"model_comparison_{timestamp}.csv"
        _, _, df_comparison = self.get_best_model()
        df_comparison.to_csv(comparison_path, index=False)
        print(f"✓ Comparación guardada en: {comparison_path}")
        
        # Guardar reporte detallado del mejor modelo
        report_path = self.reports_dir / f"best_model_report_{timestamp}.txt"
        with open(report_path, 'w', encoding='utf-8') as f:
            f.write("=" * 80 + "\n")
            f.write(f"REPORTE DEL MEJOR MODELO: {self.best_model_name}\n")
            f.write("=" * 80 + "\n\n")
            
            result = self.results[self.best_model_name]
            
            f.write(f"Modelo: {self.best_model_name}\n")
            f.write(f"Fecha: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            
            # Agregar hiperparámetros optimizados si existen
            if 'best_params' in result:
                f.write(f"Optimizado: Sí (GridSearchCV)\n")
                f.write(f"\nMEJORES HIPERPARÁMETROS:\n")
                for param, value in result['best_params'].items():
                    f.write(f"  {param}: {value}\n")
                f.write(f"  Grid Search CV Score: {result.get('grid_search_cv_score', 'N/A'):.4f}\n")
            else:
                f.write(f"Optimizado: No (hiperparámetros por defecto)\n")
            
            f.write("\n")
            
            f.write("MÉTRICAS DE RENDIMIENTO:\n")
            f.write(f"  Train Accuracy: {result['train_accuracy']:.4f}\n")
            f.write(f"  Test Accuracy:  {result['test_accuracy']:.4f}\n")
            f.write(f"  Precision:      {result['precision']:.4f}\n")
            f.write(f"  Recall:         {result['recall']:.4f}\n")
            f.write(f"  F1-Score:       {result['f1_score']:.4f}\n")
            f.write(f"  CV Mean:        {result['cv_mean']:.4f}\n")
            f.write(f"  CV Std:         {result['cv_std']:.4f}\n\n")
            
            f.write("MATRIZ DE CONFUSIÓN:\n")
            f.write(str(result['confusion_matrix']) + "\n\n")
            
            f.write("CLASSIFICATION REPORT:\n")
            f.write(result['classification_report'] + "\n")
        
        print(f"✓ Reporte guardado en: {report_path}")
        
        # Guardar métricas en JSON
        metrics_path = self.reports_dir / f"metrics_{timestamp}.json"
        metrics = {}
        for name, result in self.results.items():
            model_metrics = {
                'train_accuracy': float(result['train_accuracy']),
                'test_accuracy': float(result['test_accuracy']),
                'precision': float(result['precision']),
                'recall': float(result['recall']),
                'f1_score': float(result['f1_score']),
                'cv_mean': float(result['cv_mean']),
                'cv_std': float(result['cv_std'])
            }
            
            # Agregar hiperparámetros optimizados si existen
            if 'best_params' in result:
                model_metrics['best_params'] = result['best_params']
                model_metrics['optimized'] = True
                model_metrics['grid_search_cv_score'] = float(result.get('grid_search_cv_score', 0))
            else:
                model_metrics['optimized'] = False
            
            metrics[name] = model_metrics
        
        with open(metrics_path, 'w', encoding='utf-8') as f:
            json.dump(metrics, f, indent=2)
        
        print(f"✓ Métricas JSON guardadas en: {metrics_path}")
        
        print("\n✓ Todos los resultados guardados exitosamente")


def main():
    """Función principal"""
    print("\n" + "=" * 80)
    print("ENTRENAMIENTO DE MODELOS - CLASIFICACIÓN DE SALUD FETAL")
    print("=" * 80)
    print("Ejecutándose en contenedor Docker")
    print("=" * 80)
    
    # Configuración (rutas en el contenedor)
    # Usar el dataset limpio generado por eda.py
    data_path = "/app/data/processed/fetal_health_clean.csv"
    
    # Crear trainer
    trainer = FetalHealthModelTrainer(data_path=data_path, random_state=42)
    
    # Pipeline completo
    trainer.load_and_explore_data()
    trainer.preprocess_data(test_size=0.2, apply_smote=True)
    trainer.initialize_models()
    trainer.train_and_evaluate()
    trainer.get_best_model()
    trainer.save_results()
    
    print("\n" + "=" * 80)
    print("✅ ENTRENAMIENTO COMPLETADO EXITOSAMENTE")
    print("=" * 80)
    print(f"Modelo guardado en: /app/models/fetal_health_model.pkl")
    print(f"Reportes guardados en: /app/reports/")
    print("=" * 80)


if __name__ == "__main__":
    main()
