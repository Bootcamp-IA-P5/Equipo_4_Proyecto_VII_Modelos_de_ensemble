
from pathlib import Path

# ruta raiz del proyecto
PROJECT_ROOT = Path(__file__).parent

# ruta al archivo de datos
DATA_DIR = PROJECT_ROOT / "data"
# ruta al directorio de datos crudos
RAW_DATA = DATA_DIR / "raw"
# ruta al directorio de modelos
MODELS_DIR = PROJECT_ROOT / "models"
# ruta al directorio de resultados
RESULTS_DIR = PROJECT_ROOT / "results"
# ruta al directorio de notebook
NOTEBOOKS_DIR = PROJECT_ROOT / "notebooks" 
# ruta al directorio src
SRC_DIR = PROJECT_ROOT / "src"
