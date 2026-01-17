FROM python:3.11-slim

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    libsm6 libxext6 libxrender-dev libgl1-mesa-glx git && \
    rm -rf /var/lib/apt/lists/*

# Instalar deps mínimas
RUN pip install --no-cache-dir fastapi uvicorn pillow requests

# Instalar torch y ultralytics (esto tardará)
RUN pip install --no-cache-dir torch torchvision ultralytics

COPY src/main.py .

EXPOSE 8000
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]