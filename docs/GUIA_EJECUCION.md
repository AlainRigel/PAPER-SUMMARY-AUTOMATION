# 🚀 Guía de Ejecución Completa - Paper Collector con NLP

## 📋 Pasos para Ejecutar el Proyecto

### 1️⃣ Detener el Servidor Actual

El servidor actual está corriendo pero no tiene los cambios de NLP cargados.

**Acción**: En la terminal donde está corriendo `python app.py`:
- Presiona `Ctrl + C` para detener el servidor

---

### 2️⃣ Reiniciar el Servidor con NLP

```bash
# En la terminal:
python app.py
```

**Deberías ver**:
```
✓ NLP processor initialized
INFO:     Started server process [xxxxx]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
```

---

### 3️⃣ Abrir la Aplicación Web

1. **Abre tu navegador**
2. **Visita**: `http://localhost:8000`
3. **Verás la interfaz** de Paper Collector

---

### 4️⃣ Probar el Análisis NLP

#### Opción A: Subir un PDF desde la Web

1. Haz clic en "Choose File" o área de drag & drop
2. Selecciona un PDF de un paper científico
3. Haz clic en "Analyze Paper"
4. **Verás el análisis completo con NLP**:
   - ✅ Entidades científicas extraídas
   - ✅ Técnicas y métodos identificados
   - ✅ Métricas de evaluación
   - ✅ Contribuciones principales
   - ✅ Limitaciones
   - ✅ Conceptos clave
   - ✅ Tags temáticos

#### Opción B: Probar con CLI

```bash
# Analizar un PDF con NLP
python -m src.analyze path/to/paper.pdf

# O usar el demo completo
python examples/nlp_analysis_demo.py path/to/paper.pdf
```

#### Opción C: Probar el API directamente

```bash
# Verificar que el servidor está corriendo
curl http://localhost:8000/api/health

# Analizar un PDF
curl -X POST "http://localhost:8000/api/analyze" \
  -F "file=@path/to/paper.pdf"
```

---

## 🎯 Características Disponibles

### En la Web Interface (http://localhost:8000)

✅ **Subir PDF** - Drag & drop o selección de archivo
✅ **Análisis Automático** - Parsing + Análisis NLP
✅ **Visualización de Resultados**:
- Información del paper
- Secciones identificadas
- Análisis académico completo
- Entidades científicas
- Contribuciones y limitaciones
- Conceptos clave

### Endpoints API Disponibles

| Endpoint | Método | Descripción |
|----------|--------|-------------|
| `/` | GET | Interfaz web principal |
| `/api/health` | GET | Health check |
| `/api/upload` | POST | Solo parsear PDF |
| `/api/analyze` | POST | **Análisis completo con NLP** ⭐ |

---

## 🧪 Verificar que NLP está Funcionando

### Método 1: Observar la Consola del Servidor

Cuando subes un PDF, deberías ver en la terminal:

```
✓ NLP processor initialized
INFO:     127.0.0.1:xxxxx - "POST /api/analyze HTTP/1.1" 200 OK
```

### Método 2: Inspeccionar la Respuesta JSON

1. Abre DevTools en el navegador (F12)
2. Ve a la pestaña "Network"
3. Sube un PDF
4. Busca la petición a `/api/analyze`
5. Ve la respuesta → Deberías ver:

```json
{
  "success": true,
  "analysis": {
    "methodology": {
      "techniques": ["método 1", "método 2"],  // ← Extraído con NLP
      "evaluation": "Evaluation metrics: accuracy, 95%"  // ← NER
    },
    "key_concepts": {
      "concepto1": "definición...",  // ← Extraído con NLP
      "concepto2": "definición..."
    },
    "main_contributions": [
      "Contribución extraída con análisis de discurso..."
    ]
  }
}
```

### Método 3: Ejecutar Tests

```bash
# Test de componentes NLP
python tests/test_nlp_components.py

# Test del API web (requiere servidor corriendo)
python tests/test_web_api.py path/to/paper.pdf
```

---

## 📁 Estructura del Proyecto

```
Paper-collector/
├── app.py                          ← Servidor web con NLP ⭐
├── web/
│   ├── index.html                  ← Interfaz web
│   ├── script.js                   ← Frontend
│   └── style.css                   ← Estilos
├── src/
│   ├── analysis/
│   │   ├── nlp_processor.py        ← NLP científico ⭐
│   │   ├── embeddings.py           ← Embeddings ⭐
│   │   └── academic_analyzer.py    ← Analizador mejorado ⭐
│   ├── ingestion/
│   │   └── pdf_parser.py           ← Parser de PDF
│   └── models/
│       └── paper.py                ← Modelos de datos
├── examples/
│   └── nlp_analysis_demo.py        ← Demo NLP ⭐
├── tests/
│   ├── test_nlp_components.py      ← Tests NLP ⭐
│   └── test_web_api.py             ← Tests API ⭐
└── docs/
    ├── NLP_FEATURES.md             ← Documentación NLP ⭐
    └── WEB_APP_NLP.md              ← Guía web app ⭐
```

---

## 🔧 Solución de Problemas

### Problema: "NLP processor not initialized"

**Solución**:
```bash
# Instalar dependencias
pip install spacy nltk

# Descargar modelos
python -m spacy download en_core_web_sm
python setup_nltk.py
```

### Problema: "Server not responding"

**Solución**:
```bash
# Verificar que no hay otro proceso en el puerto 8000
# Windows:
netstat -ano | findstr :8000

# Reiniciar servidor
python app.py
```

### Problema: "Module not found"

**Solución**:
```bash
# Asegurarse de estar en el directorio correcto
cd d:\GITHUB\Paper-collector

# Reinstalar dependencias
pip install -r requirements.txt
```

---

## 🎨 Ejemplo de Uso Completo

### 1. Iniciar el Servidor

```bash
PS D:\GITHUB\Paper-collector> python app.py
✓ NLP processor initialized
INFO:     Started server process [12345]
INFO:     Uvicorn running on http://0.0.0.0:8000
```

### 2. Abrir el Navegador

Visita: `http://localhost:8000`

### 3. Subir un Paper

- Arrastra un PDF a la zona de drop
- O haz clic para seleccionar

### 4. Ver Resultados

El análisis mostrará:

```
📚 Deep Learning for Speech Recognition

1. HIGH-LEVEL TECHNICAL SUMMARY
   [Resumen técnico generado]

2. RESEARCH PROBLEM DEFINITION
   Problem: Automatic speech recognition...
   Relevance: Critical for accessibility...

3. METHODOLOGY
   Input Data: Dataset(s): TIMIT, LibriSpeech  ← NER extrajo esto
   Techniques:
   • convolutional neural network              ← NER extrajo esto
   • deep learning
   • neural network
   Evaluation: Evaluation metrics: accuracy, 95%  ← NER extrajo esto

4. MAIN CONTRIBUTIONS
   1. We propose a CNN architecture...         ← Discourse analysis
   2. Our approach achieves 95% accuracy...

5. LIMITATIONS AND ASSUMPTIONS
   • Model requires significant GPU resources  ← Discourse analysis

6. KEY CONCEPTS AND TERMINOLOGY
   Concept                          | Definition
   --------------------------------|---------------------------
   convolutional neural network    | Technical concept from...
   deep learning approach          | Key technical phrase...
   speech recognition              | Technical concept from...

7. THEMATIC CLASSIFICATION
   Speech Processing | Machine Learning | Pattern Recognition

8. POSITIONING WITHIN STATE OF THE ART
   [Análisis de posicionamiento]

9. CITATION-READY SUMMARY
   [Resumen listo para citar]
```

---

## ✅ Checklist de Verificación

Antes de usar el proyecto, verifica:

- [ ] Servidor corriendo en http://localhost:8000
- [ ] Dependencias instaladas (`pip install -r requirements.txt`)
- [ ] Modelo spaCy descargado (`python -m spacy download en_core_web_sm`)
- [ ] Datos NLTK descargados (`python setup_nltk.py`)
- [ ] Tests pasando (`python tests/test_nlp_components.py`)

---

## 🎉 ¡Listo para Usar!

El proyecto está completamente configurado con:

✅ **Web Interface** - Interfaz moderna y responsiva
✅ **NLP Analysis** - Análisis científico avanzado
✅ **API REST** - Endpoints para integración
✅ **CLI Tools** - Herramientas de línea de comandos
✅ **Documentation** - Documentación completa
✅ **Tests** - Suite de tests completa

**¡Disfruta analizando papers científicos con IA!** 🚀
