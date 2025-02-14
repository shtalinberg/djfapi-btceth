# Базовий образ Python
FROM python:3.12

ARG ENV
SHELL ["/bin/bash", "-c"]

# set working directory
WORKDIR /home/code

# install netcat (nc)
RUN apt-get update && apt-get install -y netcat-openbsd postgresql-client libpq-dev  && rm -rf /var/lib/apt/lists/*

# set environment variables
ENV PYTHONIOENCODING UTF-8
# Prevents Python from writing pyc files to disc
ENV PYTHONDONTWRITEBYTECODE 1
# Prevents Python from buffering stdout and stderr
ENV PYTHONUNBUFFERED 1

RUN mkdir logs
RUN mkdir -p /data/media
RUN mkdir -p /data/static

# install dependencies
COPY requirements/ /tmp/requirements/
RUN pip install --no-cache-dir -r /tmp/requirements/local.pip

#copy source code
COPY ./src ./src

RUN echo "ENV=${ENV}"
RUN echo pwd
RUN cp ./src/djproject/settings/example_tpls/template.docker.${ENV}.py /home/code/src/djproject/settings/local.py

COPY docker/entrypoint.sh /home/code/docker/entrypoint.sh

# Додаємо виконуваний дозвіл на entrypoint
RUN chmod +x /home/code/docker/entrypoint.sh

# Відкриваємо порт 8888
EXPOSE 8888
