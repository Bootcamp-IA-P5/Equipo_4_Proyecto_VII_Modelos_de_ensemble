# syntax=docker/dockerfile:1.5
FROM python:3.11-slim

# Configuración del entorno Python
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

# Instalar dependencias del sistema
RUN apt-get update \
    && apt-get install -y --no-install-recommends build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copiar requirements y instalar dependencias Python
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Crear usuario no-root para seguridad
RUN useradd --create-home appuser

# Copiar el código del proyecto
COPY --chown=appuser:appuser . .

# Cambiar al usuario no-root
USER appuser

# Exponer el puerto 8000
EXPOSE 8000

# Comando para ejecutar la aplicación FastAPI
#CMD ["uvicorn", "backend.main:app", "--host", "0.0.0.0", "--port", "8000"]
