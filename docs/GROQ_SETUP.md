# 🚀 Guía Rápida: Integración con Groq LLM

## ✨ ¿Qué es Groq?

Groq es una plataforma de inferencia ultra-rápida que permite correr LLMs (como Llama 3) a velocidades inigualables.
- **Velocidad Excepcional**: Inferencia casi instantánea (~300 tokens/seg)
- **Calidad SOTA**: Usa **Llama 3.3 70B**, uno de los mejores modelos open-source
- **Costo**: Actualmente ofrece un tier gratuito muy generoso
- **API Compatible**: Compatible con OpenAI SDK (con ajustes mínimos)

---

## 📋 Paso 1: Obtener API Key

1. **Visita**: https://console.groq.com/
2. **Regístrate** o inicia sesión
3. **Ve a API Keys**: https://console.groq.com/keys
4. **Crea una nueva API key**
5. **Copia la key** (empieza con `gsk_`)

---

## ⚙️ Paso 2: Configurar la API Key

### Opción A: Archivo .env (Recomendado)

1. **Edita tu archivo `.env`** en la raíz del proyecto:
   ```bash
   # Groq API Configuration
   GROQ_API_KEY=gsk_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
   ```

2. **Guarda el archivo**

### Opción B: Variable de Entorno

**Windows (PowerShell)**:
```powershell
$env:GROQ_API_KEY="gsk_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
```

**Linux/Mac**:
```bash
export GROQ_API_KEY="gsk_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
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
✓ Groq LLM initialized (Llama 3.1 70B)
INFO:     Uvicorn running on http://127.0.0.1:8000
```

### Analizar un Paper

1. **Abre** http://127.0.0.1:8000
2. **Sube un PDF**
3. **Observa en la consola del servidor**:
   ```
   🤖 Using Groq LLM for analysis...
   ```

---

## 📊 Diferencias: Groq vs Otros (DeepSeek, OpenAI)

| Característica | Groq (Llama 3.3) | DeepSeek | OpenAI (GPT-4) |
|---------------|------------------|----------|----------------|
| **Velocidad** | ⚡⚡⚡⚡⚡ (Instantáneo) | ⚡⚡ (Normal) | ⚡⚡ (Lento) |
| **Costo** | 💰 Gratis (Beta) | 💰 Muy barato | 💰💰💰 Caro |
| **Calidad** | ⭐⭐⭐⭐⭐ (Excelente) | ⭐⭐⭐⭐⭐ (Excelente) | ⭐⭐⭐⭐⭐ (Top) |
| **Modelo** | Llama 3.3 70B | DeepSeek Chat | GPT-4o |
| **Uso Ideal** | Análisis en tiempo real | Batch processing | Tareas complejas |

---

## 💡 Ejemplo de Análisis con Groq

El sistema extraerá automáticamente:

```json
{
  "main_contributions": [
    "Novel transformer architecture optimization reducing latency by 40%",
    "New dataset 'MediCorpus' with 50k annotated clinical reports",
    "State-of-the-art results on BioNLP benchmark"
  ],
  "key_concepts": {
    "Attention Mechanism": "Neural network component that weighs the importance of different input elements...",
    "Zero-shot Learning": "Ability of a model to perform tasks without specific training examples..."
  },
  "limitations": [
    "Study limitation: Small sample size (n=50)",
    "Computational constraint: Requires H100 GPU for training"
  ]
}
```

---

## 🔧 Solución de Problemas

### Problema: "GROQ_API_KEY not found"

**Solución**:
1. Verifica que el archivo `.env` existe en `d:\GITHUB\Paper-collector\.env`
2. Verifica que `GROQ_API_KEY` está escrito correctamente
3. **Reinicia el servidor** (`python app.py`)

### Problema: "Model decommissioned"

**Causa**: Groq actualiza sus modelos frecuentemente.
**Solución**:
- El código usa `llama-3.3-70b-versatile` (versión estable actual).
- Si falla, verifica https://console.groq.com/docs/models para ver el nombre más reciente.

### Problema: "Rate limit reached"

**Solución**:
- Groq tiene límites por minuto generosos pero existentes.
- Espera un minuto y reintenta.
- El sistema hará fallback a NLP tradicional si falla.

---

## 📚 Recursos

- **Groq Console**: https://console.groq.com/
- **Modelos Disponibles**: https://console.groq.com/docs/models
- **Estado del Servicio**: https://status.groq.com/

---

**¡Listo! Disfruta de la velocidad de Groq.** 🚀
