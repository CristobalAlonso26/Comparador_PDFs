# Comparador de Documentos PDF

Herramienta para comparar dos documentos PDF y encontrar su porcentaje de similitud usando un LLM. Analiza si los documentos estan relacionados, extrae temas en comun y muestra un diagrama de Venn.

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
4. El LLM analiza ambos documentos y devuelve:
   - Porcentaje de similitud
   - Explicacion de la relacion
   - Temas en comun y temas unicos
   - Diagrama de Venn visual

## Estructura del proyecto

| Archivo | Descripcion |
|---|---|
| `app.py` | Aplicacion principal de Streamlit |
| `pdf_extractor.py` | Extraccion de texto de PDFs |
| `llm_analyzer.py` | Analisis con LLM via API compatible con OpenAI |
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
