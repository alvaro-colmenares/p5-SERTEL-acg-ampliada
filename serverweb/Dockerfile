FROM python:3.10

# Crear una carpeta para la aplicación web
RUN mkdir -p /iroom

# y la declaramos como carpeta de trabajo
WORKDIR /iroom

# Copiamos el archivo requirements.txt dentro de la imagen del contenedor. 
# El contenido de este archivo se explica más adelante
COPY requirements.txt /iroom

# Instalamos las dependencias dentro de la imagen
RUN pip install --no-cache-dir -r requirements.txt

# Copiamos la aplicación web dentro de la imagen
COPY ./iroom /iroom

# Puerto en el que escuchará el contenedor
EXPOSE 5000

CMD python iroom.py