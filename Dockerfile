# Stage 1 -runs the test
#FROM python:3.11.2-slim-buster AS build
#WORKDIR /UI_web
#COPY requirements.txt /UI_web/requirements.txt
#RUN pip install --no-cache-dir --upgrade -r /UI_web/requirements.txt
#COPY ./ /UI_web/
#RUN coverage run -m pytest

# Stage 2 - runs the UI
FROM python:3.11.2-slim-buster
WORKDIR /UI_web
COPY requirements.txt /UI_web/requirements.txt
RUN pip install --no-cache-dir --upgrade -r /UI_web/requirements.txt
COPY ./ /UI_web/
EXPOSE 8050
CMD ["python", "main.py", "-d", "False"]
