FROM python:3.9-slim-buster

WORKDIR /app
COPY *.py requirements.txt ./

RUN pip install -r requirements.txt -q

COPY app ./app
COPY config ./config

EXPOSE 8080

CMD [ "python", "run.py" ]
