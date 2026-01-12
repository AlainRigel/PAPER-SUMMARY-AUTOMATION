"""
Script de diagnóstico para verificar el servidor.
"""
import requests
import json
from pathlib import Path

print("🔍 Diagnóstico del Servidor\n")

# 1. Verificar que el servidor está corriendo
print("1. Verificando servidor...")
try:
    response = requests.get("http://127.0.0.1:8000/api/health", timeout=5)
    if response.status_code == 200:
        print("   ✓ Servidor está corriendo")
        print(f"   Respuesta: {response.json()}")
    else:
        print(f"   ✗ Servidor respondió con código: {response.status_code}")
except Exception as e:
    print(f"   ✗ Error conectando al servidor: {e}")
    exit(1)

# 2. Verificar endpoint de análisis con un archivo de prueba
print("\n2. Probando endpoint /api/analyze...")

# Buscar un PDF de prueba
test_pdfs = list(Path("data").rglob("*.pdf")) if Path("data").exists() else []

if not test_pdfs:
    print("   ⚠ No se encontraron PDFs de prueba en data/")
    print("   Intenta subir un PDF manualmente en la web interface")
else:
    test_pdf = test_pdfs[0]
    print(f"   Usando: {test_pdf.name}")
    
    try:
        with open(test_pdf, 'rb') as f:
            files = {'file': (test_pdf.name, f, 'application/pdf')}
            response = requests.post(
                "http://127.0.0.1:8000/api/analyze",
                files=files,
                timeout=60
            )
        
        if response.status_code == 200:
            print("   ✓ Análisis exitoso")
            data = response.json()
            if data.get('success'):
                print(f"   Paper: {data['analysis']['paper_title']}")
            else:
                print(f"   ✗ Análisis falló: {data}")
        else:
            print(f"   ✗ Error {response.status_code}")
            print(f"   Respuesta: {response.text[:500]}")
    except Exception as e:
        print(f"   ✗ Error: {e}")

print("\n✅ Diagnóstico completado")
