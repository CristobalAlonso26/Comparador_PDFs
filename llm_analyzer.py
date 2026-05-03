from openai import OpenAI
from sklearn.feature_extraction.text import TfidfVectorizer
import re
import numpy as np
import nltk
from nltk.corpus import stopwords
import json

# descargar stopwords si no existen
nltk.download("stopwords", quiet=True)
STOPWORDS_ES = set(stopwords.words("spanish"))
STOPWORDS_EN = set(stopwords.words("english"))

IDIOMAS = {
    "espanol": {"stopwords": STOPWORDS_ES, "label": "Espanol", "lang_prompt": "español"},
    "ingles": {"stopwords": STOPWORDS_EN, "label": "Ingles", "lang_prompt": "inglés"},
}


class LLMAnalyzer:
    """analiza dos documentos usando un LLM compatible con OpenAI para evaluar relacion y similitud"""

    def __init__(self, api_key, idioma="espanol", model="qwen-3.5", base_url=None):
        self.client = OpenAI(api_key=api_key, base_url=base_url)
        self.model = model
        self.idioma_config = IDIOMAS.get(idioma, IDIOMAS["espanol"])
        self.stopwords = self.idioma_config["stopwords"]
        print(f"analizador LLM listo (modelo: {model}, idioma: {idioma})")

    def resumir_texto(self, texto, num_oraciones=3):
        """resumen extractivo: toma las oraciones mas importantes por tf-idf"""
        oraciones = re.split(r'(?<=[.!?]) +', texto)
        oraciones = [o.strip() for o in oraciones if len(o.strip()) > 20]

        if len(oraciones) <= num_oraciones:
            return " ".join(oraciones)

        vectorizer = TfidfVectorizer(stop_words=list(self.stopwords))
        tfidf_matrix = vectorizer.fit_transform(oraciones)

        scores = tfidf_matrix.sum(axis=1).A1
        top_indices = np.argsort(scores)[-num_oraciones:]
        top_indices = sorted(top_indices)

        return " ".join([oraciones[i] for i in top_indices])

    def extraer_topics(self, texto, num_topics=15):
        """extrae las palabras mas importantes del texto usando tf-idf"""
        texto_limpio = re.sub(r"[^\w\s]", " ", texto.lower(), flags=re.UNICODE)
        texto_limpio = re.sub(r"\d+", "", texto_limpio)

        palabras = texto_limpio.split()

        palabras_filtradas = [
            p for p in palabras
            if len(p) > 3 and p not in self.stopwords
        ]

        if len(palabras_filtradas) < num_topics:
            return list(set(palabras_filtradas))

        vectorizer = TfidfVectorizer(max_features=num_topics)
        tfidf_matrix = vectorizer.fit_transform([" ".join(palabras_filtradas)])

        feature_names = vectorizer.get_feature_names_out()
        return list(feature_names)

    def _construir_prompt(self, texto1, texto2):
        """construye el prompt para el LLM"""
        return f"""Analiza los siguientes dos documentos y responde SOLO con un JSON valido sin texto adicional.

Documento 1:
{texto1[:3000]}

Documento 2:
{texto2[:3000]}

Responde unicamente con este formato JSON:
{{
  "estan_relacionados": true o false,
  "porcentaje_similitud": numero entre 0 y 100,
  "explicacion": "breve explicacion en español de por que estan o no relacionados",
  "temas_comunes": ["tema1", "tema2", ...],
  "temas_documento_1": ["tema1", "tema2", ...],
  "temas_documento_2": ["tema1", "tema2", ...]
}}"""

    def analizar_documentos(self, texto1, texto2):
        """analiza dos documentos usando un LLM compatible con OpenAI"""

        # resumenes extractivos
        print("generando resumenes...")
        resumen1 = self.resumir_texto(texto1)
        resumen2 = self.resumir_texto(texto2)

        # topics por tf-idf
        print("extrayendo temas...")
        topics1 = set(self.extraer_topics(texto1))
        topics2 = set(self.extraer_topics(texto2))

        # consulta al LLM
        print("consultando al LLM...")
        prompt = self._construir_prompt(texto1, texto2)

        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": "Eres un analista de documentos experto. Responde solo con JSON valido, sin markdown ni texto adicional."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.1,
            max_tokens=500
        )

        # parsear respuesta
        contenido = response.choices[0].message.content.strip()

        # limpiar si viene con bloques de markdown
        if contenido.startswith("```"):
            contenido = contenido.split("```")[1]
            if contenido.startswith("json"):
                contenido = contenido[4:]
            contenido = contenido.strip()

        try:
            datos_llm = json.loads(contenido)
        except json.JSONDecodeError:
            datos_llm = {
                "estan_relacionados": True,
                "porcentaje_similitud": 50,
                "explicacion": "No se pudo parsear la respuesta del LLM",
                "temas_comunes": [],
                "temas_documento_1": [],
                "temas_documento_2": []
            }

        porcentaje_similitud = datos_llm.get("porcentaje_similitud", 50)
        explicacion = datos_llm.get("explicacion", "")
        temas_comunes_llm = datos_llm.get("temas_comunes", [])
        temas_doc1_llm = datos_llm.get("temas_documento_1", [])
        temas_doc2_llm = datos_llm.get("temas_documento_2", [])

        # topics compartidos por tf-idf
        topics_comunes = topics1.intersection(topics2)
        topics_unicos_1 = topics1 - topics2
        topics_unicos_2 = topics2 - topics1

        # nivel de relacion
        if porcentaje_similitud > 60:
            nivel_relacion = "alta"
        elif porcentaje_similitud > 40:
            nivel_relacion = "moderada"
        else:
            nivel_relacion = "baja"

        analisis = {
            "resumen1": resumen1,
            "resumen2": resumen2,
            "porcentaje_similitud": porcentaje_similitud,
            "nivel_relacion": nivel_relacion,
            "explicacion_llm": explicacion,
            "estan_relacionados": datos_llm.get("estan_relacionados", True),
            "topics_doc1": sorted(list(topics1)),
            "topics_doc2": sorted(list(topics2)),
            "topics_comunes": sorted(list(topics_comunes)),
            "topics_unicos_doc1": sorted(list(topics_unicos_1)),
            "topics_unicos_doc2": sorted(list(topics_unicos_2)),
            "temas_comunes_llm": temas_comunes_llm,
            "temas_documento_1_llm": temas_doc1_llm,
            "temas_documento_2_llm": temas_doc2_llm,
        }

        return analisis
