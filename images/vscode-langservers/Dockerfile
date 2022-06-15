ARG NODE_VERSION=latest
ARG LANGSERVERS_VERSION=latest
FROM node:${NODE_VERSION}
RUN npm install --location global eslint vscode-langservers-extracted@${LANGSERVERS_VERSION}
RUN echo '#!/bin/sh' >> /entrypoint.sh \
  && echo '$@' >> /entrypoint.sh \
  && chmod +x /entrypoint.sh
ENTRYPOINT ["/entrypoint.sh"]
CMD []
