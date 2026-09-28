# Usar una imagen oficial de Python basada en Linux
FROM python:3.10-slim

# Instalar dependencias del sistema necesarias para pygame
RUN apt-get update && apt-get install -y \
    gcc \
    libsdl2-dev \
    libsdl2-image-dev \
    libsdl2-mixer-dev \
    libsdl2-ttf-dev \
    && rm -rf /var/lib/apt/lists/*

# Establecer el directorio de trabajo
WORKDIR /app

# Copiar el código al contenedor
COPY . /app

# Instalar dependencias de Python
RUN pip install --no-cache-dir -r requirements.txt

# Exponer el puerto
EXPOSE 10000

# Comando para ejecutar la aplicación
CMD ["python", "app.py"]