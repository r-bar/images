FROM ubuntu:24.04

VOLUME /var/lib/mumble-server

ENV SUPERUSER_PASSWORD=""
ENV TIMEZONE=UTC
ENV CONFIG=/etc/mumble-server.ini

RUN apt-get update
RUN apt-get install -y mumble-server

# moved for easier mounting, symlink old location
RUN mkdir /etc/mumble \
  && mv /etc/mumble-server.ini /etc/mumble/config.ini \
  && ln -s /etc/mumble/config.ini /etc/mumble-server.ini

COPY entrypoint.sh /entrypoint.sh

CMD [/entrypoint.sh]
