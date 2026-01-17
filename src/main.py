from fastapi import FastAPI, File, UploadFile
from fastapi.responses import JSONResponse
from ultralytics import YOLO
import io
import logging
import time
import os
from PIL import Image

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="YOLO Light API", version="1.0.0")

# Variable global para el modelo
model = None
model_name = os.getenv("MODEL_NAME", "yolov5n.pt")

@app.on_event("startup")
async def startup():
    """Cargar modelo YOLO en startup"""
    global model, model_name
    try:
        logger.info("🚀 Iniciando YOLO Light API...")
        logger.info(f"📦 Cargando modelo: {model_name}...")
        
        # Cargar modelo YOLO (se descarga automáticamente si no existe)
        model = YOLO(model_name)
        
        logger.info(f"✅ Modelo {model_name} cargado correctamente")
        logger.info("📊 API lista para detección de objetos")
        
    except Exception as e:
        logger.error(f"❌ Error al cargar modelo: {e}")
        raise

@app.get("/health")
async def health_check():
    """Health check endpoint - muestra estado del modelo"""
    try:
        model_status = "loaded" if model is not None else "not_loaded"
        model_ready = model is not None and hasattr(model, 'names')
        
        return {
            "status": "healthy" if model_ready else "unhealthy",
            "model": model_name,
            "model_status": model_status,
            "model_ready": model_ready,
            "version": "1.0.0",
            "classes": len(model.names) if model_ready else 0
        }
    except Exception as e:
        logger.error(f"Error en health check: {e}")
        return {
            "status": "unhealthy",
            "model": model_name,
            "model_status": "error",
            "model_ready": False,
            "error": str(e)
        }

@app.get("/")
async def root():
    """API info endpoint"""
    return {
        "name": "YOLO Light API",
        "version": "1.0.0",
        "description": "Lightweight YOLO object detection API for RPi4",
        "model": model_name,
        "model_classes": len(model.names) if model is not None else 80,
        "endpoints": {
            "POST /detect": "Detectar objetos en imagen",
            "GET /health": "Verificar estado de API",
            "GET /": "Información de API"
        }
    }

@app.post("/detect")
async def detect_objects(file: UploadFile = File(...)):
    """
    Detectar objetos en imagen usando YOLOv5n
    
    Args:
        file: Archivo de imagen (JPG, PNG, etc)
    
    Returns:
        JSON con objetos detectados, confianza y bounding boxes
    """
    try:
        # Validar tipo de archivo
        if not file.content_type or not file.content_type.startswith("image/"):
            logger.warning(f"Invalid content type: {file.content_type}")
            return JSONResponse(
                status_code=400,
                content={
                    "success": False,
                    "error": "El archivo debe ser una imagen (JPG, PNG, etc)"
                }
            )
        
        # Leer imagen
        logger.info(f"Procesando archivo: {file.filename}")
        start_time = time.time()
        
        image_bytes = await file.read()
        img = Image.open(io.BytesIO(image_bytes)).convert('RGB')
        
        logger.info(f"Imagen cargada: {img.size}")
        
        # Inferencia con YOLOv5n
        inference_start = time.time()
        results = model(img, conf=0.4, verbose=False)
        inference_time = (time.time() - inference_start) * 1000
        
        # Procesar resultados
        objects = []
        detections = results[0]
        
        if detections.boxes is not None:
            for box_data in detections.boxes:
                # Extraer coordenadas
                xyxy = box_data.xyxy[0].tolist()
                x1, y1, x2, y2 = xyxy
                
                # Confianza
                conf = float(box_data.conf[0])
                
                # Clase
                cls_idx = int(box_data.cls[0])
                class_name = detections.names.get(cls_idx, f"unknown_{cls_idx}")
                
                # Crear objeto de detección
                objects.append({
                    "class": class_name,
                    "confidence": round(conf, 3),
                    "bbox": {
                        "x1": round(x1),
                        "y1": round(y1),
                        "x2": round(x2),
                        "y2": round(y2)
                    }
                })
        
        # Ordenar por confianza (descendente)
        objects.sort(key=lambda x: x['confidence'], reverse=True)
        
        total_time = (time.time() - start_time) * 1000
        
        logger.info(f"✅ Detección completada: {len(objects)} objetos en {inference_time:.1f}ms")
        
        return {
            "success": True,
            "count": len(objects),
            "inference_time_ms": round(inference_time, 1),
            "total_time_ms": round(total_time, 1),
            "model": model_name,
            "image_size": list(img.size),
            "objects": objects
        }
    
    except Exception as e:
        logger.error(f"❌ Error en detección: {e}", exc_info=True)
        return JSONResponse(
            status_code=500,
            content={
                "success": False,
                "error": f"Error en detección: {str(e)}"
            }
        )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
