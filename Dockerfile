FROM python:3.10

WORKDIR /app
COPY . /app

RUN cd /app && pip install -U pipenv && pipenv install

EXPOSE 8000

ENTRYPOINT ["pipenv", "run", "python", "-m", "knative_ml_services", "--mode", "api"]
