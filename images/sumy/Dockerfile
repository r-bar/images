FROM python:3.9
ARG VERSION=0.8.1
RUN pip install sumy==$VERSION numpy
RUN python -c 'import nltk; nltk.download("punkt")'
ENTRYPOINT ["sumy"]
