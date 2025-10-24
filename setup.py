from setuptools import setup, find_packages

setup(
    name="equipo4-ml-project",
    version="0.1.0",
    description="Proyecto de clasificación multiclase con modelos de ensemble",
    author="Equipo 4",
    packages=find_packages(),
    py_modules=["configure"],  # Incluir configure.py de la raíz
    python_requires=">=3.8",
    install_requires=[
        "pandas>=1.5.0",
        "numpy>=1.23.0",
        "scikit-learn>=1.2.0",
        "matplotlib>=3.6.0",
        "seaborn>=0.12.0",
        "jupyter>=1.0.0",
    ],
    extras_require={
        "dev": [
            "pytest>=7.0.0",
            "black>=22.0.0",
            "flake8>=5.0.0",
        ]
    },
)