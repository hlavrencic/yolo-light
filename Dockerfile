# Build para desarrollo local (x86_64)
# En RPi4, usar: arm64v8/python:3.11-slim-bullseye
FROM python:3.11-slim-bullseye AS base

# Instalar dependencias necesarias mínimas
RUN apt-get update && apt-get install -y --no-install-recommends \
    libgl1-mesa-glx \
    libglib2.0-0 \
    gcc \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copiar requirements y instalar con optimizaciones
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip setuptools wheel && \
    pip install --no-cache-dir -r requirements.txt

# Copiar código fuente
COPY src/ .

# Crear directorio para modelos (que puede ser un volumen)
RUN mkdir -p /app/models

# Usuario no-root por seguridad
RUN useradd -m -u 1000 yolo
USER yolo

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=40s --retries=3 \
    CMD python -c "import requests; requests.get('http://localhost:8000/health')" || exit 1

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]