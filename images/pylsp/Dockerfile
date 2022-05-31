ARG PYTHON_VERSION=3.10
ARG PYLSP_VERSION='==1.4.1'
FROM registry.barth.tech/docker.io/library/python:$PYTHON_VERSION-slim
RUN pip install "python-lsp-server[all]${PYLSP_VERSION}"
VOLUME /venv /workspace
WORKDIR /workspace
ENTRYPOINT ["/usr/local/bin/python", "/usr/local/bin/pylsp"]
