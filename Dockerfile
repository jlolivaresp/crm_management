FROM python:3.11-slim

ENV PYTHONUNBUFFERED=1 \
    POETRY_VIRTUALENVS_CREATE=false \
    PATH="/root/.local/bin:$PATH"

RUN pip install poetry

WORKDIR /app

ENV PYTHONPATH="${PYTHONPATH}:/app"

COPY . .

COPY pyproject.toml .
COPY poetry.lock .

RUN poetry install --only main --no-interaction --no-ansi --no-cache

ENTRYPOINT ["poetry", "run", "python"]
