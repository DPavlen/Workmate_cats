FROM python:3.11.9-slim

ENV SRC_DIR=/app \
    APP_USER=backend-user \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    GUNICORN_PROCESSES=4 \
    GUNICORN_CONNECTIONS=8 \
    GUNICORN_LOGLEVEL='error'

RUN apt-get update && \
    apt-get install -y dos2unix && \
    apt-get install -y gcc libpq-dev

WORKDIR /app

RUN pip install poetry

COPY pyproject.toml /app/
#COPY poetry.lock /app/
# Копируем только файлы зависимостей и устанавливаем их
#COPY pyproject.toml poetry.lock /app/

RUN poetry config virtualenvs.create true && \
    poetry config virtualenvs.path /app/.venv && \
    poetry install --no-interaction --no-ansi

#RUN poetry lock && poetry install --only main

COPY . /app/

CMD ["bash", "/app/run_django.sh"]

RUN poetry install --no-root