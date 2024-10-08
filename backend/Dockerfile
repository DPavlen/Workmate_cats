FROM python:3.11.9-slim

ENV SRC_DIR=/app \
    APP_USER=backend-user \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    GUNICORN_PROCESSES=4 \
    GUNICORN_CONNECTIONS=8 \
    GUNICORN_LOGLEVEL="error"\
    POETRY_VIRTUALENVS_IN_PROJECT=true\
    PATH="/app/.venv/bin:$PATH"


RUN apt-get update && \
    apt-get install -y dos2unix && \
    apt-get install -y gcc libpq-dev

WORKDIR /app

RUN pip install poetry

COPY pyproject.toml /app/

RUN poetry install --no-interaction --no-ansi --no-root

COPY . /app/

CMD ["bash", "/app/run_django.sh"]