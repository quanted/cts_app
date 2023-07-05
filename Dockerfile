# FROM python:3.10-alpine
FROM python:3.10.12-slim

ENV APP_USER=www-data

# RUN adduser -S $APP_USER -G $APP_USER

# RUN apk add --update --no-cache \
#     build-base \
#     jpeg-dev \
#     zlib-dev \
#     libjpeg \
#     gettext \
#     py3-lxml \
#     py3-pillow \
#     openldap-dev \
#     python3-dev \
#     linux-headers \
#     && rm -rf /var/cache/apk/*

RUN apt-get update && \
    apt-get upgrade && \
    apt-get install -y build-essential

WORKDIR /src/cts_app
COPY . /src/cts_app

RUN pip install -r /src/cts_app/requirements.txt
RUN pip install uwsgi
RUN pip install --upgrade pip

COPY uwsgi.ini /etc/uwsgi/
RUN chown -R $APP_USER:$APP_USER /src/cts_app
RUN chmod 755 /src/cts_app/docker-start.sh

ENV DJANGO_SETTINGS_MODULE "settings"
EXPOSE 8080

ENV PYTHONPATH="/src:/src/cts_app:${PYTHONPATH}"
ENV PATH="/src:/src/cts_app:${PATH}"

USER $APP_USER

CMD ["sh", "/src/cts_app/docker-start.sh"]
