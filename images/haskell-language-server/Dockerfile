FROM alpine:3.16

VOLUME /workdir
WORKDIR /workdir
ENTRYPOINT ["haskell-language-server-wrapper", "--lsp"]

RUN apk add curl build-base ncurses-dev
ADD https://get-ghcup.haskell.org /tmp/install.sh
RUN BOOTSTRAP_HASKELL_NONINTERACTIVE=1 sh /tmp/install.sh

ENV PATH=/root/.cabel/bin:/root/.gchup/bin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin
