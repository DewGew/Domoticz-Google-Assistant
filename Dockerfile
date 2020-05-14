# Dockerfile for Domoticz-Google-Assistant

# Install minimal Python 3.
FROM arm32v6/python:3.7-alpine

RUN mkdir -p config

COPY *.py /
COPY *.html /
COPY requirements/pip-requirements.txt /requirements.txt
RUN pip install --no-cache-dir -r /requirements.txt
# Create volume
VOLUME /config

# Configure Services and Port
CMD ["python3 /__main__.py"]

EXPOSE 3030
