From python:3.8-slim-buster

RUN mkdir ./app

COPY ./lab_1 ./app

WORKDIR ./app

CMD ["python3", "rules_and_facts.py"]
