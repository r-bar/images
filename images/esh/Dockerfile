FROM ubuntu:latest
ARG VERSION=0.3.0
ADD https://github.com/jirutka/esh/archive/v$VERSION/esh-$VERSION.tar.gz esh-$VERSION.tar.gz
RUN tar -xzf esh-$VERSION.tar.gz esh-$VERSION/esh

FROM ubuntu:latest
ARG VERSION=0.3.0
COPY --from=0 /esh-$VERSION/esh /usr/bin/esh
ENTRYPOINT ["/usr/bin/esh"]
