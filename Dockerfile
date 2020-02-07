# Dockerfile for Domoticz-Google-Assistant
#
# Build image:
#   docker build -t domoticz-google-assistant ./Domoticz-Google-Assistant
# Dockerize dzga (Run container in background and print container ID):
#   docker run -d --name dzga -p 3030:3030 domoticz-google-assistant
# Start dockerized dzga container:
#   docker start dzga
# Stop dockerized dzga container:
#   docker stop dzga

# Install minimal Python 3.
FROM jfloff/alpine-python:3.7-slim

# Install Software
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
