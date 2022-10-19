FROM python:3.10

RUN pip install -U pipenv

WORKDIR /app

COPY . /app

RUN cd /app && pipenv install

EXPOSE 8000

ENTRYPOINT ["pipenv", "run", "python", "-m", "knative_ml_services", "--mode", "api"]
