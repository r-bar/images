ARG BASE_VERSION=trixie-slim
FROM debian:${BASE_VERSION}

ARG OPENCODE_VERSION
ARG OPENCODE_PACKAGE
ARG OPENCODE_ARCH

ADD "https://github.com/anomalyco/opencode/releases/download/${OPENCODE_VERSION}/opencode-${OPENCODE_PACKAGE}-${OPENCODE_ARCH}.tar.gz" "/opencode.tar.gz"
RUN tar xfz /opencode.tar.gz \
  && mv /opencode /usr/local/bin/opencode \
  && chmod +x /usr/local/bin/opencode \
  ;

VOLUME /workdir
WORKDIR /workdir

ENTRYPOINT ["/usr/local/bin/opencode"]
CMD []
