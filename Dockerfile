# FROM mambaorg/micromamba:2.5-alpine3.22
FROM python:3.13-slim

ENV APP_USER=www-data
ENV CONDA_ENV="pyenv"

USER root

RUN apt-get update && \
    apt-get install -y \
        pkg-config \
        libcairo2-dev \
        python3-dev \
        gcc

WORKDIR /src/cts_app
COPY . /src/cts_app

RUN pip install -r requirements.txt

RUN find /opt/conda -name "*test.key" -delete || true
RUN find /opt/conda/ -name 'test.key' -delete || true
RUN find /opt/conda/ -name 'localhost.key' -delete || true
RUN find /opt/conda/ -name 'server.pem' -delete || true
RUN find /opt/conda/ -name 'client.pem' -delete || true
RUN find /opt/conda/ -name 'password_protected.pem' -delete || true

# RUN find /opt/conda/ -type d -name "test" -exec find {} -type f -name "*.pem" -delete \; || true
RUN find /opt/conda/ -type d -name "test" -exec sh -c 'find "{}" -type f -name "*.pem" -delete' \; || true

# ------------------------- #

COPY uwsgi.ini /etc/uwsgi/
RUN chown -R $APP_USER:$APP_USER /src
RUN chmod 755 /src/cts_app/docker-start.sh

ENV DJANGO_SETTINGS_MODULE "settings"
EXPOSE 8080

ENV PYTHONPATH="/src:/src/cts_app:${PYTHONPATH}"
ENV PATH="/src:/src/cts_app:${PATH}"

USER $APP_USER

CMD ["sh", "/src/cts_app/docker-start.sh"]
# ENV START_COMMAND="micromamba run -n $CONDA_ENV sh docker-start.sh"
# CMD ${START_COMMAND}
