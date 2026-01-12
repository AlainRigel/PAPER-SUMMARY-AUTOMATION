# 📚 Índice de Documentación del Proyecto

Este archivo describe el propósito y contenido de cada archivo de documentación disponible en el proyecto **Paper Collector**.

## 🚀 Guías de Inicio y Ejecución (Para Usuarios)

Archivos indispensables para poner en marcha el sistema.

| Archivo | Descripción |
|---------|-------------|
| **`docs/GUIA_EJECUCION.md`** | **⭐ LEER PRIMERO.** Guía completa paso a paso para instalar dependencias y ejecutar el servidor y la web. |
| **`docs/QUICKSTART.md`** | Versión resumida para arrancar rápidamente si ya conoces el proyecto. |
| **`docs/GROQ_SETUP.md`** | Guía específica para configuración de **Groq LLM** (anteriormente DeepSeek). |

## 🏗️ Arquitectura y Diseño (Para Arquitectos)

Documentos que definen qué es el sistema y cómo está diseñado.

| Archivo | Descripción |
|---------|-------------|
| **`design_specification.md`** | Especificación técnica original. Define la arquitectura, modelos de datos y fases del proyecto. |
| **`docs/PROJECT_SUMMARY.md`** | Resumen de alto nivel del estado actual del proyecto, hitos alcanzados y fases pendientes. |
| **`README.md`** | La "cara" del repositorio. Descripción general, features principales y estructura básica. |

## 🧠 Documentación Técnica de NLP (Para Desarrolladores)

Detalles profundos sobre la implementación de Inteligencia Artificial.

| Archivo | Descripción |
|---------|-------------|
| **`docs/NLP_FEATURES.md`** | Explica las capacidades de NLP: NER, segmentación de discurso, embeddings, etc. |
| **`docs/NLP_IMPLEMENTATION_SUMMARY.md`** | Resumen técnico de cómo se implementó el módulo de NLP en código. |
| **`docs/WEB_APP_NLP.md`** | Detalla cómo el frontend (web) se comunica con el backend para mostrar los datos de NLP. |
| **`docs/RESUMEN_NLP.md`** | Resumen ejecutivo (en español) de la implementación de la Fase 2 (NLP). |

## 📝 Bitácoras de Desarrollo (Histórico)

Registros cronológicos de lo que se ha ido construyendo.

| Archivo | Descripción |
|---------|-------------|
| **`docs/DESARROLLO_PASO_A_PASO.md`** | **Muy detallado.** Bitácora completa de cada comando, error y solución durante el desarrollo. |
| **`docs/NLP_COMPLETADO.md`** | Checklist final y resumen de éxito al terminar la implementación de NLP. |

## 📂 Documentación de Componentes

Léemes específicos dentro de carpetas clave.

| Archivo | Ubicación | Descripción |
|---------|-----------|-------------|
| `README.md` | `web/` | Documentación específica del Frontend (HTML/JS/CSS). |
| `README.md` | `data/` | Explica la estructura de almacenamiento de PDFs y datos. |
| `README.md` | `examples/` | Guía para usar los scripts de ejemplo (demos). |

---

## 💡 Recomendación de Orden de Lectura

1. Si quieres **ejecutar ya**: Ve a `GUIA_EJECUCION.md`.
2. Si quieres **entender el código**: Lee `design_specification.md` y luego `docs/NLP_FEATURES.md`.
3. Si quieres **configurar la IA**: Ve directo a `docs/DEEPSEEK_SETUP.md` (aunque ahora usamos Groq, la estructura es similar).
