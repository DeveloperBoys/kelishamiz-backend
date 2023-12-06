FROM python:3.10-alpine

RUN pip install --upgrade pip

WORKDIR /usr/src/app
COPY ./ ./

COPY ./backend/poetry.lock ./backend/pyproject.toml ./
RUN pip install poetry
RUN poetry config virtualenvs.create false && \
    poetry install --no-interaction --no-ansi

RUN ["chmod", "+x", "./docker/backend/entrypoint.sh"]
ENTRYPOINT ["./docker/celery-worker/entrypoint.sh"]
