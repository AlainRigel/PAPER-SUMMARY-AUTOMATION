# 🚀 Guía Rápida: Integración con DeepSeek LLM

## ✨ ¿Qué es DeepSeek?

DeepSeek es un LLM (Large Language Model) de alta calidad que ofrece:
- **Análisis inteligente** de papers científicos
- **Mejor precisión** que métodos basados en patrones
- **Costo reducido** comparado con OpenAI
- **API compatible** con OpenAI SDK

---

## 📋 Paso 1: Obtener API Key

1. **Visita**: https://platform.deepseek.com/
2. **Regístrate** o inicia sesión
3. **Ve a API Keys**: https://platform.deepseek.com/api_keys
4. **Crea una nueva API key**
5. **Copia la key** (la necesitarás en el siguiente paso)

---

## ⚙️ Paso 2: Configurar la API Key

### Opción A: Archivo .env (Recomendado)

1. **Copia el archivo de ejemplo**:
   ```bash
   copy .env.example .env
   ```

2. **Edita `.env`** y agrega tu API key:
   ```bash
   DEEPSEEK_API_KEY=sk-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
   ```

3. **Guarda el archivo**

### Opción B: Variable de Entorno

**Windows (PowerShell)**:
```powershell
$env:DEEPSEEK_API_KEY="sk-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
```

**Windows (CMD)**:
```cmd
set DEEPSEEK_API_KEY=sk-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
```

**Linux/Mac**:
```bash
export DEEPSEEK_API_KEY="sk-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
```

---

## 🧪 Paso 3: Probar la Integración

### Reiniciar el Servidor

```bash
# Detener el servidor actual (Ctrl+C)
# Luego reiniciar:
python app.py
```

Deberías ver:
```
✓ DeepSeek LLM initialized
INFO:     Uvicorn running on http://127.0.0.1:8000
```

### Analizar un Paper

1. **Abre** http://127.0.0.1:8000
2. **Sube un PDF**
3. **Observa en la consola del servidor**:
   ```
   🤖 Using DeepSeek LLM for analysis...
   ```

---

## 📊 Diferencias: LLM vs NLP vs Templates

| Característica | LLM (DeepSeek) | NLP (spaCy) | Templates |
|---------------|----------------|-------------|-----------|
| **Precisión** | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐ |
| **Velocidad** | ⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ |
| **Costo** | 💰 (~$0.001/paper) | Gratis | Gratis |
| **Comprensión** | Contextual | Patrones | Básico |
| **Contribuciones** | Precisas | Aproximadas | Genéricas |
| **Limitaciones** | Detecta reales | Aproximadas | No detecta |
| **Conceptos** | Con definiciones | Solo nombres | No extrae |

---

## 💡 Ejemplo de Análisis

### Con Templates (sin LLM):
```json
{
  "main_contributions": [
    "Contribution extraction requires LLM-based analysis"
  ],
  "key_concepts": {
    "Concept Extraction": "Requires NER and semantic analysis"
  }
}
```

### Con DeepSeek LLM:
```json
{
  "main_contributions": [
    "Novel CNN architecture for speech recognition achieving 95% accuracy",
    "Efficient training method reducing computation by 40%",
    "New dataset with 10,000 hours of annotated speech"
  ],
  "key_concepts": {
    "Convolutional Neural Network": "Deep learning architecture using convolutional layers for feature extraction",
    "Acoustic Modeling": "Process of representing relationship between audio signals and phonetic units",
    "TIMIT Dataset": "Standard corpus for speech recognition containing 630 speakers"
  },
  "limitations": [
    "Model requires significant GPU memory (16GB minimum)",
    "Performance degrades with noisy audio environments",
    "Limited to English language only"
  ]
}
```

---

## 🔧 Solución de Problemas

### Problema: "DEEPSEEK_API_KEY not found"

**Solución**:
1. Verifica que el archivo `.env` existe
2. Verifica que la key está correctamente escrita
3. Reinicia el servidor

### Problema: "LLM analysis failed"

**Posibles causas**:
1. **API key inválida**: Verifica en https://platform.deepseek.com/
2. **Sin créditos**: Recarga tu cuenta
3. **Conexión a internet**: Verifica tu conexión
4. **Rate limit**: Espera unos segundos y reintenta

**El sistema automáticamente hará fallback a NLP si LLM falla**.

### Problema: Análisis muy lento

**Solución**:
- DeepSeek tarda ~5-10 segundos por paper
- Esto es normal para análisis de calidad
- Si necesitas velocidad, desactiva LLM:
  ```python
  analyzer = AcademicAnalyzer(use_llm=False, use_nlp=True)
  ```

---

## 💰 Costos Estimados

DeepSeek es muy económico:

| Operación | Tokens | Costo |
|-----------|--------|-------|
| Paper corto (4 páginas) | ~2,000 | $0.0003 |
| Paper medio (8 páginas) | ~4,000 | $0.0006 |
| Paper largo (12 páginas) | ~6,000 | $0.0009 |

**Ejemplo**: Analizar 1,000 papers = ~$0.60 USD

---

## 🎯 Mejores Prácticas

1. **Usa LLM para análisis final** - Mayor calidad
2. **Usa NLP para pruebas rápidas** - Sin costo
3. **Monitorea tu uso** en https://platform.deepseek.com/usage
4. **Establece límites** de gasto si es necesario

---

## 📚 Recursos

- **DeepSeek Platform**: https://platform.deepseek.com/
- **Documentación API**: https://platform.deepseek.com/api-docs/
- **Pricing**: https://platform.deepseek.com/pricing
- **Discord Community**: https://discord.gg/deepseek

---

## ✅ Checklist de Configuración

- [ ] Cuenta creada en DeepSeek
- [ ] API key obtenida
- [ ] Archivo `.env` configurado
- [ ] Servidor reiniciado
- [ ] Mensaje "✓ DeepSeek LLM initialized" visible
- [ ] Paper de prueba analizado exitosamente

---

**¡Listo! Ahora tienes análisis inteligente de papers con DeepSeek LLM.** 🎉
