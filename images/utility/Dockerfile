FROM python:3.10-alpine
RUN apk update --no-cache \
  && apk add --no-progress --no-cache \
    curl \
    git \
    make \
    jq \
    aws-cli \
    ;
RUN pip install pyyaml requests
#RUN echo "#\!/bin/ash\n\$@" > /entrypoint.sh && chmod +x /entrypoint.sh
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh
ENTRYPOINT ["/entrypoint.sh"]
