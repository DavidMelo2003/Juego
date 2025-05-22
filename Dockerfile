# Usar una imagen base de Python. Elige una versión que sea compatible.
# python:3.9-slim es una buena opción por su tamaño reducido.
FROM python:3.9-slim

# Establecer el directorio de trabajo dentro del contenedor
WORKDIR /app

# Instalar dependencias del sistema necesarias para Pygame y X11
# libsdl2-mixer-2.0-0, libsdl2-image-2.0-0, libsdl2-2.0-0 son para Pygame
# libsm6, libxext6, libxrender1 son para la interfaz gráfica (X11)
# python3-tk puede ser necesario para algunas funcionalidades o si Pygame no encuentra un backend.
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    python3-tk \
    libsdl2-mixer-2.0-0 \
    libsdl2-image-2.0-0 \
    libsdl2-2.0-0 \
    libsm6 \
    libxext6 \
    libxrender1 \
    && rm -rf /var/lib/apt/lists/*

# Instalar Pygame
RUN pip install --no-cache-dir pygame

# Copiar todos los archivos del proyecto (script principal, carpeta assets) al directorio de trabajo en el contenedor
COPY . .

# Establecer la variable de entorno DISPLAY.
# Esto es crucial para que las aplicaciones GUI dentro de Docker puedan mostrarse en el host.
# El valor exacto de DISPLAY se pasará en el comando `docker run`.
ENV DISPLAY=:0

# Comando para ejecutar el juego cuando se inicie el contenedor
ENTRYPOINT ["python", "eco_guardian_mk3.py"]
