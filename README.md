# Domoticz-Google-Assistant

Standalone implementation. It means that you can put this server wherever you want, even on another machine. You need to setup a project in Actions on Google Console. You find instructions below.

Required:
- Public IP
- python >= 3.5
- reverse proxy for establishing secure connection (Domoticz-Google-Assistant itself provides currently only unsecure one - http only)

Domoticz-Google-Assistant delivers: 
- the oauth authorization and smarthome endpoint for the google assistant
- Two-factor authentication pin for domoticz protected devices (works best with english language)
- Acknowledgement with Yes or No. (works best with english language)
- Arm Disarm Securitypanel (works best with english language)
- On/Off, Brightness, Thermostat, Color Settings, speaker volume, Lock/Unlock, Scene and Open/Close
- Stream surveillance camera to chromecast

Please feel free to modify it, extend and improve

## Installation with git
NOTE: "${USER}" will automatically take your username. No need to change that. Just copy and paste.
```
cd /home/${USER}/
git clone https://github.com/DewGew/Domoticz-Google-Assistant
```
Rename default_config.py to config.py:
```
cd /home/${USER}/Domoticz-Google-Assistant
mv default_config.py config.py
```

Before first launch, [Actions on Google](https://github.com/DewGew/Domoticz-Google-Assistant/wiki/2.-Setup-Actions-on-Google) and config.py must be modified properly.
```
PORT_NUMBER = 3030 -> port number for the Domoticz-Google-Assistant server

SMARTHOMEPROVIDERGOOGLECLIENTID = 'AxqqWpwYj4'                      # Client ID
SMARTHOMEPROVIDEGOOGLECLIENTSECRET = '0KUYN5ExD62QOsWCO8zoFSS_'     # Client secret
SMARTHOMEPROVIDERAPIKEY = 'zOzaSyBu5Y8W7EiHvO1eyPmOAtZRxM9GaLP_uLA' # Request Sync API

#Oauth credentials -> required for app linking
U_NAME = 'oauth_username'
U_PASSWD = 'oauth_password'

DOMOTICZ_URL='http://[DOMOTICZ_IP]:[PORT]'
U_NAME_DOMOTICZ = 'domoticz_username'
U_PASSWD_DOMOTICZ = 'domoticz_password'
#Idx of Room plan. 0 is all devices.
DOMOTICZ_ROOMPLAN = '0'
# Set to 'DOMOTICZ_SWITCH_PROTECTION_PASSWD = False' if ask for pin function is not needed
DOMOTICZ_SWITCH_PROTECTION_PASSWD = '1234' # Only works with numbers as protection password in domoticz
```
##  Setup Actions on Google Console Instructions
- Use the [Actions on Google Console](https://console.actions.google.com/) to add a new project with a name of your choosing and click     - Create Project.
  - Click Home Control, then click Smart Home.
  - On the top menu click Develop, then on the left navigation menu click on Invocation.
  - Add your App's name. Click Save.
  - Click 'Save'.

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
  - On the top menu click Develop, then on the left navigation menu click on Actions.
    Enter the URL for fulfillment, e.g. `https://[YOUR REVERSE PROXY URL]/smarthome`, click Done.
  - On the left navigation menu under Account Linking.
  - Select No, I only want to allow account creation on my website.
  - For Linking Type, select OAuth.
  - For Grant Type, select 'Authorization Code' for Grant Type.
  - Under Client Information, enter the client ID and secret from earlier.
  - Change Authorization URL to `https://[YOUR REVERSE PROXY URL]/oauth` (replace with your actual URL).
  - Change Token URL to `https://[YOUR REVERSE PROXY URL]/token` (replace with your actual URL).  
  - Do NOT check 'Google to transmit clientID and secret via HTTP basic auth header'.
  - Click 'Save' at the top right corner, then click 'Test' to generate a new draft version of the Test App.
  
## Starting Domoticz-Google-Assistant server:
```
cd /home/${USER}/
python3 Domoticz-Google-Assistant
```
## Connect smart home devices to your Google Home device
- On your mobile device, open the Google Home app.
- On the Home tab, tap the “Add” quick action .
- Tap Set up a device
- Tap Have something already set up?
- Select your device app e.g: "[test]Your Appname"
- Login with Oauth credentials from config.py

## Share devices
If you want to allow other household users to control the devices:
- Go to the settings for the project you created in the [Actions on Google Console](https://console.actions.google.com/).
- Click `Test -> Simulator`, then click Share icon in the right top corner. Follow the on-screen instruction:
  - Add team members: Got to `Settings -> Permission`, click Add, type the new user’s e-mail address and choose `Project -> Viewer role`.
  - Copy and share the link with the new user.
  - When the new user opens the link with their own Google account, it will enable your draft test app under their account.
- Have the new user go to their Google Home app to add "[test]Your Appname" to their account. Login with Oauth credentials from config.py

## Stream camera to chromecast
Stream security camera to chromecast. Supports hls, dash, smooth streaming, Progressive MP4 urls. More info: https://developers.google.com/actions/smarthome/traits/camerastream#video-formats. You need a to convert your video url to one of above. Try with ffmpeg or with a surveillance software system. Try out http://shinobi.video.  
In domoticz you need to attach a switch to your camera (create a switch then in Settings/Camera, add the switch to the camera)

Example convert rtsp to hls or mp4 using ffmpeg:
```
ffmpeg -rtsp_transport tcp -i rtsp://admin:123456@192.168.0.218/live/ch1 \
  -acodec copy \
  -vcodec copy \
  -hls_wrap 40 \
  -flags -global_header \
  /var/www/html/cam/cam.m3u8
```
```
ffmpeg -rtsp_transport tcp -i rtsp://admin:123456@192.168.0.218/live/ch1 \
  -c:a aac \
  -vcodec copy \
  -f mp4 \
  -y \
  -flags -global_header \
  /var/www/html/cam/cam.mp4
```   
In config.py:
```
CAMERA_STREAM = True

DOMOTICZ_IDX_CAMERAURL = {
    '398' : 'http://your.web.server/cam/cam.m3u8',
    '396' : 'https://content.jwplatform.com/manifests/yp34SRmf.m3u8', 
    '392' : 'http://user:password@192.168.1.102:8080/mp4/cctv/camera2/s.mp4',
    }
```

## Device Settings
Nicknames, rooms and ack can be set in the Domoticz user interface. Simply put the device configuration in the device description, in a section between 'voicecontrol' tags like:
```
<voicecontrol>
nicknames = Kitchen Blind One, Left Blind, Blue Blind
room = Kitchen
ack = True
</voicecontrol>
```
Other parts of the description are ignored, so you can still leave other useful descriptions.
Every variable should be on a separate line.
If there is no such configuration in the Domoticz device it will still try the config.py.

## Useful commands
With `'ack' : True`:
>**User:** Turn on the dining room light.  
>**Google Assistant:** Turning on the dining room light. Are you sure?  
>**User:**	Yes.  
>**Google Assistant:** Turning on the dining room light.

Security device:
>**User:** Set the security system to armed away.  
>**Google Assistant:** Can I have your security code?  
>**User**: 1234  
>**Google Assistant:** Ok, arming the security system to armed away.

>**User**: Is my security system armed?  
>**Google Assistant:** The security system is armed to armed away.

Speaker volume:
>**User**: Set volume on living room speaker to 50%  
>**Google Assistant:** Sure

>**User**: Turn up the volume on living room speaker?  
>**Google Assistant:** Alright (Volume increases with 1%)

When a device has low battery:
>**User**: Lock front door.  
>**Google Assistant:** The front door lock has low battery. Locking the front door.

Stream front door camera to TV.
>**User**: Show front door camera on [Chromecast device name].  
>**Google**: Streaming front door on  [Chromecast device name].

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

[Unit]
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
## Update
```
cd /home/${USER}/Domoticz-Google-Assistant/
git pull
```
If needed, restart service:
```
sudo systemctl restart dzga.service
```
**Config.py will not be updated** but if there is any changes on the config file compare your file with default_config.py
