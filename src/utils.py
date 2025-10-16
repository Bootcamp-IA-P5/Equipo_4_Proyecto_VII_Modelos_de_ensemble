# Utilidades para el Proyecto de Clasificación Multiclase

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics import (
    accuracy_score, precision_score, recall_score, f1_score,
    classification_report, confusion_matrix, roc_curve, auc
)
from sklearn.preprocessing import label_binarize
import json
import pickle
from pathlib import Path


def load_preprocessed_data(data_dir='../data/processed'):
    """
    Carga los datos preprocesados
    
    Returns:
        X_train, X_test, y_train, y_test
    """
    X_train = np.load(f'{data_dir}/X_train_selected.npy')
    X_test = np.load(f'{data_dir}/X_test_selected.npy')
    y_train = np.load(f'{data_dir}/y_train_resampled.npy')
    y_test = np.load(f'{data_dir}/y_test.npy')
    
    return X_train, X_test, y_train, y_test


def load_model(model_path):
    """
    Carga un modelo guardado
    
    Args:
        model_path: Ruta al archivo del modelo
        
    Returns:
        Modelo cargado
    """
    with open(model_path, 'rb') as f:
        model = pickle.load(f)
    return model


def save_model(model, model_path):
    """
    Guarda un modelo
    
    Args:
        model: Modelo a guardar
        model_path: Ruta donde guardar el modelo
    """
    Path(model_path).parent.mkdir(parents=True, exist_ok=True)
    with open(model_path, 'wb') as f:
        pickle.dump(model, f)
    print(f"✓ Modelo guardado en: {model_path}")


def plot_confusion_matrix(cm, classes, title='Matriz de Confusión', 
                          figsize=(10, 8), save_path=None):
    """
    Visualiza una matriz de confusión
    
    Args:
        cm: Matriz de confusión
        classes: Nombres de las clases
        title: Título del gráfico
        figsize: Tamaño de la figura
        save_path: Ruta para guardar la imagen
    """
    plt.figure(figsize=figsize)
    sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', 
                xticklabels=classes, yticklabels=classes,
                cbar_kws={'label': 'Número de predicciones'})
    plt.title(title, fontsize=14, fontweight='bold')
    plt.ylabel('Clase Real', fontsize=12)
    plt.xlabel('Clase Predicha', fontsize=12)
    plt.tight_layout()
    
    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        print(f"✓ Gráfico guardado en: {save_path}")
    
    plt.show()


def evaluate_model(model, X_test, y_test, class_names=None):
    """
    Evalúa un modelo y retorna métricas
    
    Args:
        model: Modelo entrenado
        X_test: Datos de prueba
        y_test: Etiquetas reales
        class_names: Nombres de las clases
        
    Returns:
        Dictionary con métricas
    """
    # Predicciones
    y_pred = model.predict(X_test)
    
    # Métricas
    accuracy = accuracy_score(y_test, y_pred)
    precision = precision_score(y_test, y_pred, average='weighted', zero_division=0)
    recall = recall_score(y_test, y_pred, average='weighted', zero_division=0)
    f1 = f1_score(y_test, y_pred, average='weighted', zero_division=0)
    
    # Matriz de confusión
    cm = confusion_matrix(y_test, y_pred)
    
    # Imprimir resultados
    print("=" * 60)
    print("MÉTRICAS DE EVALUACIÓN")
    print("=" * 60)
    print(f"Accuracy:  {accuracy:.4f}")
    print(f"Precision: {precision:.4f}")
    print(f"Recall:    {recall:.4f}")
    print(f"F1-Score:  {f1:.4f}")
    print("\n" + "=" * 60)
    
    if class_names is not None:
        print("\nReporte de Clasificación:")
        print(classification_report(y_test, y_pred, target_names=class_names, zero_division=0))
    
    results = {
        'accuracy': accuracy,
        'precision': precision,
        'recall': recall,
        'f1_score': f1,
        'confusion_matrix': cm.tolist()
    }
    
    return results


def plot_feature_importance(model, feature_names, top_n=20, 
                            title='Feature Importance', save_path=None):
    """
    Visualiza la importancia de características
    
    Args:
        model: Modelo con atributo feature_importances_
        feature_names: Nombres de las características
        top_n: Número de características principales a mostrar
        title: Título del gráfico
        save_path: Ruta para guardar
    """
    if hasattr(model, 'feature_importances_'):
        importances = model.feature_importances_
        indices = np.argsort(importances)[::-1][:top_n]
        
        plt.figure(figsize=(12, 8))
        plt.barh(range(top_n), importances[indices], color='steelblue', edgecolor='black')
        plt.yticks(range(top_n), [feature_names[i] for i in indices])
        plt.xlabel('Importancia', fontsize=12)
        plt.title(title, fontsize=14, fontweight='bold')
        plt.gca().invert_yaxis()
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
        
        plt.show()
    else:
        print("El modelo no tiene atributo 'feature_importances_'")


def compare_models(results_df, metric='test_accuracy', figsize=(12, 6), save_path=None):
    """
    Compara múltiples modelos visualmente
    
    Args:
        results_df: DataFrame con resultados de modelos
        metric: Métrica a comparar
        figsize: Tamaño de la figura
        save_path: Ruta para guardar
    """
    sorted_df = results_df.sort_values(metric, ascending=True)
    
    plt.figure(figsize=figsize)
    colors = plt.cm.viridis(np.linspace(0, 1, len(sorted_df)))
    plt.barh(sorted_df['model_name'], sorted_df[metric], color=colors, edgecolor='black')
    plt.xlabel(metric.replace('_', ' ').title(), fontsize=12)
    plt.title(f'Comparación de Modelos - {metric.replace("_", " ").title()}', 
              fontsize=14, fontweight='bold')
    plt.xlim([0, 1])
    
    # Añadir valores
    for i, v in enumerate(sorted_df[metric]):
        plt.text(v + 0.01, i, f'{v:.4f}', va='center', fontweight='bold')
    
    plt.tight_layout()
    
    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
    
    plt.show()


def save_results(results, filename):
    """
    Guarda resultados en formato JSON
    
    Args:
        results: Dictionary o DataFrame con resultados
        filename: Nombre del archivo
    """
    Path(filename).parent.mkdir(parents=True, exist_ok=True)
    
    if isinstance(results, pd.DataFrame):
        results.to_json(filename, orient='records', indent=2)
    else:
        with open(filename, 'w') as f:
            json.dump(results, f, indent=2)
    
    print(f"✓ Resultados guardados en: {filename}")


def load_results(filename):
    """
    Carga resultados desde JSON
    
    Args:
        filename: Nombre del archivo
        
    Returns:
        Resultados cargados
    """
    with open(filename, 'r') as f:
        results = json.load(f)
    return results


def plot_learning_curves(model, X_train, y_train, cv=5, figsize=(10, 6), save_path=None):
    """
    Genera curvas de aprendizaje
    
    Args:
        model: Modelo a evaluar
        X_train: Datos de entrenamiento
        y_train: Etiquetas de entrenamiento
        cv: Número de folds para cross-validation
        figsize: Tamaño de la figura
        save_path: Ruta para guardar
    """
    from sklearn.model_selection import learning_curve
    
    train_sizes, train_scores, val_scores = learning_curve(
        model, X_train, y_train, cv=cv, n_jobs=-1,
        train_sizes=np.linspace(0.1, 1.0, 10),
        scoring='accuracy'
    )
    
    train_mean = np.mean(train_scores, axis=1)
    train_std = np.std(train_scores, axis=1)
    val_mean = np.mean(val_scores, axis=1)
    val_std = np.std(val_scores, axis=1)
    
    plt.figure(figsize=figsize)
    plt.plot(train_sizes, train_mean, label='Training score', color='blue', marker='o')
    plt.fill_between(train_sizes, train_mean - train_std, train_mean + train_std, 
                     alpha=0.15, color='blue')
    plt.plot(train_sizes, val_mean, label='Validation score', color='red', marker='s')
    plt.fill_between(train_sizes, val_mean - val_std, val_mean + val_std, 
                     alpha=0.15, color='red')
    
    plt.xlabel('Training Size', fontsize=12)
    plt.ylabel('Accuracy', fontsize=12)
    plt.title('Learning Curves', fontsize=14, fontweight='bold')
    plt.legend(loc='best')
    plt.grid(alpha=0.3)
    plt.tight_layout()
    
    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
    
    plt.show()


def get_classification_metrics(y_true, y_pred, average='weighted'):
    """
    Obtiene todas las métricas de clasificación
    
    Args:
        y_true: Etiquetas reales
        y_pred: Etiquetas predichas
        average: Tipo de promedio para métricas multiclase
        
    Returns:
        Dictionary con todas las métricas
    """
    return {
        'accuracy': accuracy_score(y_true, y_pred),
        'precision': precision_score(y_true, y_pred, average=average, zero_division=0),
        'recall': recall_score(y_true, y_pred, average=average, zero_division=0),
        'f1_score': f1_score(y_true, y_pred, average=average, zero_division=0)
    }


if __name__ == "__main__":
    print("Módulo de utilidades cargado correctamente")
    print("Funciones disponibles:")
    print("  - load_preprocessed_data()")
    print("  - load_model()")
    print("  - save_model()")
    print("  - plot_confusion_matrix()")
    print("  - evaluate_model()")
    print("  - plot_feature_importance()")
    print("  - compare_models()")
    print("  - save_results()")
    print("  - load_results()")
    print("  - plot_learning_curves()")
    print("  - get_classification_metrics()")
