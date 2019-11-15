# -*- coding: utf-8 -*-
# Default config file

#Http server port
PORT_NUMBER = 3030

#Set your Credentials here
SMARTHOMEPROVIDERGOOGLECLIENTID = 'sampleClientId'
SMARTHOMEPROVIDEGOOGLECLIENTSECRET = 'sampleClientSecret'
SMARTHOMEPROVIDERAPIKEY = 'homegraph_api_key_here'

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
#Nicknames, rooms and ack can be set in the Domoticz user interface.
#Simply put the device configuration in the device description, in a section between 'voicecontrol' tags like:
# <voicecontrol>
# nicknames = Kitchen Blind One, Left Blind, Blue Blind
# room = Kitchen
# ack = True
# </voicecontrol>

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
# In domoticz you need to attach a switch to your camera (create a switch then in Settings/Camera, add the switch to the camera)
CAMERA_STREAM = False

DOMOTICZ_IDX_CAMERAURL = {
    '382' : 'https://content.jwplatform.com/manifests/yp34SRmf.m3u8', 
    '392' : 'http://user:password@192.168.1.102:8080/mp4/cctv/camera2/s.mp4',
    }
