FROM python:3.11.2-slim-buster

WORKDIR /UI_web

COPY requirements.txt /UI_web/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /UI_web/requirements.txt

COPY ./ /UI_web/
# Open the port conection
EXPOSE 8050
# Para que el contenedor este encendido continuamente (Un while inf)
#CMD bash -c "while true; do sleep 1; done"
CMD ['python' 'main.py', '-d', 'False']
