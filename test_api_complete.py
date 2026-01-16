#!/usr/bin/env python3
"""
Script completo para testing de YOLO Light API
Prueba todos los endpoints y mide rendimiento
"""

import requests
import json
import time
import sys
from pathlib import Path

API_URL = "http://localhost:8000"
TIMEOUT = 30

class Colors:
    OK = '\033[92m'
    FAIL = '\033[91m'
    WARN = '\033[93m'
    INFO = '\033[94m'
    END = '\033[0m'

def print_result(test_name, success, message=""):
    symbol = f"{Colors.OK}✓{Colors.END}" if success else f"{Colors.FAIL}✗{Colors.END}"
    status = f"{Colors.OK}PASS{Colors.END}" if success else f"{Colors.FAIL}FAIL{Colors.END}"
    msg = f" - {message}" if message else ""
    print(f"{symbol} {test_name:<40} {status}{msg}")

def test_health_check():
    """Test /health endpoint"""
    print(f"\n{Colors.INFO}=== Health Check ==={Colors.END}")
    try:
        response = requests.get(f"{API_URL}/health", timeout=TIMEOUT)
        if response.status_code == 200:
            data = response.json()
            print_result("GET /health", True, f"Status: {data.get('status')}")
            print(f"  Mode: {data.get('mode')}")
            print(f"  Model: {data.get('model')}")
            print(f"  TFLite Runtime: {data.get('has_tflite_runtime', 'N/A')}")
            return True
        else:
            print_result("GET /health", False, f"Status code: {response.status_code}")
            return False
    except Exception as e:
        print_result("GET /health", False, str(e))
        return False

def test_root():
    """Test / endpoint"""
    print(f"\n{Colors.INFO}=== API Info ==={Colors.END}")
    try:
        response = requests.get(f"{API_URL}/", timeout=TIMEOUT)
        if response.status_code == 200:
            data = response.json()
            print_result("GET /", True, f"API: {data.get('name')}")
            print(f"  Version: {data.get('version')}")
            print(f"  Mode: {data.get('mode')}")
            return True
        else:
            print_result("GET /", False, f"Status code: {response.status_code}")
            return False
    except Exception as e:
        print_result("GET /", False, str(e))
        return False

def test_detect_image(image_path):
    """Test /detect endpoint with image file"""
    print(f"\n{Colors.INFO}=== Object Detection ==={Colors.END}")
    
    if not Path(image_path).exists():
        print_result(f"Detect {Path(image_path).name}", False, "Archivo no encontrado")
        return False
    
    try:
        with open(image_path, 'rb') as f:
            files = {'file': (Path(image_path).name, f, 'image/jpeg')}
            start_time = time.time()
            response = requests.post(f"{API_URL}/detect", files=files, timeout=TIMEOUT)
            elapsed = (time.time() - start_time) * 1000
        
        if response.status_code == 200:
            data = response.json()
            success = data.get('success', False)
            count = data.get('count', 0)
            inference_time = data.get('inference_time_ms', 0)
            mode = data.get('mode', 'Unknown')
            
            print_result(f"POST /detect ({Path(image_path).name})", success, 
                        f"{count} objetos, {inference_time:.2f}ms")
            
            if success and count > 0:
                print(f"  Mode: {mode}")
                print(f"  Total request time: {elapsed:.2f}ms")
                print(f"  Inference time: {inference_time:.2f}ms")
                print(f"  \n  Detecciones:")
                for obj in data.get('objects', []):
                    bbox = obj.get('bbox', {})
                    print(f"    - {obj['class']} ({obj['id']}) - Confianza: {obj['confidence']:.2%}")
                    print(f"      Bbox: ({bbox.get('x1')}, {bbox.get('y1')}) -> ({bbox.get('x2')}, {bbox.get('y2')})")
            
            return success
        else:
            print_result(f"POST /detect ({Path(image_path).name})", False, 
                        f"Status code: {response.status_code}")
            print(f"  Response: {response.text}")
            return False
            
    except Exception as e:
        print_result(f"POST /detect ({Path(image_path).name})", False, str(e))
        return False

def test_invalid_file():
    """Test /detect with invalid file"""
    print(f"\n{Colors.INFO}=== Error Handling ==={Colors.END}")
    try:
        files = {'file': ('test.txt', b'not an image', 'text/plain')}
        response = requests.post(f"{API_URL}/detect", files=files, timeout=TIMEOUT)
        
        if response.status_code == 400:
            print_result("Invalid file rejection", True, "400 Bad Request")
            return True
        else:
            print_result("Invalid file rejection", False, f"Expected 400, got {response.status_code}")
            return False
    except Exception as e:
        print_result("Invalid file rejection", False, str(e))
        return False

def test_performance(image_path, iterations=5):
    """Test performance with multiple requests"""
    print(f"\n{Colors.INFO}=== Performance Test ({iterations} iterations) ==={Colors.END}")
    
    if not Path(image_path).exists():
        print_result("Performance test", False, "Archivo no encontrado")
        return False
    
    times = []
    successful = 0
    
    try:
        with open(image_path, 'rb') as f:
            image_data = f.read()
        
        for i in range(iterations):
            files = {'file': (Path(image_path).name, image_data, 'image/jpeg')}
            start_time = time.time()
            response = requests.post(f"{API_URL}/detect", files=files, timeout=TIMEOUT)
            elapsed = (time.time() - start_time) * 1000
            
            if response.status_code == 200:
                data = response.json()
                inference_time = data.get('inference_time_ms', 0)
                times.append(inference_time)
                successful += 1
                print(f"  Iteración {i+1}: {elapsed:.2f}ms (inferencia: {inference_time:.2f}ms)")
        
        if times:
            avg_time = sum(times) / len(times)
            min_time = min(times)
            max_time = max(times)
            print_result("Performance", successful == iterations,
                        f"Avg: {avg_time:.2f}ms, Min: {min_time:.2f}ms, Max: {max_time:.2f}ms")
            return True
        else:
            print_result("Performance", False, "No respuestas válidas")
            return False
            
    except Exception as e:
        print_result("Performance", False, str(e))
        return False

def main():
    print(f"\n{Colors.INFO}╔════════════════════════════════════════════════════════╗{Colors.END}")
    print(f"{Colors.INFO}║         YOLO Light API - Test Suite                     ║{Colors.END}")
    print(f"{Colors.INFO}║         API URL: {API_URL:<35} ║{Colors.END}")
    print(f"{Colors.INFO}╚════════════════════════════════════════════════════════╝{Colors.END}")
    
    # Verificar conexión
    try:
        response = requests.get(f"{API_URL}/health", timeout=5)
        if response.status_code != 200:
            print(f"\n{Colors.FAIL}✗ API no responde en {API_URL}{Colors.END}")
            print(f"  Asegúrate que Docker está corriendo:")
            print(f"  docker run -d -p 8000:8000 --name yolo-api yolo-light:latest")
            sys.exit(1)
    except Exception as e:
        print(f"\n{Colors.FAIL}✗ Error conectando a {API_URL}{Colors.END}")
        print(f"  {str(e)}")
        print(f"  Asegúrate que Docker está corriendo:")
        print(f"  docker run -d -p 8000:8000 --name yolo-api yolo-light:latest")
        sys.exit(1)
    
    results = []
    
    # Ejecutar tests
    results.append(("health_check", test_health_check()))
    results.append(("root", test_root()))
    results.append(("invalid_file", test_invalid_file()))
    
    # Test con imágenes
    test_images = [
        "testing/foto.jpg",
        "testing/habitacion.jpg"
    ]
    
    for image in test_images:
        if Path(image).exists():
            results.append((f"detect_{Path(image).name}", test_detect_image(image)))
    
    # Performance test
    if Path("testing/foto.jpg").exists():
        results.append(("performance", test_performance("testing/foto.jpg", iterations=3)))
    
    # Resumen
    print(f"\n{Colors.INFO}=== Resumen ==={Colors.END}")
    passed = sum(1 for _, r in results if r)
    total = len(results)
    percentage = (passed / total * 100) if total > 0 else 0
    
    for test_name, result in results:
        symbol = f"{Colors.OK}✓{Colors.END}" if result else f"{Colors.FAIL}✗{Colors.END}"
        print(f"{symbol} {test_name}")
    
    print(f"\n{Colors.OK}Resultados: {passed}/{total} ({percentage:.0f}%){Colors.END}\n")
    
    if passed == total:
        print(f"{Colors.OK}✓ Todos los tests pasaron!{Colors.END}\n")
        return 0
    else:
        print(f"{Colors.FAIL}✗ Algunos tests fallaron{Colors.END}\n")
        return 1

if __name__ == "__main__":
    sys.exit(main())
