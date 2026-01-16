from fastapi import FastAPI, File, UploadFile
from fastapi.responses import JSONResponse
import io
import os
import sys
import subprocess
from PIL import Image
import logging
import time
import numpy as np

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="YOLO Light API - RPi4 Optimized", version="1.0.0")

interpreter = None

@app.on_event("startup")
async def load_model():
    global interpreter
    try:
        import tensorflow as tf
        
        # Cargar modelo TFLite (mucho más ligero para RPi4)
        model_path = "yolo11n_float16.tflite"
        if not os.path.exists(model_path):
            logger.warning(f"Modelo {model_path} no encontrado!")
            return
        
        interpreter = tf.lite.Interpreter(model_path=model_path)
        interpreter.allocate_tensors()
        logger.info("✓ Modelo TFLite cargado correctamente")
    except ImportError:
        logger.info("TensorFlow no disponible, intentando PyTorch...")
        try:
            from ultralytics import YOLO
            global model
            model = YOLO("yolo11n.pt")
            model(Image.new('RGB', (640, 640)))
            logger.info("✓ Modelo YOLO cargado correctamente")
        except Exception as e:
            logger.error(f"Error cargando modelo: {e}")
            raise
    except Exception as e:
        logger.error(f"Error con TFLite: {e}")
        raise

@app.get("/health")
async def health_check():
    return {"status": "healthy", "model": "YOLO11n"}

@app.get("/")
async def root():
    return {
        "name": "YOLO Light API",
        "version": "1.0.0",
        "description": "API liviana para detección de objetos en RPi4",
        "endpoints": {
            "POST /detect": "Enviar foto para detectar objetos",
            "GET /health": "Estado de la API"
        }
    }

@app.post("/detect")
async def detect_objects(file: UploadFile = File(...)):
    try:
        if interpreter is None:
            return JSONResponse(status_code=503, content={"error": "Modelo no disponible"})
        
        if not file.content_type.startswith("image/"):
            return JSONResponse(status_code=400, content={"error": "Debe ser una imagen"})
        
        start_time = time.time()
        image_bytes = await file.read()
        img = Image.open(io.BytesIO(image_bytes)).convert('RGB')
        
        # Redimensionar a 640x640 (entrada del modelo YOLO)
        img_resized = img.resize((640, 640))
        img_array = np.array(img_resized, dtype=np.float32) / 255.0
        
        # Preparar entrada
        input_details = interpreter.get_input_details()
        output_details = interpreter.get_output_details()
        
        interpreter.set_tensor(input_details[0]['index'], np.expand_dims(img_array, 0))
        interpreter.invoke()
        
        # Obtener predicciones
        predictions = interpreter.get_tensor(output_details[0]['index'])
        
        # Parsear predicciones y retornar
        detections = parse_yolo_predictions(predictions)
        inference_time = time.time() - start_time
        
        return {
            "success": True,
            "count": len(detections),
            "inference_time_ms": round(inference_time * 1000, 2),
            "objects": detections
        }
    
    except Exception as e:
        logger.error(f"Error: {e}")
        return JSONResponse(status_code=500, content={"error": str(e)})

def parse_yolo_predictions(predictions):
    """Parse YOLO output format"""
    detections = []
    # predictions shape: (1, 25200, 85) para YOLOv8
    # Format: [x, y, w, h, conf, class_probs...]
    
    CONF_THRESHOLD = 0.4
    pred = predictions[0]
    
    coco_classes = [
        'person', 'bicycle', 'car', 'motorcycle', 'airplane', 'bus', 'train', 'truck',
        'boat', 'traffic light', 'fire hydrant', 'stop sign', 'parking meter', 'bench',
        'cat', 'dog', 'horse', 'sheep', 'cow', 'elephant', 'bear', 'zebra', 'giraffe',
        'backpack', 'umbrella', 'handbag', 'tie', 'suitcase', 'frisbee', 'skis',
        'snowboard', 'sports ball', 'kite', 'baseball bat', 'baseball glove', 'skateboard',
        'surfboard', 'tennis racket', 'bottle', 'wine glass', 'cup', 'fork', 'knife',
        'spoon', 'bowl', 'banana', 'apple', 'sandwich', 'orange', 'broccoli', 'carrot',
        'hot dog', 'pizza', 'donut', 'cake', 'chair', 'couch', 'potted plant', 'bed',
        'dining table', 'toilet', 'tv', 'laptop', 'mouse', 'remote', 'keyboard', 'microwave',
        'oven', 'toaster', 'sink', 'refrigerator', 'book', 'clock', 'vase', 'scissors',
        'teddy bear', 'hair drier', 'toothbrush'
    ]
    
    for i, detection in enumerate(pred):
        x, y, w, h = detection[:4]
        conf = detection[4]
        
        if conf > CONF_THRESHOLD:
            class_probs = detection[5:]
            class_id = np.argmax(class_probs)
            class_conf = float(class_probs[class_id])
            
            detections.append({
                "id": i + 1,
                "class": coco_classes[int(class_id)] if class_id < len(coco_classes) else f"class_{class_id}",
                "confidence": round(float(class_conf), 3),
                "bbox": {
                    "x": round(float(x), 2),
                    "y": round(float(y), 2),
                    "width": round(float(w), 2),
                    "height": round(float(h), 2)
                }
            })
    
    return detections[:10]  # Limitar a top 10 detecciones
