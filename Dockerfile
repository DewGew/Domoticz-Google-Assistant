# Dockerfile for Domoticz-Google-Assistant

# Install minimal Python 3.
FROM jfloff/alpine-python:3.7-slim

# Update Software repository
RUN cd / && \
    apk add  --no-cache --virtual=build-dependencies \
                git \
                libffi-dev \
                libressl-dev && \
    git clone https://github.com/DewGew/Domoticz-Google-Assistant.git dzGA && \
    cp /dzGA/requirements/pip-requirements.txt /requirements.txt

# Create volume
VOLUME /dzGA/config

# Configure Services and Port
CMD ["python3 /dzGA/__main__.py"]

EXPOSE 3030
