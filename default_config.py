# -*- coding: utf-8 -*-
# Default config file

#Http server port
PORT_NUMBER = 3030

#Set your Credentials here
SMARTHOMEPROVIDERGOOGLECLIENTID = 'sidjhfer87y'
SMARTHOMEPROVIDEGOOGLECLIENTSECRET = 'bfuosydgrf83ye'
SMARTHOMEPROVIDERAPIKEY = 'uwyte6514325r'

#Oauth credentials
U_NAME = 'oauth_user_name'
U_PASSWD = 'oauth_passwd'

#Domoticz settings
DOMOTICZ_URL='http://192.168.1.251:8080'
U_NAME_DOMOTICZ = 'user_name'
U_PASSWD_DOMOTICZ = 'passwd'
#Idx of Room plan. 0 is all devices.
DOMOTICZ_ROOMPLAN = '0'
#Set to 'DOMOTICZ_SWITCH_PROTECTION_PASSWD = False' if ask for pin function is not needed
DOMOTICZ_SWITCH_PROTECTION_PASSWD = '331122' # Only works with numbers as protection password in domoticz

#Report low battery 
LOW_BATTERY_LIMIT = 9

#Ligths, switches, media, etc. are using domoticz's "Light/Switch" type.
#So to differentiate them additionaly image names are used.
IMAGE_SWITCH = ['Generic']
IMAGE_LIGHT = ['Light']
IMAGE_MEDIA = ['Media', 'TV']
IMAGE_OUTLET = ['WallSocket']
IMAGE_SPEAKER = ['Speaker']

#Additional nicknames and room configuration
DEVICE_CONFIG = {
    '135' : {
        'nicknames' : ['Kitchen Blind One'],
        'room' : 'Kitchen' ,
        'ack' : True,
        },
    '150' : {
        'nicknames' : ['Dining Room Light'],
        'room' : 'Dining Room',
        },
    '180' : {
        'nicknames' : ['Simon Printer'],
        'room' : 'Simon',
        'ack' : False,
        },          
}

SCENE_CONFIG = {
    '3' : {
        'nicknames' : ['Blinders']},
    '5' : {
        'nicknames' : ['Test']},    
}

# User-friendly name for the level in your language..
# See: https://developers.google.com/actions/smarthome/traits/#supported-languages
ARMHOME = {
    "level_synonym": ["låg säkerhet", "Level 1", "hemmaläge", "SL1"], # Custom levelnames
    "lang": "sv" # langauge
    }
          
ARMAWAY = {
    "level_synonym": ["hög säkerhet", "Level 2", "bortaläge", "SL2"], # Custom levelnames
    "lang": "sv" # language
    }

# Stream security camera to chromecast. Supports hls, dash, smooth streaming, Progressive MP4 urls.
# More info: https://developers.google.com/actions/smarthome/traits/camerastream#video-formats
# You need a to convert your video url to one of above. Try with ffmpeg or with 
# a surveillance software system. Try out http://shinobi.video
CAMERA_STREAM = False

DOMOTICZ_IDX_CAMERAURL = {
    '382' : 'https://content.jwplatform.com/manifests/yp34SRmf.m3u8', 
    '392' : 'http://user:password@192.168.1.102:8080/mp4/cctv/camera2/s.mp4',
    }
