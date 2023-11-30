FROM python:3.10-alpine
EXPOSE 5555

ENV DEBIAN_FRONTEND noninteractive
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV LC_ALL C.UTF-8
ENV LANG C.UTF-8

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
RUN chmod 755 /etc/init.d/celeryd
RUN chmod 755 /etc/init.d/celerybeat
RUN chmod 640 /etc/default/celeryd

COPY ./docker/celery-flower/entry.sh /usr/src/app
RUN chmod +x /usr/src/app/entry.sh

ENTRYPOINT ["/usr/src/app/entry.sh"]
