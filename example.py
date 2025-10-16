"""
Script de Ejemplo - Clasificación Multiclase
Este script muestra cómo usar el proyecto de forma programática
"""

import numpy as np
import pandas as pd
import pickle
from pathlib import Path

# Importar utilidades personalizadas
import sys
sys.path.append('src')
from utils import (
    load_preprocessed_data,
    load_model,
    evaluate_model,
    plot_confusion_matrix,
    compare_models
)


def main():
    """
    Función principal que ejecuta el flujo completo
    """
    print("=" * 80)
    print("PROYECTO DE CLASIFICACIÓN MULTICLASE - EJEMPLO DE USO")
    print("=" * 80)
    
    # 1. Cargar datos preprocesados
    print("\n1. Cargando datos preprocesados...")
    X_train, X_test, y_train, y_test = load_preprocessed_data()
    print(f"   ✓ Datos cargados: {X_train.shape[0]} muestras de entrenamiento")
    print(f"   ✓ Características: {X_train.shape[1]}")
    
    # 2. Cargar label encoder
    print("\n2. Cargando codificador de etiquetas...")
    with open('models/label_encoder.pkl', 'rb') as f:
        label_encoder = pickle.load(f)
    print(f"   ✓ Número de clases: {len(label_encoder.classes_)}")
    print(f"   ✓ Clases: {label_encoder.classes_}")
    
    # 3. Cargar y evaluar modelos
    print("\n3. Evaluando modelos guardados...")
    
    models_to_test = [
        ('Random Forest', 'models/random_forest_model.pkl'),
        ('XGBoost', 'models/xgboost_ensemble.pkl'),
        ('Gradient Boosting', 'models/gradient_boosting_ensemble.pkl')
    ]
    
    results_list = []
    
    for model_name, model_path in models_to_test:
        if Path(model_path).exists():
            print(f"\n   Evaluando {model_name}...")
            model = load_model(model_path)
            results = evaluate_model(model, X_test, y_test, label_encoder.classes_)
            results['model_name'] = model_name
            results_list.append(results)
        else:
            print(f"   ⚠️ Modelo no encontrado: {model_path}")
            print(f"   Ejecuta primero los notebooks de entrenamiento")
    
    # 4. Comparar resultados
    if results_list:
        print("\n4. Comparando resultados...")
        results_df = pd.DataFrame(results_list)
        results_df = results_df.sort_values('accuracy', ascending=False)
        
        print("\n" + "=" * 80)
        print("COMPARACIÓN DE MODELOS")
        print("=" * 80)
        print(results_df[['model_name', 'accuracy', 'precision', 'recall', 'f1_score']].to_string(index=False))
        
        # 5. Mejor modelo
        best_model_name = results_df.iloc[0]['model_name']
        best_accuracy = results_df.iloc[0]['accuracy']
        
        print("\n" + "=" * 80)
        print(f"🏆 MEJOR MODELO: {best_model_name}")
        print(f"   Accuracy: {best_accuracy:.4f}")
        print("=" * 80)
    else:
        print("\n⚠️ No se encontraron modelos entrenados.")
        print("   Ejecuta primero los notebooks:")
        print("   - 03_baseline_models.ipynb")
        print("   - 04_ensemble_models.ipynb")
    
    print("\n✓ Proceso completado")


def predict_example():
    """
    Ejemplo de cómo hacer predicciones con nuevos datos
    """
    print("\n" + "=" * 80)
    print("EJEMPLO DE PREDICCIÓN")
    print("=" * 80)
    
    # Cargar modelo
    model_path = 'models/xgboost_ensemble.pkl'
    if not Path(model_path).exists():
        print("⚠️ Modelo no encontrado. Entrena primero los modelos.")
        return
    
    model = load_model(model_path)
    
    # Cargar preprocesadores
    with open('models/scaler.pkl', 'rb') as f:
        scaler = pickle.load(f)
    with open('models/label_encoder.pkl', 'rb') as f:
        label_encoder = pickle.load(f)
    
    # Cargar datos de prueba
    _, X_test, _, y_test = load_preprocessed_data()
    
    # Tomar una muestra
    sample_size = 5
    X_sample = X_test[:sample_size]
    y_sample = y_test[:sample_size]
    
    # Hacer predicciones
    predictions = model.predict(X_sample)
    predictions_original = label_encoder.inverse_transform(predictions)
    actual_original = label_encoder.inverse_transform(y_sample)
    
    print("\nPredicciones vs Real:")
    print("-" * 40)
    for i in range(sample_size):
        status = "✓" if predictions[i] == y_sample[i] else "✗"
        print(f"{status} Muestra {i+1}: Predicho={predictions_original[i]}, Real={actual_original[i]}")
    
    # Calcular accuracy de la muestra
    accuracy = (predictions == y_sample).sum() / sample_size
    print(f"\nAccuracy en muestra: {accuracy:.2%}")


if __name__ == "__main__":
    # Ejecutar función principal
    main()
    
    # Ejecutar ejemplo de predicción
    predict_example()
