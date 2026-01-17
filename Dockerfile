FROM python:3.11-slim

WORKDIR /app

# Sistema y librerías base (casi nunca cambia)
RUN apt-get update && apt-get install -y --no-install-recommends \
    git && \
    rm -rf /var/lib/apt/lists/*

# Librerías de visualización y OpenGL (separadas para fácil modificación)
RUN apt-get update && apt-get install -y --no-install-recommends \
    libsm6 libxext6 libxrender-dev libgl1 libglvnd0 && \
    rm -rf /var/lib/apt/lists/*

# FastAPI y Uvicorn
RUN pip install --no-cache-dir fastapi uvicorn python-multipart

# Pillow y Requests
RUN pip install --no-cache-dir pillow requests

# PyTorch (pesado, separado)
RUN pip install --no-cache-dir torch torchvision

# Ultralytics YOLO
RUN pip install --no-cache-dir ultralytics

COPY src/main.py .

EXPOSE 8000
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]