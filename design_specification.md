# Arquitectura de Sistema: Amplificador Cognitivo para Investigación Académica

**Versión:** 1.0.0
**Fecha:** 2026-01-06
**Tipo de Documento:** Especificación Técnica y Metodológica

## 1. Arquitectura Técnica del Sistema (Pipeline)

La arquitectura propuesta sigue un patrón de **RAG (Retrieval-Augmented Generation) Modular Especializado**, desacoplando la ingestión, el procesamiento semántico y la interfaz de análisis.

### A. Capa de Ingestión y Normalización (ETL)
*   **Fuentes:** APIs académicas (Scholarly, Semantic Scholar, CrossRef, arXiv, PubMed) y carga manual de PDFs.
*   **Preprocesamiento:**
    *   *Parsing Estructural:* Uso de herramientas como **Grobid** o **Nougat** para convertir PDFs en XML/JSON estructurado, preservando secciones (Abstract, Metodología, Resultados, Referencias).
    *   *Resolución de Metadatos:* Deduplicación basada en DOIs y normalización de nombres de autores/afiliaciones.

### B. Capa de Procesamiento Semántico (AI Core)
*   **Vectorización (Embeddings):** Generación de vectores densos para búsqueda semántica.
*   **Grafo de Conocimiento (KG):** Inferencias de relaciones (ej. "Autor X *emplea* Método Y", "Paper A *refuta* Paper B").
*   **Extracción de Entidades:** Identificación de variables, métricas, datasets y métodos.

### C. Capa de Persistencia
*   **Vector Store:** Qdrant o Weaviate para almacenamiento de embeddings de alta dimensión.
*   **Graph Database:** Neo4j o RDF Store para almacenar relaciones de citas y co-autorías.
*   **Relational Meta-store:** PostgreSQL para gestión de usuarios, proyectos y metadatos bibliográficos "duros".

### D. Capa de Aplicación y Análisis
*   **Backend:** FastAPI (Python) para orquestación de servicios de inferencia.
*   **Frontend:** Interfaz reactiva (React/Next.js) enfocada en visualización de datos (D3.js / Cytoscape.js para grafos).

---

## 2. Definición de Componentes de IA

### A. Modelos de Representación (Embeddings)
No se utilizarán modelos genéricos (tipo text-embedding-ada-002) como fuente primaria, sino modelos pre-entrenados en corpus científicos para capturar matices disciplinares.
*   **Modelo Principal:** `allenai/specter2` (Specific for scientific tasks) o `allenai/scibert`. Estos modelos agrupan papers basándose en la topología de citas, no solo en similitud léxica.
*   **Fine-tuning:** Adaptadores LoRA opcionales para dominios muy específicos (ej. Bioinformática vs. Sociología).

### B. Pipeline de NLP y Extracción de Información (IE)
1.  **Segmentación Discursiva:** Clasificación de sentencias por función retórica (Background, Method, Result, Conclusion) usando clasificadores basados en BERT.
2.  **NER Científico (Named Entity Recognition):** Extracción de:
    *   `Task` (Tarea resuelta)
    *   `Method` (Metodología empleada)
    *   `Metric` (Métricas de evaluación)
    *   `Material` (Datasets o sustratos)
3.  **Cross-Document Coreference Resolution:** Identificar cuándo "el modelo propuesto" en una sección se refiere al mismo concepto en otro paper.

### C. Clasificación y Clustering
*   **Taxonomía Dinámica:** Uso de **BERTopic** o **Hierarchical Clustering** sobre los embeddings para descubrir clusters temáticos emergentes sin imponer categorías predefinidas rígidamente.

---

## 3. Especificación de Outputs Académicos

El sistema no "chatea", sino que "construye" artefactos de investigación.

### A. Matriz de Estado del Arte (State-of-the-Art Matrix)
Tabla dinámica generada automáticamente donde:
*   *Filas:* Papers seleccionados.
*   *Columnas:* Dimensiones de análisis (Problema, Solución, Métricas, Datasets, Limitaciones).
*   *Celdas:* Fragmentos extractivos o resúmenes abstractivos verificables.

### B. Grafo de Genealogía Científica
Visualización de árbol de citas que permite identificar:
*   **Papers Seminales:** Nodos raíz con alto impacto.
*   **Papers de Revisión:** Hubs que conectan múltiples ramas.
*   **Frentes de Investigación:** Clusters recientes de alta densidad.

### C. Reporte de Brechas (Gap Analysis)
Síntesis generada por LLM (con estricto *grounding*) que sugiere áreas poco exploradas basándose en las intersecciones vacías de la matriz de estado del arte.

---

## 4. Criterios de Calidad Científica

### A. Trazabilidad (Factuality & Grounding)
*   Cada afirmación generada por el sistema debe tener un hipervínculo directo al fragmento del PDF fuente (Page-level citation).
*   **Métrica:** RAGAS (Retrieval Augmented Generation Assessment) scores enfocados en *faithfulness* y *citation precision*.

### B. Reproducibilidad de Búsqueda
*   Los logs de búsqueda estructurada deben ser exportables (formato PRIMSA flowchart) para incluir en apéndices de tesis/papers.

### C. Tratamiento de la Incertidumbre
*   El sistema debe explicitar cuando la información es insuficiente o ambigua, en lugar de alucinar una respuesta definitiva. Uso de "hedging language" en los resúmenes.

---

## 5. Riesgos Metodológicos y Éticos

### A. Sesgo de Citación (Matthew Effect)
*   **Riesgo:** El algoritmo podría privilegiar papers altamente citados (efecto "rico se hace más rico"), invisibilizando investigación novedosa o de nicho.
*   **Mitigación:** Mecanismos de re-ranking que ponderen novedad ("recency") y relevancia semántica por sobre el mero conteo de citas.

### B. Alucinación de Referencias
*   **Riesgo:** LLMs generativos inventando papers que parecen reales.
*   **Mitigación:** Restricción dura (Hard Constraint): El sistema SOLO puede citar documentos que existen en su base de datos vectorial ingestada. Verificación de existencia de DOI antes de mostrar cualquier referencia.

### C. Dependencia Cognitiva
*   **Riesgo:** Estudiantes aceptando la taxonomía de la IA sin crítica.
*   **Mitigación:** La UX debe obligar al usuario a validar/editar las categorías propuestas. Modo "Copiloto" vs "Piloto Automático".

---

## 6. Extensiones Futuras (Roadmap)

### Fase 1: Asistente de Tesis (Escritura)
*   Módulo de "Consistency Check": Verificar que las conclusiones sean coherentes con los resultados presentados en los papers citados.

### Fase 2: Peer Review Simulator
*   Agente 'Adversario' configurado con distintas personalidades académicas (el metodólogo estricto, el revisor conceptual) para criticar los borradores del usuario.

### Fase 3: Predicción de Impacto
*   Análisis de grafos temporales para predecir qué temas emergentes tienen alta probabilidad de convertirse en tendencia (Hot topics).
