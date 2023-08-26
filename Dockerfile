FROM python:3.10

ENV PYTHONUNBUFFERED 1

COPY poetry.lock pyproject.toml /code/
USER root

WORKDIR /code/
RUN pip3 install poetry

RUN poetry install
COPY . /code/
EXPOSE 8000