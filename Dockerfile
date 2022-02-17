# FROM continuumio/miniconda3:4.10.3
# FROM python:3.10.2-alpine
# FROM python:3.10.2-slim
FROM python:3.8-slim

ARG APP_USER=appuser
RUN groupadd -r ${APP_USER} && useradd --no-log-init -r -g ${APP_USER} ${APP_USER}

RUN apt-get update --allow-releaseinfo-change -y
RUN apt-get upgrade --fix-missing -y
# RUN apt-get install -y --fix-missing --no-install-recommends \
#     python3-pip software-properties-common build-essential \
#     cmake sqlite3 gfortran python-dev && \
#     pip install -U pip
RUN apt-get install -y --fix-missing --no-install-recommends \
    software-properties-common build-essential \
    cmake python-dev

WORKDIR /src/cts_app
COPY . /src/cts_app

# RUN conda create --name pyenv python=3.9
# RUN conda config --add channels conda-forge
# RUN conda run -n pyenv --no-capture-output pip install -r /src/cts_app/requirements.txt
# RUN conda install -n pyenv uwsgi

RUN pip install -r /src/cts_app/requirements.txt
RUN pip install uwsgi

COPY uwsgi.ini /etc/uwsgi/
RUN chown -R www-data:www-data /src/cts_app
RUN chmod 755 /src/cts_app/docker-start.sh

ENV DJANGO_SETTINGS_MODULE "settings"
EXPOSE 8080

ENV PYTHONPATH="/src:/src/cts_app:${PYTHONPATH}"
ENV PATH="/src:/src/cts_app:${PATH}"
#USER ${APP_USER}:${APP_USER}

# CMD ["conda", "run", "-n", "pyenv", "--no-capture-output", "sh", "/src/cts_app/docker-start.sh"]
# CMD ["sh", "/src/cts_app/docker-start.sh"]
CMD ["ls", "-l", "/src/cts_app"]