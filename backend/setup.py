from setuptools import setup, find_packages
from pathlib import Path

# Leer requirements.txt
def read_requirements(filename):
    requirements_path = Path(__file__).parent / filename
    with open(requirements_path, encoding='utf-8') as f:
        return [
            line.strip() 
            for line in f 
            if line.strip() and not line.startswith('#')
        ]

setup(
    name="equipo4-ml-project",
    version="0.1.0",
    description="Proyecto de clasificación multiclase con modelos de ensemble",
    author="Equipo 4",
    packages=find_packages(),
    py_modules=["configure"],  # Incluir configure.py de la raíz
    python_requires=">=3.8",
    install_requires=read_requirements('requirements.txt'),
    extras_require={
        "dev": [
            "pytest>=7.0.0",
            "black>=22.0.0",
            "flake8>=5.0.0",
        ]
    },
)
