import pdfplumber
import os


def extract_text(pdf_path):
    """extrae texto completo de un archivo pdf"""
    if not os.path.exists(pdf_path):
        raise FileNotFoundError(f"el archivo no existe: {pdf_path}")

    texto_completo = ""

    with pdfplumber.open(pdf_path) as pdf:
        # recorrer todas las paginas del pdf
        for pagina in pdf.pages:
            texto_pagina = pagina.extract_text()
            if texto_pagina:
                texto_completo += texto_pagina + "\n\n"

    # limpiar espacios extras
    texto_completo = texto_completo.strip()

    if not texto_completo:
        raise ValueError("no se pudo extraer texto del pdf, puede ser escaneado")

    return texto_completo


def extract_text_limited(pdf_path, max_chars=4000):
    """extrae texto pero limitado a cierto numero de caracteres (para no saturar el modelo)"""
    texto = extract_text(pdf_path)

    # si el texto es muy largo, cortar al limite
    if len(texto) > max_chars:
        texto = texto[:max_chars]
        # intentar cortar en un punto limpio (final de parrafo)
        ultimo_punto = texto.rfind(".")
        if ultimo_punto > max_chars * 0.8:
            texto = texto[:ultimo_punto + 1]

    return texto
