# Módulo de Preprocesamiento
# Este archivo contiene funciones para preprocesar datos

from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.feature_selection import VarianceThreshold, SelectKBest, f_classif
from sklearn.model_selection import train_test_split
import numpy as np
import pandas as pd
import pickle


class DataPreprocessor:
    """
    Clase para preprocesar datos de clasificación
    """
    
    def __init__(self, variance_threshold=0.01, k_best=50):
        """
        Args:
            variance_threshold: Umbral de varianza para eliminar características
            k_best: Número de mejores características a seleccionar
        """
        self.variance_threshold = variance_threshold
        self.k_best = k_best
        
        self.scaler = StandardScaler()
        self.label_encoder = LabelEncoder()
        self.variance_selector = None
        self.feature_selector = None
        self.selected_features = None
        
    def fit_transform_target(self, y):
        """
        Codifica la variable objetivo
        
        Args:
            y: Variable objetivo
            
        Returns:
            Variable objetivo codificada
        """
        return self.label_encoder.fit_transform(y)
    
    def transform_target(self, y):
        """
        Transforma la variable objetivo
        
        Args:
            y: Variable objetivo
            
        Returns:
            Variable objetivo codificada
        """
        return self.label_encoder.transform(y)
    
    def inverse_transform_target(self, y):
        """
        Decodifica la variable objetivo
        
        Args:
            y: Variable objetivo codificada
            
        Returns:
            Variable objetivo original
        """
        return self.label_encoder.inverse_transform(y)
    
    def remove_low_variance(self, X_train, X_test):
        """
        Elimina características con baja varianza
        
        Args:
            X_train: Datos de entrenamiento
            X_test: Datos de prueba
            
        Returns:
            X_train, X_test filtrados
        """
        self.variance_selector = VarianceThreshold(threshold=self.variance_threshold)
        X_train_filtered = self.variance_selector.fit_transform(X_train)
        X_test_filtered = self.variance_selector.transform(X_test)
        
        return X_train_filtered, X_test_filtered
    
    def scale_features(self, X_train, X_test):
        """
        Escala características usando StandardScaler
        
        Args:
            X_train: Datos de entrenamiento
            X_test: Datos de prueba
            
        Returns:
            X_train, X_test escalados
        """
        X_train_scaled = self.scaler.fit_transform(X_train)
        X_test_scaled = self.scaler.transform(X_test)
        
        return X_train_scaled, X_test_scaled
    
    def select_best_features(self, X_train, X_test, y_train):
        """
        Selecciona las K mejores características
        
        Args:
            X_train: Datos de entrenamiento
            X_test: Datos de prueba
            y_train: Etiquetas de entrenamiento
            
        Returns:
            X_train, X_test con características seleccionadas
        """
        k = min(self.k_best, X_train.shape[1])
        self.feature_selector = SelectKBest(score_func=f_classif, k=k)
        X_train_selected = self.feature_selector.fit_transform(X_train, y_train)
        X_test_selected = self.feature_selector.transform(X_test)
        
        return X_train_selected, X_test_selected
    
    def preprocess(self, X_train, X_test, y_train):
        """
        Pipeline completo de preprocesamiento
        
        Args:
            X_train: Datos de entrenamiento
            X_test: Datos de prueba
            y_train: Etiquetas de entrenamiento
            
        Returns:
            X_train, X_test preprocesados y y_train codificado
        """
        # Codificar objetivo
        y_train_encoded = self.fit_transform_target(y_train)
        
        # Eliminar baja varianza
        X_train, X_test = self.remove_low_variance(X_train, X_test)
        
        # Escalar
        X_train, X_test = self.scale_features(X_train, X_test)
        
        # Seleccionar características
        X_train, X_test = self.select_best_features(X_train, X_test, y_train_encoded)
        
        return X_train, X_test, y_train_encoded
    
    def save(self, filepath):
        """
        Guarda el preprocesador
        
        Args:
            filepath: Ruta del archivo
        """
        with open(filepath, 'wb') as f:
            pickle.dump(self, f)
        print(f"✓ Preprocesador guardado en: {filepath}")
    
    @staticmethod
    def load(filepath):
        """
        Carga un preprocesador
        
        Args:
            filepath: Ruta del archivo
            
        Returns:
            Preprocesador cargado
        """
        with open(filepath, 'rb') as f:
            preprocessor = pickle.load(f)
        return preprocessor


if __name__ == "__main__":
    print("Módulo de preprocesamiento cargado correctamente")
