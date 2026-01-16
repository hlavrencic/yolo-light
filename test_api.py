#!/usr/bin/env python3
"""
Script para probar la API YOLO Light localmente
"""
import requests
import sys
from pathlib import Path

API_URL = "http://localhost:8000"

def test_health():
    """Verificar que la API está funcionando"""
    try:
        response = requests.get(f"{API_URL}/health")
        print(f"✓ Health check: {response.json()}")
        return True
    except Exception as e:
        print(f"✗ API no disponible: {e}")
        return False

def test_detect(image_path):
    """Enviar una imagen y obtener detecciones"""
    if not Path(image_path).exists():
        print(f"✗ Archivo no encontrado: {image_path}")
        return
    
    try:
        with open(image_path, 'rb') as f:
            files = {'file': f}
            response = requests.post(f"{API_URL}/detect", files=files)
        
        if response.status_code == 200:
            result = response.json()
            print(f"\n✓ Detección completada en {result['inference_time_ms']}ms")
            print(f"  Objetos detectados: {result['count']}")
            
            for obj in result['objects']:
                print(f"  - {obj['class']} (confianza: {obj['confidence']})")
        else:
            print(f"✗ Error: {response.status_code} - {response.text}")
    
    except Exception as e:
        print(f"✗ Error en detección: {e}")

def main():
    print("🚀 Test YOLO Light API\n")
    
    if not test_health():
        print("\n⚠️  Asegúrate de que la API esté corriendo:")
        print("   docker run -p 8000:8000 yolo-light:latest")
        return
    
    # Probar con imágenes de testing
    test_images = [
        "testing/foto.jpg",
        "testing/habitacion.jpg"
    ]
    
    for img in test_images:
        if Path(img).exists():
            print(f"\nProbando: {img}")
            test_detect(img)

if __name__ == "__main__":
    main()
