import numpy as np
from PIL import Image
import tflite_runtime.interpreter as tflite
from fastapi import FastAPI, File, UploadFile

app = FastAPI()

# Configuración del modelo (debes tener el archivo .tflite en la carpeta)
MODEL_PATH = "yolo11n_float16.tflite"
interpreter = tflite.Interpreter(model_path=MODEL_PATH)
interpreter.allocate_tensors()

input_details = interpreter.get_input_details()
output_details = interpreter.get_output_details()

@app.post("/predict")
async def predict(file: UploadFile = File(...)):
    # 1. Leer y redimensionar imagen
    image = Image.open(file.file).convert('RGB').resize((640, 640))
    input_data = np.expand_dims(np.array(image) / 255.0, axis=0).astype(np.float32)

    # 2. Inferencia
    interpreter.set_tensor(input_details[0]['index'], input_data)
    interpreter.invoke()
    
    # 3. Obtener resultados (simplificado)
    output = interpreter.get_tensor(output_details[0]['index'])
    
    return {"status": "success", "raw_output_shape": str(output.shape)}