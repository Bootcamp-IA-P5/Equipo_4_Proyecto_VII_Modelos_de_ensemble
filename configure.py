from pathlib import Path

# __file__ es este archivo (src/configure.py)
# .parent es la carpeta 'src'
# .parent.parent es la RAÍZ del proyecto (la carpeta Equipo_4_...)
PROJECT_ROOT = Path(__file__).parent

# Esta es la ruta correcta a tus datos
RAW_DATA = PROJECT_ROOT / "datasets"

# El resto de rutas 
DATA_DIR = PROJECT_ROOT / "data"
MODELS_DIR = PROJECT_ROOT / "models"
RESULT_DIR = PROJECT_ROOT / "results"
NOTEBOOK_DIR = PROJECT_ROOT / "notebooks"
SRC_DIR = PROJECT_ROOT / "src"