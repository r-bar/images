ARG PYTHON_VERSION=3.10-slim
ARG PYLSP_VERSION='==1.4.1'
FROM registry.barth.tech/docker.io/library/python:$PYTHON_VERSION
RUN pip install "python-lsp-server[all]${PYLSP_VERSION}"
VOLUME /venv /workdir
WORKDIR /workdir
COPY entrypoint.sh /entrypoint.sh
ENTRYPOINT ["/entrypoint.sh"]
