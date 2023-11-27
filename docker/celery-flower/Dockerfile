FROM python:3.10-alpine
EXPOSE 5555

ENV DEBIAN_FRONTEND noninteractive
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV LC_ALL C.UTF-8
ENV LANG C.UTF-8

RUN apt-get update && apt-get -y upgrade
RUN apt-get install -y gcc
RUN apt-get install -y g++
RUN apt-get install -y build-essential
RUN apt-get install -y wget

USER root
RUN useradd -ms /bin/bash celery
RUN usermod -a -G celery celery
RUN usermod -a -G celery root

WORKDIR /usr/src/app
COPY ./ ./

RUN RUN pip install poetry
RUN poetry config virtualenvs.create false && \
    poetry install --no-interaction --no-ansi


COPY ./docker/celery/celeryd /etc/init.d/
COPY ./docker/celery/celerybeat /etc/init.d/
COPY ./docker/celery/config/celeryd /etc/default/
RUN ["chmod", "755", "/etc/init.d/celeryd"]
RUN ["chmod", "755", "/etc/init.d/celerybeat"]
RUN ["chmod", "640", "/etc/default/celeryd"]


RUN ["chmod", "+x", "./docker/celery-flower/entry.sh"]
ENTRYPOINT ["./docker/celery-flower/entry.sh"]