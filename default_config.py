# -*- coding: utf-8 -*-
# Default config file

#Http server port
PORT_NUMBER = 3030

#Set your Credentials here
SMARTHOMEPROVIDERGOOGLECLIENTID = 'sidjhfer87y'
SMARTHOMEPROVIDEGOOGLECLIENTSECRET = 'bfuosydgrf83ye'
SMARTHOMEPROVIDERAPIKEY = 'uwyte6514325r'

#Domoticz settings
DOMOTICZ_URL='http://192.168.1.251:8080'
U_NAME_DOMOTICZ = 'user_name'
U_PASSWD_DOMOTICZ = 'passwd'
DOMOTICZ_SWITCH_PROTECTION_PASSWD = '2774' # Only works with numbers as protection password in domoticz
# Set to 'DOMOTICZ_SWITCH_PROTECTION_PASSWD = False' if not needed

#Oauth credentials
U_NAME = 'oauth_user_name'
U_PASSWD = 'oauth_passwd'

#Ligths, switches, media, etc. are using domoticz's "Light/Switch" type.
#So to differentiate them additionaly image names are used.
IMAGE_SWITCH = ['WallSocket']
IMAGE_LIGHT = ['Light']
#'Speaker'
#'Media'

#Additional nicknames and room configuration
DEVICE_CONFIG = {
    '135' : {
            'nicknames' : ['Kitchen Blind One'],
            'room' : 'Kitchen' ,
            'ack' : True},
    '150' : {
            'nicknames' : ['Dining Room Light'],
            'room' : 'Dining Room'},
    '180' : {
            'nicknames' : ['Simon Printer'],
            'room' : 'Simon',
            'ack' : False}          
}

SCENE_CONFIG = {
    '3' : {
            'nicknames' : ['Blinders']
            },
    '5' : {
            'nicknames' : ['Test'] },    
}


#Hardcoded values - do not modify it!
SESSION_TIMEOUT = 3600
AUTH_CODE_TIMEOUT = 600
HOMEGRAPH_URL = 'https://homegraph.googleapis.com/'
REQUEST_SYNC_BASE_URL = HOMEGRAPH_URL + 'v1/devices:requestSync'
DOMOTICZ_GET_ALL_DEVICES_URL = DOMOTICZ_URL + '/json.htm?type=devices&filter=all&used=true'
DOMOTICZ_GET_ONE_DEVICE_URL = DOMOTICZ_URL + '/json.htm?type=devices&rid='
DOMOTICZ_GET_SCENES_URL = DOMOTICZ_URL + '/json.htm?type=scenes'

#https://developers.google.com/actions/smarthome/guides/
PREFIX_TYPES = 'action.devices.types.'
TYPE_LIGHT = PREFIX_TYPES + 'LIGHT'
TYPE_SWITCH = PREFIX_TYPES + 'SWITCH'
TYPE_VACUUM = PREFIX_TYPES + 'VACUUM'
TYPE_SCENE = PREFIX_TYPES + 'SCENE'
TYPE_FAN = PREFIX_TYPES + 'FAN'
TYPE_THERMOSTAT = PREFIX_TYPES + 'THERMOSTAT'
TYPE_LOCK = PREFIX_TYPES + 'LOCK'
TYPE_BLINDS = PREFIX_TYPES + 'BLINDS'
TYPE_SCREEN = PREFIX_TYPES + 'SCREEN'
TYPE_DOOR = PREFIX_TYPES + 'DOOR'

# Error codes used for SmartHomeError class
# https://developers.google.com/actions/smarthome/create-app#error_responses
ERR_DEVICE_OFFLINE = "deviceOffline"
ERR_DEVICE_NOT_FOUND = "deviceNotFound"
ERR_VALUE_OUT_OF_RANGE = "valueOutOfRange"
ERR_NOT_SUPPORTED = "notSupported"
ERR_PROTOCOL_ERROR = 'protocolError'
ERR_UNKNOWN_ERROR = 'unknownError'
ERR_FUNCTION_NOT_SUPPORTED = 'functionNotSupported'
ERR_CHALLENGE_NEEDED = 'challengeNeeded'
ERR_WRONG_PIN = 'pinIncorrect'

groupDOMAIN = 'Group'
sceneDOMAIN = 'Scene'
lightDOMAIN = 'Light/Switch'
switchDOMAIN = 'Switch'
blindsDOMAIN = 'Blinds'
screenDOMAIN = 'Screen'
climateDOMAIN = 'Thermostat'
tempDOMAIN = 'Temp'
lockDOMAIN = 'Door Lock'
invlockDOMAIN = 'Door Lock Inverted'
colorDOMAIN = 'Color Switch'

attribBRIGHTNESS = 1
attribTHERMSTATSETPOINT = 1
attribCOLOR = 1

#Todo... dynamic tokens handling/generation if needed
Auth = {
    'clients': {
        SMARTHOMEPROVIDERGOOGLECLIENTID: {
          'clientId':       SMARTHOMEPROVIDERGOOGLECLIENTID,
          'clientSecret':   SMARTHOMEPROVIDEGOOGLECLIENTSECRET,
        },
    },
    'tokens': {
        'ZsokmCwKjdhk7qHLeYd2': {
            'uid': '1234',
            'accessToken': 'ZsokmCwKjdhk7qHLeYd2',
            'refreshToken': 'ZsokmCwKjdhk7qHLeYd2',
            'userAgentId': '1234',
        },
    },
    'users': {
        '1234': {
            'uid': '1234',
            'name': U_NAME,
            'password': U_PASSWD,
            'tokens': ['ZsokmCwKjdhk7qHLeYd2'],
        },
    },
    'usernames': {
        U_NAME: '1234',
    }
}

