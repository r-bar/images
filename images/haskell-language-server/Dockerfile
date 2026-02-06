ARG UBUNTU_VERSION=22.04
ARG GHC_VERSION=9.2.1
ARG HLS_VERSION=1.7.0.0
FROM docker.io/library/ubuntu:$UBUNTU_VERSION

VOLUME /workdir
WORKDIR /workdir
ENTRYPOINT ["haskell-language-server-wrapper", "--lsp"]

RUN apt-get update && apt-get install -y curl build-essential libncurses-dev
ADD https://get-ghcup.haskell.org /tmp/install.sh
RUN BOOTSTRAP_HASKELL_NONINTERACTIVE=1 sh /tmp/install.sh

ENV PATH=/root/.cabal/bin:/root/.ghcup/bin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin

RUN ghcup install ghc ${GHC_VERSION}
RUN ghcup set ghc ${GHC_VERSION}
RUN ghcup install hls ${HLS_VERSION}
RUN ghcup set hls ${HLS_VERSION}
