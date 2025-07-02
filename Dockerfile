FROM python:3.11-slim

# 1. Instala dependências do sistema com versões específicas do Debian
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    # Versões do GDAL disponíveis nos repositórios oficiais do Debian
    gdal-bin \
    libgdal-dev \
    python3-gdal \
    && rm -rf /var/lib/apt/lists/*

# 2. Configura variáveis de ambiente para o GDAL
ENV CPLUS_INCLUDE_PATH=/usr/include/gdal
ENV C_INCLUDE_PATH=/usr/include/gdal
ENV LD_LIBRARY_PATH=/usr/lib

# 3. Instala os pacotes Python
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .