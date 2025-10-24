"""
Módulo para carga de datos
"""
import pandas as pd

def load_data(file_path):
    """
    Carga los datos desde un archivo CSV.
    
    Args:
        file_path: Ruta al archivo CSV (string o Path)
    Returns:
        DataFrame de pandas con los datos cargados
    """
    data = pd.read_csv(file_path)
    return data

if __name__ == "__main__":
    
    # Ejemplo de uso
    from configure import RAW_DATA
    
    data = load_data(RAW_DATA / 'fetal_health.csv')
    print(data.head())
    print(f"\nShape: {data.shape}")
    print(f"Columns: {list(data.columns)}")