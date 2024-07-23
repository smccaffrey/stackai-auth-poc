FROM python:3.11

WORKDIR /auth

COPY pyproject.toml ./
COPY poetry.lock ./

RUN pip install poetry

COPY ./ ./

RUN poetry install --no-root --no-interaction

CMD ["poetry", "run", "uvicorn", "auth.app:app", "--host", "0.0.0.0", "--port", "9898"]