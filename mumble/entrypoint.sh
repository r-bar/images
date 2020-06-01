#!/bin/sh

if ![ -z ${SUPERUSER_PASSWORD+x} ]; then
  murmurd -supw $SUPERUSER_PASSWORD
fi

echo ${TIMEZONE:-UTC} > /etc/timezone

# ensure that any mounted volume is owned by the mumble-server user
chown -R mumble-server: /var/lib/mumble-server

murmurd -ini /etc/mumble-server.ini -fg
