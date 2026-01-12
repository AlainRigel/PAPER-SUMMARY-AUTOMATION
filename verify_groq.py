"""
Script de verificación rápida de Groq.
"""
import os
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("GROQ_API_KEY")

print("🔍 Verificación de Groq\n")
print("="*50)

if api_key:
    masked = api_key[:7] + "..." + api_key[-4:]
    print(f"✓ GROQ_API_KEY encontrada: {masked}")
    print(f"✓ Longitud: {len(api_key)} caracteres")
    
    if api_key.startswith("gsk_"):
        print("✓ Formato correcto (empieza con 'gsk_')")
    else:
        print("⚠ Advertencia: debería empezar con 'gsk_'")
else:
    print("✗ GROQ_API_KEY NO encontrada")
    print("\nVerifica que .env contiene:")
    print("GROQ_API_KEY=gsk_tu_key_aqui")

print("="*50)
