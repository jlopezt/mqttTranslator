# Un archivo docker (dockerfile) comienza siempre importanto la imagen base. 
# Utilizamos la palabra clave 'FROM' para hacerlo.
# En nuestro ejemplo, queremos importar la imagen de python.
# Así que escribimos 'python' para el nombre de la imagen y 'latest' para la versión.
#FROM python:3.13.0a3-alpine3.19
FROM python:3.10-alpine3.19

# Para lanzar nuestro código python, debemos importarlo a nuestra imagen.
# Utilizamos la palabra clave 'COPY' para hacerlo.
# El primer parámetro 'main.py' es el nombre del archivo en el host.
# El segundo parámetro '/' es la ruta donde poner el archivo en la imagen.
# Aquí ponemos el archivo en la carpeta raíz de la imagen. 
COPY main.py /
COPY config.py /
COPY config.json /
COPY requirements.txt /

WORKDIR /

RUN pip install -r requirements.txt

# Necesitamos definir el comando a lanzar cuando vayamos a ejecutar la imagen.
# Utilizamos la palabra clave 'CMD' para hacerlo.
# El siguiente comando ejecutará "python ./main.py".
#CMD [ "python", "./main.py -c config.json" ]

ENTRYPOINT python main.py -c config.json
#ENTRYPOINT python -V