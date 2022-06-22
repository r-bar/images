ARG ALPINE_VERSION=3.16

FROM alpine:${ALPINE_VERSION}
# darwin, linux, windows
ARG OS=linux
# amd64, arm64, armv6, armv7
ARG ARCH=amd64
ARG VERSION=0.7.2
RUN echo curl -L --output /usr/local/bin/jsonnet-language-server https://github.com/grafana/jsonnet-language-server/releases/download/v${VERSION}/jsonnet-language-server_${VERSION}_${OS}_${ARCH}
ADD https://github.com/grafana/jsonnet-language-server/releases/download/v${VERSION}/jsonnet-language-server_${VERSION}_${OS}_${ARCH} /usr/local/bin/jsonnet-language-server
RUN chmod +x /usr/local/bin/jsonnet-language-server
ENTRYPOINT ["/usr/local/bin/jsonnet-language-server"]
