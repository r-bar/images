ARG VERSION=latest

FROM ghcr.io/advplyr/audiobookshelf:${VERSION}

ARG USER=audiobookshelf
ARG GROUP=audiobookshelf
ARG UID=1000
ARG GID=1000
ARG HOME=/home/audiobookshelf

RUN addgroup -g ${GID} ${GROUP} \
    && adduser -h ${HOME} -u ${UID} -g ${GID} -D -s /bin/ash ${USER} \
    ;

USER ${USER}:${GROUP}
