FROM python:3.10-alpine

RUN apk update && apk upgrade
RUN apk add --no-cache gcc g++ build-base wget

USER root
RUN adduser -D celery
RUN addgroup celery celery
RUN addgroup root celery

WORKDIR /usr/src/app
COPY ./ ./

COPY ./backend/poetry.lock ./backend/pyproject.toml ./
RUN pip install poetry
RUN poetry config virtualenvs.create false && \
    poetry install --no-interaction --no-ansi

COPY ./docker/celery/celeryd /etc/init.d/
COPY ./docker/celery/celerybeat /etc/init.d/
COPY ./docker/celery/config/celeryd /etc/default/
RUN ["chmod", "755", "/etc/init.d/celeryd"]
RUN ["chmod", "755", "/etc/init.d/celerybeat"]
RUN ["chmod", "640", "/etc/default/celeryd"]

RUN ["chmod", "+x", "docker/celery-worker/entry.sh"]
ENTRYPOINT ["docker/celery-worker/entry.sh"]
