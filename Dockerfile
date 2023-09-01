FROM python:3.10

ENV PYTHONUNBUFFERED 1

# Set the working directory to /code/
WORKDIR /code/

# Copy the project files from the build context into the container at /code/
COPY . /code/

# Install Poetry
RUN pip install poetry

# Install project dependencies using Poetry
RUN poetry install --no-interaction --no-ansi

# Expose port
EXPOSE 8000
