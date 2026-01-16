FROM python:3.9-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# Actualización de dependencias para Debian Trixie/Bookworm
RUN apt-get update && apt-get install -y --no-install-recommends \
    libgl1 \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

# CORRECCIÓN DE NUMPY (Para evitar el error de TFLite con NumPy 2.0)
RUN pip install --no-cache-dir "numpy>=1.23.5,<2.0.0"

# Instalación de librerías de Python
RUN pip install --no-cache-dir \
    tflite-runtime \
    fastapi \
    uvicorn \
    Pillow \
    python-multipart

COPY . .

EXPOSE 8000

CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]