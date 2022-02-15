FROM continuumio/miniconda3:4.10.3

ARG APP_USER=appuser
RUN groupadd -r ${APP_USER} && useradd --no-log-init -r -g ${APP_USER} ${APP_USER}

RUN apt-get update --allow-releaseinfo-change -y
RUN apt-get upgrade --fix-missing -y
RUN apt-get install -y --fix-missing --no-install-recommends \
    python3-pip software-properties-common build-essential \
    cmake sqlite3 gfortran python-dev && \
    pip install -U pip

WORKDIR /src/cts_app
COPY . /src/cts_app

RUN conda create --name pyenv python=3.9
RUN conda config --add channels conda-forge
RUN conda run -n pyenv --no-capture-output pip install -r /src/cts_app/requirements.txt
RUN conda install -n pyenv uwsgi

COPY uwsgi.ini /etc/uwsgi/
RUN chown -R www-data:www-data /src/cts_app

ENV DJANGO_SETTINGS_MODULE "settings"
EXPOSE 8080

ENV PYTHONPATH="/src:/src/cts_app:${PYTHONPATH}"
ENV PATH="/src:/src/cts_app:${PATH}"
#USER ${APP_USER}:${APP_USER}

CMD ["conda", "run", "-n", "pyenv", "--no-capture-output", "sh", "/src/cts_app/docker-start.sh"]