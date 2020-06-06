FROM python:alpine3.7

# Enable for gcc issues on requirements install issues
# RUN apk add build-base

COPY . /app
WORKDIR /app

RUN python -m pip install --upgrade pip
RUN python -m pip install /app

CMD python -m PROJECT_NAME
