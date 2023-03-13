# Stage 1 -runs the test
FROM kevingerardo23/bank-api:9dd57c4490b5d135ca2e4122daf7b910a5a51e24 AS test
WORKDIR /UI_web
COPY requirements.txt /UI_web/requirements.txt
RUN pip install --no-cache-dir --upgrade -r /UI_web/requirements.txt
COPY ./ /UI_web/
RUN pip install --no-cache-dir --upgrade -r ../app/requirements_api.txt
RUN timeout 20s python ../app/bank_api/api.py &
RUN ls
RUN python ./utils/auto_reg.py
#["timeout", "10s", "python", "../app/bank_api/api.py", "&"]; exit 0
RUN coverage run -m pytest
#CMD bash -c "while true; do sleep 1; done"

# Stage 2 - runs the UI
FROM python:3.11.2-slim-buster
WORKDIR /UI_web
COPY requirements.txt /UI_web/requirements.txt
RUN pip install --no-cache-dir --upgrade -r /UI_web/requirements.txt
COPY ./ /UI_web/
EXPOSE 8050
CMD ["python", "main.py", "-d", "False"]
