# -*- coding: utf-8 -*-

from config import (SMARTHOMEPROVIDERGOOGLECLIENTID, SMARTHOMEPROVIDEGOOGLECLIENTSECRET, U_NAME, U_PASSWD, 
                    DOMOTICZ_URL, DOMOTICZ_ROOMPLAN)
                    
"""Constants for Google Assistant."""
HOMEGRAPH_URL = 'https://homegraph.googleapis.com/'
REQUEST_SYNC_BASE_URL = HOMEGRAPH_URL + 'v1/devices:requestSync'

SESSION_TIMEOUT = 3600
AUTH_CODE_TIMEOUT = 600

DOMOTICZ_GET_ALL_DEVICES_URL = DOMOTICZ_URL + '/json.htm?type=devices&plan=' + DOMOTICZ_ROOMPLAN + '&filter=all&used=true'
DOMOTICZ_GET_ONE_DEVICE_URL = DOMOTICZ_URL + '/json.htm?type=devices&rid='
DOMOTICZ_GET_SCENES_URL = DOMOTICZ_URL + '/json.htm?type=scenes'
DOMOTICZ_GET_SETTINGS_URL = DOMOTICZ_URL + '/json.htm?type=settings'
DOMOTICZ_GET_CAMERAS_URL = DOMOTICZ_URL + '/json.htm?type=cameras'

#https://developers.google.com/actions/smarthome/guides/
PREFIX_TYPES = 'action.devices.types.'
TYPE_LIGHT = PREFIX_TYPES + 'LIGHT'
TYPE_SWITCH = PREFIX_TYPES + 'SWITCH'
TYPE_OUTLET = PREFIX_TYPES + 'OUTLET'
TYPE_VACUUM = PREFIX_TYPES + 'VACUUM'
TYPE_SCENE = PREFIX_TYPES + 'SCENE'
TYPE_FAN = PREFIX_TYPES + 'FAN'
TYPE_THERMOSTAT = PREFIX_TYPES + 'THERMOSTAT'
TYPE_LOCK = PREFIX_TYPES + 'LOCK'
TYPE_BLINDS = PREFIX_TYPES + 'BLINDS'
TYPE_SCREEN = PREFIX_TYPES + 'SCREEN'
TYPE_DOOR = PREFIX_TYPES + 'DOOR'
TYPE_MEDIA = PREFIX_TYPES + 'TV'
TYPE_SECURITY = PREFIX_TYPES + 'SECURITYSYSTEM'
TYPE_SPEAKER = PREFIX_TYPES + 'SPEAKER'
TYPE_CAMERA = PREFIX_TYPES + 'CAMERA'

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
ERR_ALREADY_IN_STATE = 'alreadyInState'

groupDOMAIN = 'Group'
sceneDOMAIN = 'Scene'
lightDOMAIN = 'Light/Switch'
switchDOMAIN = 'Switch'
outletDOMAIN = 'Outlet'
blindsDOMAIN = 'Blinds'
screenDOMAIN = 'Screen'
climateDOMAIN = 'Thermostat'
tempDOMAIN = 'Temp'
lockDOMAIN = 'DoorLock'
invlockDOMAIN = 'DoorLockInverted'
colorDOMAIN = 'ColorSwitch'
mediaDOMAIN = 'Media'
securityDOMAIN = 'Security'
pushDOMAIN = 'Push'
speakerDOMAIN = 'Speaker'
cameraDOMAIN = 'Camera'

ATTRS_BRIGHTNESS = 1
ATTRS_THERMSTATSETPOINT = 1
ATTRS_COLOR = 2
ATTRS_COLOR_TEMP = 3
ATTRS_PERCENTAGE = 1

DOMOTICZ_TO_GOOGLE_TYPES = {
    groupDOMAIN: TYPE_SWITCH,
    sceneDOMAIN: TYPE_SCENE,
    lightDOMAIN: TYPE_LIGHT,
    switchDOMAIN: TYPE_SWITCH,
    outletDOMAIN: TYPE_OUTLET,
    blindsDOMAIN: TYPE_BLINDS,
    screenDOMAIN: TYPE_SCREEN,
    climateDOMAIN: TYPE_THERMOSTAT,
    tempDOMAIN: TYPE_THERMOSTAT,
    lockDOMAIN: TYPE_LOCK,
    invlockDOMAIN: TYPE_LOCK,
    colorDOMAIN: TYPE_LIGHT,
    mediaDOMAIN: TYPE_MEDIA,
    securityDOMAIN: TYPE_SECURITY,
    pushDOMAIN: TYPE_SWITCH,
    speakerDOMAIN: TYPE_SPEAKER,
    cameraDOMAIN: TYPE_CAMERA,
}

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
