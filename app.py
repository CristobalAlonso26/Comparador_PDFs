import os
os.environ["TRANSFORMERS_VERBOSITY"] = "error"
os.environ["TF_CPP_MIN_LOG_LEVEL"] = "3"

import streamlit as st
import tempfile
from dotenv import load_dotenv
from pdf_extractor import extract_text_limited
from llm_analyzer import LLMAnalyzer
from venn_diagram import crear_venn_por_similitud

# cargar variables de entorno desde .env
load_dotenv()

# configuracion de la pagina
st.set_page_config(
    page_title="Comparador de PDFs",
    page_icon="📄",
    layout="wide"
)

# titulo principal
st.title("Comparador de Documentos PDF")
st.markdown("---")

# selector de idioma
idioma = st.selectbox(
    "Idioma de los documentos",
    options=["espanol", "ingles"],
    format_func=lambda x: "Espanol" if x == "espanol" else "Ingles",
    index=0
)

st.markdown("---")

# sidebar con info
with st.sidebar:
    st.header("Instrucciones")
    st.write("1. Selecciona el idioma de los documentos")
    st.write("2. Sube dos archivos PDF")
    st.write("3. Presiona el boton 'Comparar Documentos'")
    st.write("4. Espera el analisis y resultados")
    st.markdown("---")
    st.caption("Sistemas Inteligentes - Comparador PDFs")

# crear columnas para los uploads
col1, col2 = st.columns(2)

with col1:
    st.subheader("Documento 1")
    archivo1 = st.file_uploader("Subir primer PDF", type=["pdf"], key="doc1")

with col2:
    st.subheader("Documento 2")
    archivo2 = st.file_uploader("Subir segundo PDF", type=["pdf"], key="doc2")

# boton para comparar
if st.button("Comparar Documentos", type="primary", use_container_width=True):
    # verificar que ambos archivos fueron subidos
    if archivo1 is None or archivo2 is None:
        st.error("Por favor sube ambos archivos PDF antes de comparar")
    else:
        # verificar api key
        api_key = os.getenv("LLM_API_KEY", "")
        if not api_key or api_key == "tu-api-key-aqui":
            st.error("Configura tu LLM_API_KEY en el archivo .env")
            st.info("Obten una API key de tu proveedor compatible con OpenAI")
        else:
            modelo = os.getenv("LLM_MODEL", "qwen-3.5")
            base_url = os.getenv("LLM_BASE_URL", None)

            # mostrar spinner mientras procesa
            with st.spinner("Analizando documentos con el LLM... esto puede tardar un momento"):
                try:
                    # guardar archivos temporalmente
                    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp1:
                        tmp1.write(archivo1.getvalue())
                        path1 = tmp1.name

                    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp2:
                        tmp2.write(archivo2.getvalue())
                        path2 = tmp2.name

                    # extraer texto de ambos pdfs
                    texto1 = extract_text_limited(path1, max_chars=4000)
                    texto2 = extract_text_limited(path2, max_chars=4000)

                    # limpiar archivos temporales
                    os.unlink(path1)
                    os.unlink(path2)

                    # inicializar analizador y procesar
                    analyzer = LLMAnalyzer(api_key=api_key, idioma=idioma, model=modelo, base_url=base_url)
                    resultados = analyzer.analizar_documentos(texto1, texto2)

                    # mostrar resultados
                    st.markdown("---")
                    st.header("Resultados del Analisis")

                    # mostrar porcentaje de similitud grande
                    col_metric1, col_metric2, col_metric3 = st.columns(3)

                    with col_metric1:
                        st.metric(
                            label="Similitud",
                            value=f"{resultados['porcentaje_similitud']}%"
                        )

                    with col_metric2:
                        st.metric(
                            label="Nivel de Relacion",
                            value=resultados["nivel_relacion"].capitalize()
                        )

                    with col_metric3:
                        st.metric(
                            label="Temas en Comun",
                            value=len(resultados["topics_comunes"])
                        )

                    # mostrar diagrama de venn + temas del LLM lado a lado
                    st.markdown("---")
                    st.subheader("Comparacion Visual y Temas Identificados")

                    venn_path = "venn_diagram.png"
                    crear_venn_por_similitud(
                        resultados["porcentaje_similitud"],
                        output_path=venn_path
                    )

                    col_venn, col_llm = st.columns([1, 1])

                    with col_venn:
                        st.markdown("**Diagrama de Venn (similitud porcentual)**")
                        st.image(venn_path, width=500)

                    with col_llm:
                        st.markdown("**Temas identificados por el LLM**")
                        st.caption("Estos temas fueron extraidos directamente por el modelo de lenguaje")

                        temas_comunes_llm = resultados.get("temas_comunes_llm", [])
                        temas_doc1_llm = resultados.get("temas_documento_1_llm", [])
                        temas_doc2_llm = resultados.get("temas_documento_2_llm", [])

                        # el llm devuelve "temas_documento_1" y "temas_documento_2" en el JSON
                        if not temas_doc1_llm:
                            temas_doc1_llm = resultados.get("temas_documento_1", [])
                        if not temas_doc2_llm:
                            temas_doc2_llm = resultados.get("temas_documento_2", [])

                        if temas_comunes_llm:
                            st.markdown("**Temas en comun:**")
                            for tema in temas_comunes_llm:
                                st.write(f"- {tema}")

                        if temas_doc1_llm:
                            st.markdown("**Solo Doc 1:**")
                            for tema in temas_doc1_llm:
                                st.write(f"- {tema}")

                        if temas_doc2_llm:
                            st.markdown("**Solo Doc 2:**")
                            for tema in temas_doc2_llm:
                                st.write(f"- {tema}")

                        if not temas_comunes_llm and not temas_doc1_llm and not temas_doc2_llm:
                            st.write("El LLM no identifico temas especificos.")

                    # mostrar explicacion del LLM
                    st.markdown("---")
                    st.subheader("Analisis del LLM")
                    if resultados["explicacion_llm"]:
                        st.info(resultados["explicacion_llm"])
                    else:
                        st.info("El LLM no proporciono una explicacion detallada.")

                    # mostrar resmenes (generados por TF-IDF, no por LLM)
                    st.markdown("---")
                    st.subheader("Resumenes (analisis directo del texto)")
                    st.caption("Generados automaticamente seleccionando las oraciones mas relevantes del texto original")
                    col_res1, col_res2 = st.columns(2)

                    with col_res1:
                        st.markdown("**Documento 1:**")
                        st.info(resultados["resumen1"])

                    with col_res2:
                        st.markdown("**Documento 2:**")
                        st.info(resultados["resumen2"])

                    # mostrar topics (generados por TF-IDF, no por LLM)
                    st.subheader("Temas identificados por TF-IDF (analisis directo del texto)")
                    st.caption("Palabras clave extraidas por frecuencia y relevancia estadistica en el texto")
                    col_t1, col_t2, col_t3 = st.columns(3)

                    with col_t1:
                        st.markdown("**Solo Doc 1:**")
                        if resultados["topics_unicos_doc1"]:
                            for topic in resultados["topics_unicos_doc1"]:
                                st.write(f"- {topic}")
                        else:
                            st.write("(sin temas unicos)")

                    with col_t2:
                        st.markdown("**Temas Compartidos:**")
                        if resultados["topics_comunes"]:
                            for topic in resultados["topics_comunes"]:
                                st.write(f"- {topic}")
                        else:
                            st.write("(sin temas compartidos)")

                    with col_t3:
                        st.markdown("**Solo Doc 2:**")
                        if resultados["topics_unicos_doc2"]:
                            for topic in resultados["topics_unicos_doc2"]:
                                st.write(f"- {topic}")
                        else:
                            st.write("(sin temas unicos)")

                    # analisis final
                    st.markdown("---")
                    st.subheader("Conclusion")

                    if resultados["porcentaje_similitud"] > 60:
                        st.success(
                            f"Los documentos tienen una relacion **ALTA** ({resultados['porcentaje_similitud']}%). "
                            f"Comparten {len(resultados['topics_comunes'])} temas principales y tratan sobre temas muy similares."
                        )
                    elif resultados["porcentaje_similitud"] > 40:
                        st.warning(
                            f"Los documentos tienen una relacion **MODERADA** ({resultados['porcentaje_similitud']}%). "
                            f"Comparten algunos temas pero tambien tienen contenido diferente."
                        )
                    else:
                        st.info(
                            f"Los documentos tienen una relacion **BAJA** ({resultados['porcentaje_similitud']}%). "
                            f"Solo comparten {len(resultados['topics_comunes'])} temas y tratan sobre temas distintos."
                        )

                except Exception as e:
                    st.error(f"Error al procesar los documentos: {str(e)}")
                    st.exception(e)

# footer
st.markdown("---")
st.caption("Comparador de PDFs usando LLM y analisis directo de texto ")
