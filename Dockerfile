# Dockerfile for Domoticz-Google-Assistant

# Update Software repository
RUN apk add --update --no-cache git

ARG COMMIT_ID
RUN cd / && \
    git clone https://github.com/DewGew/Domoticz-Google-Assistant && \
    cp ./Domoticz-Google-Assistant/requirements/pip-requirements.txt requirements.txt

#Copy configuration
COPY apk-requirements.txt /Domoticz-Google-Assistant/requirements/apk-requirements.txt
COPY config.yaml /Domoticz-Google-Assistant/config/config.yaml
COPY smart-home-key.json /Domoticz-Google-Assistant/config/smart-home-key.json
 
# Configure Services and Port
CMD ["python3 Domoticz-Google-Assistant"]
 
EXPOSE 3030
