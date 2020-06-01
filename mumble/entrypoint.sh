#!/bin/sh

if ![ -z ${SUPERUSER_PASSWORD+x} ]; then
  murmurd -supw $SUPERUSER_PASSWORD
fi

echo ${TIMEZONE:-UTC} > /etc/timezone

murmurd -ini /etc/mumble-server.ini -fg
