# Multi-stage build para YOLO Light con YOLOv5n
FROM python:3.11-slim-bullseye AS base

# Instalar dependencias del sistema necesarias para PyTorch y OpenCV
RUN apt-get update && apt-get install -y --no-install-recommends \
    libsm6 \
    libxext6 \
    libxrender-dev \
    libgomp1 \
    libgl1-mesa-glx \
    libglib2.0-0 \
    gcc \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copiar requirements e instalar dependencias
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip setuptools wheel && \
    pip install --no-cache-dir -r requirements.txt

# Pre-descargar modelo YOLOv5n (opcional pero recomendado)
# Esto hace que la imagen sea más grande pero más rápida en startup
RUN python -c "from ultralytics import YOLO; YOLO('yolov5n.pt')" || echo "Modelo será descargado en startup"

# Copiar código fuente
COPY src/main.py .

# Crear directorio para caché de modelos
# Create cache directory for models
RUN mkdir -p /root/.cache/ultralytics

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=15s --retries=3 \
    CMD python -c "import requests; requests.get('http://localhost:8000/health', timeout=5)" || exit 1

# Expose port
EXPOSE 8000

# Run API
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]

# Exponer puerto
EXPOSE 8000

# Ejecutar API
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
    CMD python -c "import requests; requests.get('http://localhost:8000/health')" || exit 1

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]