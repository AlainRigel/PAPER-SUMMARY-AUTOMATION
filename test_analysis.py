"""
Script simple para probar el endpoint de análisis.
"""
import requests

print("🔍 Probando endpoint /api/analyze...\n")

# Verificar health
response = requests.get("http://127.0.0.1:8000/api/health")
print(f"Health check: {response.json()}\n")

# Probar con un PDF de ejemplo
import sys
from pathlib import Path

if len(sys.argv) > 1:
    pdf_path = Path(sys.argv[1])
    
    if pdf_path.exists():
        print(f"Analizando: {pdf_path.name}")
        
        with open(pdf_path, 'rb') as f:
            files = {'file': (pdf_path.name, f, 'application/pdf')}
            response = requests.post(
                "http://127.0.0.1:8000/api/analyze",
                files=files,
                timeout=60
            )
        
        if response.status_code == 200:
            data = response.json()
            print(f"\n✓ Análisis exitoso!")
            print(f"\nPaper title: {data.get('paper', {}).get('title', 'N/A')}")
            
            # Verificar si hay análisis
            if 'analysis' in data:
                analysis = data['analysis']
                print(f"\n📊 Análisis NLP:")
                print(f"  - Technical summary: {'✓' if analysis.get('technical_summary') else '✗'}")
                print(f"  - Contributions: {len(analysis.get('main_contributions', []))} encontradas")
                print(f"  - Key concepts: {len(analysis.get('key_concepts', {}))} encontrados")
                print(f"  - Methodology: {'✓' if analysis.get('methodology') else '✗'}")
                print(f"  - Limitations: {len(analysis.get('limitations', []))} encontradas")
                print(f"  - Thematic tags: {len(analysis.get('thematic_tags', []))} tags")
                
                # Mostrar contribuciones
                if analysis.get('main_contributions'):
                    print(f"\n🎯 Contribuciones:")
                    for i, contrib in enumerate(analysis['main_contributions'], 1):
                        print(f"  {i}. {contrib[:100]}...")
                
                # Mostrar conceptos
                if analysis.get('key_concepts'):
                    print(f"\n💡 Conceptos clave:")
                    for concept in list(analysis['key_concepts'].keys())[:5]:
                        print(f"  - {concept}")
            else:
                print("\n⚠ No se encontró 'analysis' en la respuesta")
                print(f"Keys en respuesta: {list(data.keys())}")
        else:
            print(f"\n✗ Error {response.status_code}")
            print(response.text[:500])
    else:
        print(f"✗ Archivo no encontrado: {pdf_path}")
else:
    print("Uso: python test_analysis.py path/to/paper.pdf")
