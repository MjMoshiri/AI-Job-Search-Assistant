FROM python:3.10-slim-buster

WORKDIR /app
COPY . /app

RUN pip install Flask sqlalchemy psycopg2-binary Flask-Cors

CMD ["python", "api.py"]
