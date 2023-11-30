FROM python:3.10-alpine

RUN pip install --upgrade pip

COPY ./ ./
WORKDIR /usr/src/app

COPY ./backend/poetry.lock ./backend/pyproject.toml ./
RUN pip install poetry
RUN poetry config virtualenvs.create false && \
    poetry install --no-interaction --no-ansi

COPY ./docker/backend/entrypoint.sh /usr/src/app
RUN chmod +x /usr/src/app/entrypoint.sh

ENTRYPOINT ["/usr/src/app/entrypoint.sh"]
