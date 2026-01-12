"""
Script de diagnóstico para verificar la configuración de DeepSeek.
"""
import os
from pathlib import Path

print("🔍 Diagnóstico de Configuración DeepSeek\n")
print("="*60)

# 1. Verificar archivo .env
env_file = Path(".env")
print(f"\n1. Archivo .env:")
if env_file.exists():
    print(f"   ✓ Existe: {env_file.absolute()}")
    with open(env_file, 'r') as f:
        content = f.read()
        if 'DEEPSEEK_API_KEY' in content:
            print("   ✓ Contiene DEEPSEEK_API_KEY")
        else:
            print("   ✗ No contiene DEEPSEEK_API_KEY")
else:
    print(f"   ✗ No existe")

# 2. Verificar variable de entorno
print(f"\n2. Variable de entorno:")
api_key = os.getenv("DEEPSEEK_API_KEY")
if api_key:
    # Ocultar la key real
    masked_key = api_key[:7] + "..." + api_key[-4:] if len(api_key) > 11 else "***"
    print(f"   ✓ DEEPSEEK_API_KEY encontrada: {masked_key}")
    
    # Verificar si es el placeholder
    if api_key == "your_deepseek_api_key_here":
        print("   ⚠ ADVERTENCIA: Usando placeholder, no una key real")
        print("   → Necesitas reemplazarla con tu key de DeepSeek")
    elif not api_key.startswith("sk-"):
        print("   ⚠ ADVERTENCIA: La key no parece válida (debería empezar con 'sk-')")
    else:
        print("   ✓ Formato de key parece correcto")
else:
    print("   ✗ DEEPSEEK_API_KEY no encontrada")
    print("   → Asegúrate de que el archivo .env contiene:")
    print("      DEEPSEEK_API_KEY=sk-tu-key-aqui")

# 3. Verificar python-dotenv
print(f"\n3. Librería python-dotenv:")
try:
    import dotenv
    print("   ✓ python-dotenv instalado")
    
    # Intentar cargar .env
    from dotenv import load_dotenv
    load_dotenv()
    
    api_key_after_load = os.getenv("DEEPSEEK_API_KEY")
    if api_key_after_load:
        masked = api_key_after_load[:7] + "..." + api_key_after_load[-4:] if len(api_key_after_load) > 11 else "***"
        print(f"   ✓ .env cargado correctamente: {masked}")
    else:
        print("   ✗ .env no se cargó correctamente")
        
except ImportError:
    print("   ✗ python-dotenv NO instalado")
    print("   → Instalar con: pip install python-dotenv")

# 4. Verificar openai library
print(f"\n4. Librería openai:")
try:
    import openai
    print(f"   ✓ openai instalado (versión: {openai.__version__})")
except ImportError:
    print("   ✗ openai NO instalado")
    print("   → Instalar con: pip install openai")

# 5. Probar inicialización de DeepSeekAnalyzer
print(f"\n5. Inicialización de DeepSeekAnalyzer:")
try:
    from src.analysis.llm_analyzer import DeepSeekAnalyzer
    
    # Cargar .env primero
    from dotenv import load_dotenv
    load_dotenv()
    
    api_key = os.getenv("DEEPSEEK_API_KEY")
    if api_key and api_key != "your_deepseek_api_key_here":
        analyzer = DeepSeekAnalyzer(api_key=api_key)
        print("   ✓ DeepSeekAnalyzer inicializado correctamente")
    else:
        print("   ⚠ No se puede inicializar: API key no configurada")
        
except Exception as e:
    print(f"   ✗ Error al inicializar: {e}")

print("\n" + "="*60)
print("\n📋 Resumen:")

if not env_file.exists():
    print("❌ Crear archivo .env con tu API key")
elif api_key == "your_deepseek_api_key_here" or not api_key:
    print("❌ Editar .env y poner tu API key real de DeepSeek")
    print("   Obtener en: https://platform.deepseek.com/api_keys")
else:
    print("✅ Configuración parece correcta")
    print("   Reinicia el servidor: python app.py")

print()
