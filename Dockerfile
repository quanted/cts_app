# ---- build stage (has shell, compiler, headers) ----
FROM dhi.io/python:3.14-dev AS build

USER root

# # gcc + python headers so uwsgi's wheel compiles
# RUN apt-get update && \
#     apt-get install -y --no-install-recommends gcc && \
#     rm -rf /var/lib/apt/lists/*


RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        gcc \
        libxrender1 \
        libxext6 && \
    rm -rf /var/lib/apt/lists/*


WORKDIR /src/cts_app
COPY . /src/cts_app

RUN pip install --prefix=/install -r requirements.txt

# make the installed packages importable in THIS stage so we can collectstatic
ENV PYTHONPATH="/install/lib/python3.14/site-packages:/src:/src/cts_app"
ENV PATH="/install/bin:${PATH}"
ENV DJANGO_SETTINGS_MODULE="settings"

COPY uwsgi.ini /etc/uwsgi/uwsgi.ini

# collect static at build time — runtime image has no shell to do it later.
# STATIC_ROOT in your settings must point somewhere under /src/cts_app.
RUN django-admin collectstatic --noinput

# normalize ownership to the runtime nonroot user (65532)
# RUN chown -R 65532:65532 /install /src/cts_app

# ---- runtime stage (distroless, nonroot, no shell) ----
FROM dhi.io/python:3.14

COPY --from=build --chown=65532:65532 /install /usr/local
COPY --from=build --chown=65532:65532 /src/cts_app /src/cts_app
COPY --from=build --chown=65532:65532 /etc/uwsgi /etc/uwsgi

COPY --from=build /usr/lib/x86_64-linux-gnu/libXrender.so.1* /usr/lib/x86_64-linux-gnu/
COPY --from=build /usr/lib/x86_64-linux-gnu/libXext.so.6* /usr/lib/x86_64-linux-gnu/
COPY --from=build /usr/lib/x86_64-linux-gnu/libX11.so.6* /usr/lib/x86_64-linux-gnu/
COPY --from=build /usr/lib/x86_64-linux-gnu/libxcb.so.1* /usr/lib/x86_64-linux-gnu/
COPY --from=build /usr/lib/x86_64-linux-gnu/libXau.so.6* /usr/lib/x86_64-linux-gnu/
COPY --from=build /usr/lib/x86_64-linux-gnu/libXdmcp.so.6* /usr/lib/x86_64-linux-gnu/

ENV DJANGO_SETTINGS_MODULE="settings"
# ENV PYTHONPATH="/src:/src/cts_app"
ENV PYTHONPATH="/usr/local/lib/python3.14/site-packages:/src:/src/cts_app"
ENV PATH="/src:/src/cts_app:${PATH}"

# no shell in this image — call python directly, not sh
ENTRYPOINT ["python", "/src/cts_app/entrypoint.py"]