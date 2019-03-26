# Domoticz-Google-Assistant

Based on the home assistant implementation:
https://github.com/home-assistant/home- ... _assistant
and https://github.com/actions-on-google/smart-home-nodejs

Required:
- Public IP
- python >= 3.5
- reverse proxy for establishing secure connection (aog itself provides currently only unsecure one - http only)

Aog delivers: 
- the oauth authorization and smarthome endpoint for the google assistant
- OnOff, Brightness, Scene and OpenClose traits, rest to be done...
Please feel free to modify it, extend and improve


Before first launch, config.py must be modified properly:
```
PORT_NUMBER = 3030 -> port number for the aog server

SMARTHOMEPROVIDERGOOGLECLIENTID = 'AxqqWpwYj4' - Client ID issued by your Actions to Google, check actions on google configuration
SMARTHOMEPROVIDEGOOGLECLIENTSECRET = '0KUYN5ExD62QOsWCO8zoFSS_' - Client secret
SMARTHOMEPROVIDERAPIKEY = 'zOzaSyBu5Y8W7EiHvO1eyPmOAtZRxM9GaLP_uLA' -> https://github.com/actions-on-google/sm ... quest-sync

DOMOTICZ_URL='http://[DOMOTICZ_IP]:[PORT]'
U_NAME_DOMOTICZ = 'domoticz user name'
U_PASSWD_DOMOTICZ = 'domoticz user password'

#oauth credentials -> required for app linking
U_NAME = 'username'
U_PASSWD = 'password'
```
