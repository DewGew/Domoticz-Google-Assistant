# Domoticz-Google-Assistant

Based on the home assistant implementation: https://github.com/home-assistant/home-assistant/tree/dev/homeassistant/components/google_assistant and https://github.com/actions-on-google/smart-home-nodejs

Required:
- Public IP
- python >= 3.5
- reverse proxy for establishing secure connection (aog itself provides currently only unsecure one - http only)

Aog delivers: 
- the oauth authorization and smarthome endpoint for the google assistant
- OnOff, Brightness, Scene and OpenClose traits, rest to be done...
Please feel free to modify it, extend and improve


Before first launch, Actions on Google and config.py must be modified properly:
```
PORT_NUMBER = 3030 -> port number for the Domoticz-Google-Assistant server

SMARTHOMEPROVIDERGOOGLECLIENTID = 'AxqqWpwYj4' - Client ID
SMARTHOMEPROVIDEGOOGLECLIENTSECRET = '0KUYN5ExD62QOsWCO8zoFSS_' - Client secret
SMARTHOMEPROVIDERAPIKEY = 'zOzaSyBu5Y8W7EiHvO1eyPmOAtZRxM9GaLP_uLA' -> Request Sync API

DOMOTICZ_URL='http://[DOMOTICZ_IP]:[PORT]'
U_NAME_DOMOTICZ = 'domoticz user name'
U_PASSWD_DOMOTICZ = 'domoticz user password'

#oauth credentials -> required for app linking
U_NAME = 'username'
U_PASSWD = 'password'
```
## Setup Instructions
- Use the [Actions on Google Console](https://console.actions.google.com/) to add a new project with a name of your choosing and click     - Create Project.
  - Click Home Control, then click Smart Home.
  - On the left navigation menu under SETUP, click on Invocation.
  - Add your App's name. Click Save.
  - Click Save.

- Add Credentials
  - Navigate to the [Google Cloud Console API Manager](https://console.cloud.google.com/apis/credentials) for your project id.
  - Click 'Create credentials'
  - Click 'OAuth client ID'
  - Choose 'other'
  - Add name e.g. 'SMARTHOMEPROVIDERGOOGLECLIENTID'
  - Copy the client ID shown and insert it in `SMARTHOMEPROVIDERGOOGLECLIENTID` in config.py
  - Copy the client secret shown and insert it in `SMARTHOMEPROVIDEGOOGLECLIENTSECRET`in config.py

- Add Request Sync

  The Request Sync feature allows a cloud integration to send a request to the Home Graph to send a new SYNC request.
  - Navigate to the [Google Cloud Console API Manager](https://console.cloud.google.com/apis/credentials) for your project id.
  - Enable the HomeGraph API. This will be used to request a new sync and to report the state back to the HomeGraph.
  - Click Credentials
  - Click 'Create credentials'
  - Click 'API key'
  - Copy the API key shown and insert it in `SMARTHOMEPROVIDERAPIKEY` in config.py.

- Navigate back to the [Actions on Google Console](https://console.actions.google.com/).
  - On the left navigation menu under BUILD, click on Actions. Click on Add Your First Action and choose your app's language(s).
    Enter the URL for fulfillment, e.g. https://[YOUR REVERSE PROXY URL]/smarthome, click Done.
  - On the left navigation menu under ADVANCED OPTIONS, click on Account Linking.
  - Select No, I only want to allow account creation on my website. Click Next.
  - For Linking Type, select OAuth.
  - For Grant Type, select 'Authorization Code' for Grant Type.
  - Under Client Information, enter the client ID and secret from earlier.
  - Change Authorization URL to https://[YOUR REVERSE PROXY URL]/oauth (replace with your actual URL).
  - Change Token URL to https://[YOUR REVERSE PROXY URL]/token (replace with your actual URL).
  In the Configure your client section:
  - Do NOT check Google to transmit clientID and secret via HTTP basic auth header.
  - Click ‘Save’ at the top right corner, then click ‘Test’ to generate a new draft version of the Test App.
  
## Starting Domoticz-Google-Assistant server:
```
python3 Domoticz-Google-Assistant
```
## Force devices sync
```
https://[YOUR REVERSE PROXY URL]/sync
```
## Run as service for autorun at startup
Open terminal or putty.
```
cd /etc/systemd/system/
sudo nano dzga.service
```
Add this in nano:
```
Description=Domoticz-Google-Assistant Service
After=multi-user.target
Conflicts=getty@tty1.service

[Service]
Type=simple
ExecStart=/usr/bin/python3 /home/${USER}/Domoticz-Google-Assistant/
StandardInput=tty-force

[Install]
WantedBy=multi-user.target
```
Then ctrl-x save and close.
Enable service:
```
 sudo systemctl enable dzga.service
 sudo systemctl start dzga.service
```
