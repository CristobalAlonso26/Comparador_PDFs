# Comparador de Documentos PDF

## Acerca del proyecto

Herramienta que permite comparar dos documentos PDF utilizando un LLM y análisis estadístico de texto (TF-IDF) para determinar su porcentaje de similitud, identificar temas en común y únicos, y generar un diagrama de Venn visual. Combina inteligencia artificial con técnicas clásicas de procesamiento de lenguaje natural para ofrecer resultados más completos. La interfaz está construida con **Streamlit**, lo que permite una interacción rápida y sencilla desde el navegador.

### Decisiones estructurales

El proyecto sigue un enfoque modular para mantener el código organizado y fácil de mantener:

- **`pdf_extractor.py`**: Encapsula la lógica de extracción de texto de PDFs, separando esta responsabilidad del resto del flujo.
- **`llm_analyzer.py`**: Combina comunicación con el LLM (API compatible con OpenAI) y análisis estadístico de texto con TF-IDF para extracción de temas y resumenes extractivos. Esto permite tener resultados tanto semánticos como estadísticos sin depender exclusivamente del modelo.
- **`venn_diagram.py`**: Generación independiente del diagrama de Venn, reutilizable en otros contextos.
- **`app.py`**: Punto de entrada de la aplicación Streamlit, orquestando los módulos anteriores sin contener lógica de negocio.
- **Dockerizado**: Se incluye `Dockerfile` y `docker-compose.yml` para facilitar el despliegue sin dependencias locales.

---

Herramienta para comparar dos documentos PDF y encontrar su porcentaje de similitud usando un LLM y analisis estadistico de texto (TF-IDF). Analiza si los documentos estan relacionados, extrae temas en comun y muestra un diagrama de Venn.

## Instalacion con Docker (recomendado)

### 1. Configurar API key

Edita el archivo `.env` y configura tu proveedor compatible con OpenAI:

```
LLM_API_KEY=tu-api-key-aqui
LLM_BASE_URL=https://tu-endpoint.com/v1
LLM_MODEL=qwen-3.5
```

### 2. Ejecutar con docker-compose

```bash
docker compose up --build
```

Se abrira en `http://localhost:8501`

## Instalacion local (sin Docker)

### 1. Configurar API key

Edita el archivo `.env` y configura tu proveedor compatible con OpenAI:

```
LLM_API_KEY=tu-api-key-aqui
LLM_BASE_URL=https://tu-endpoint.com/v1
LLM_MODEL=qwen-3.5
```

### 2. Instalar dependencias

```bash
pip install -r requirements.txt
```

### 3. Ejecutar

```bash
python -m streamlit run app.py
```

Se abrira en `http://localhost:8501`

## Como funciona

1. Selecciona el idioma de los documentos (Espanol o Ingles)
2. Sube dos archivos PDF
3. Presiona "Comparar Documentos"
4. La app muestra primero los resultados del **LLM**:
   - Porcentaje de similitud y nivel de relacion
   - Diagrama de Venn visual
   - Temas en comun y unicos identificados por el modelo
   - Explicacion semantica de la relacion entre documentos
5. Mas abajo se presentan los resultados del **analisis estadistico (TF-IDF)** para comparar:
   - Resumenes extractivos de cada documento
   - Palabras clave extraidas por relevancia estadistica (temas compartidos y unicos)

## Estructura del proyecto

| Archivo | Descripcion |
|---|---|
| `app.py` | Aplicacion principal de Streamlit |
| `pdf_extractor.py` | Extraccion de texto de PDFs |
| `llm_analyzer.py` | Analisis con LLM + analisis estadistico TF-IDF (resumenes extractivos, extraccion de temas) |
| `venn_diagram.py` | Generacion del diagrama de Venn |
| `.env` | Configuracion de API key (no subir a git) |
| `Dockerfile` | Configuracion del contenedor Docker |
| `docker-compose.yml` | Ejecucion con docker compose |
| `requirements.txt` | Dependencias del proyecto |
| `ejemplo.py` | Ejemplo de clase con question-answering |

## Modelos soportados

Cualquier modelo de un proveedor compatible con la API de OpenAI:
- **Qwen 3.5**, **Llama 3.1**, **Mistral**, **GPT-4o**, etc.
- Configurable en `.env` con `LLM_MODEL` y `LLM_BASE_URL`

## Nota

Los PDFs deben tener texto extraible (no pueden ser imagenes escaneadas).
