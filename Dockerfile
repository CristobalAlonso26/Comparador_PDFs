FROM python:3.11-slim

# evitar prompts interactivos de apt
ENV DEBIAN_FRONTEND=noninteractive

# dependencias del sistema para matplotlib y pdfplumber
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libgl1 \
    libglib2.0-0 \
    fonts-dejavu-core \
    && rm -rf /var/lib/apt/lists/*

# directorio de trabajo
WORKDIR /app

# copiar solo requirements primero para aprovechar cache de docker
COPY requirements.txt .

# instalar dependencias de python
RUN pip install -r requirements.txt

# copiar el resto del codigo
COPY . .

# variables de entorno para silenciar warnings
ENV TRANSFORMERS_VERBOSITY=error
ENV TF_CPP_MIN_LOG_LEVEL=3

# exponer puerto de streamlit
EXPOSE 8501

# crear directorio para datos de streamlit
RUN mkdir -p /root/.streamlit

# comando de ejecucion
CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0", "--server.headless=true"]
