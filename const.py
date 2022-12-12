# -*- coding: utf-8 -*-
                    
"""Constants for Google Assistant."""
VERSION = '1.22.24'
PUBLIC_URL = 'https://[your public url]'
CONFIGFILE = 'config/config.yaml'
LOGFILE = 'dzga.log'
KEYFILE = 'config/smart-home-key.json'

HOMEGRAPH_URL = "https://homegraph.googleapis.com/"
HOMEGRAPH_SCOPE = "https://www.googleapis.com/auth/homegraph"
HOMEGRAPH_TOKEN_URL = "https://accounts.google.com/o/oauth2/token"
REQUEST_SYNC_BASE_URL = HOMEGRAPH_URL + "v1/devices:requestSync"
REPORT_STATE_BASE_URL = HOMEGRAPH_URL + "v1/devices:reportStateAndNotification"

SESSION_TIMEOUT = 3600
AUTH_CODE_TIMEOUT = 600

DOMOTICZ_GET_ALL_DEVICES_URL = '/json.htm?type=devices&plan='
DOMOTICZ_GET_ONE_DEVICE_URL = '/json.htm?type=devices&rid='
DOMOTICZ_GET_SCENES_URL = '/json.htm?type=scenes'
DOMOTICZ_GET_SETTINGS_URL = '/json.htm?type=settings'
DOMOTICZ_GET_CAMERAS_URL = '/json.htm?type=cameras'
DOMOTICZ_GET_VERSION = '/json.htm?type=command&param=getversion'
DOMOTICZ_SEND_COMMAND = 'json.htm?type=command&param='

# https://developers.google.com/actions/smarthome/guides/
PREFIX_TYPES = 'action.devices.types.'
TYPE_AC_UNIT = PREFIX_TYPES + 'AC_UNIT'
TYPE_BATHTUB = PREFIX_TYPES + 'BATHTUB'
TYPE_BLINDS = PREFIX_TYPES + 'BLINDS'
TYPE_CAMERA = PREFIX_TYPES + 'CAMERA'
TYPE_COFFEE = PREFIX_TYPES + 'COFFEE_MAKER'
TYPE_COOKTOP = PREFIX_TYPES + 'COOKTOP'
TYPE_CURTAIN = PREFIX_TYPES + 'CURTAIN'
TYPE_DISHWASHER = PREFIX_TYPES + 'DISHWASHER'
TYPE_DOOR = PREFIX_TYPES + 'DOOR'
TYPE_DOORBELL = PREFIX_TYPES + 'DOORBELL'
TYPE_DRYER = PREFIX_TYPES + 'DRYER'
TYPE_FAN = PREFIX_TYPES + 'FAN'
TYPE_GARAGE = PREFIX_TYPES + 'GARAGE'
TYPE_GATE = PREFIX_TYPES + 'GATE'
TYPE_HEATER = PREFIX_TYPES + 'HEATER'
TYPE_KETTLE = PREFIX_TYPES + 'KETTLE'
TYPE_LIGHT = PREFIX_TYPES + 'LIGHT'
TYPE_LOCK = PREFIX_TYPES + 'LOCK'
TYPE_MEDIA = PREFIX_TYPES + 'TV'
TYPE_MICRO = PREFIX_TYPES + 'MICROWAVE'
TYPE_MOWER = PREFIX_TYPES + 'MOWER'
TYPE_OUTLET = PREFIX_TYPES + 'OUTLET'
TYPE_OVEN = PREFIX_TYPES + 'OVEN'
TYPE_RADIATOR = PREFIX_TYPES + 'RADIATOR'
TYPE_SCENE = PREFIX_TYPES + 'SCENE'
TYPE_SCREEN = PREFIX_TYPES + 'SCREEN'
TYPE_SECURITY = PREFIX_TYPES + 'SECURITYSYSTEM'
TYPE_SENSOR = PREFIX_TYPES + 'SENSOR'
TYPE_SMOKE_DETECTOR = PREFIX_TYPES + 'SMOKE_DETECTOR'
TYPE_SPEAKER = PREFIX_TYPES + 'SPEAKER'
TYPE_SWITCH = PREFIX_TYPES + 'SWITCH'
TYPE_THERMOSTAT = PREFIX_TYPES + 'THERMOSTAT'
TYPE_VACUUM = PREFIX_TYPES + 'VACUUM'
TYPE_VALVE = PREFIX_TYPES + 'VALVE'
TYPE_WASHER = PREFIX_TYPES + 'WASHER'
TYPE_WATERHEATER = PREFIX_TYPES + 'WATERHEATER'
TYPE_WINDOW = PREFIX_TYPES + 'WINDOW'

# Error codes used for SmartHomeError class
# https://developers.google.com/actions/smarthome/create-app#error_responses
ERR_ALREADY_IN_STATE = 'alreadyInState'
ERR_CHALLENGE_NEEDED = 'challengeNeeded'
ERR_DEVICE_NOT_FOUND = "deviceNotFound"
ERR_DEVICE_OFFLINE = "deviceOffline"
ERR_FUNCTION_NOT_SUPPORTED = 'functionNotSupported'
ERR_NOT_SUPPORTED = "notSupported"
ERR_PROTOCOL_ERROR = 'protocolError'
ERR_UNKNOWN_ERROR = 'unknownError'
ERR_VALUE_OUT_OF_RANGE = "valueOutOfRange"
ERR_WRONG_PIN = 'pinIncorrect'

DOMAINS = {
    'ac_unit': 'AcUnit',
    'bathtub': 'Bathtub',
    'blinds': 'Blind',
    'blindsinv': 'BlindInverted',
    'camera': 'Camera',
    'coffeemaker': 'Coffeemaker',
    'color': 'ColorSwitch',
    'cooktop': 'Cooktop',
    'door': 'DoorSensor',
    'doorbell': 'Doorbell',
    'dishwasher': 'Dishwasher',
    'dryer': 'Dryer',
    'fan': 'Fan',
    'garage': 'GarageSensor',
    'gate': 'Gate',
    'group': 'Group',
    'heater': 'Heater',
    'hidden': 'Hidden',
    'kettle': 'Kettle',
    'light': 'Light',
    'lock': 'DoorLock',
    'lockinv': 'DoorLockInv',
    'media': 'Media',
    'merged': 'Merged(Idx:',
    'microwave': 'Microwave',
    'mower': 'Mower',
    'outlet': 'Outlet',
    'oven': 'Oven',
    'push': 'PushButton',
    'radiator': 'Radiator',
    'scene': 'Scene',
    'screen': 'Screen',
    'security': 'Security',
    'selector': 'Selector',
    'sensor': 'Sensor',
    'smokedetector': 'SmokeDetector',
    'speaker': 'Speaker',
    'switch': 'Switch',
    'temperature': 'Temperature',
    'thermostat': 'Thermostat',
    'valve': 'Valve',
    'vacuum': 'Vacuum',
    'washer': 'Washer',
    'waterheater': 'Waterheater',
    'window': 'Window'
    }

ATTRS_BRIGHTNESS = 1
ATTRS_THERMSTATSETPOINT = 1
ATTRS_COLOR = 2
ATTRS_COLOR_TEMP = 3
ATTRS_PERCENTAGE = 1
ATTRS_FANSPEED = 1
ATTRS_VACUUM_MODES = 1
ATTRS_HUMIDITY = 1

DOMOTICZ_TO_GOOGLE_TYPES = {
    DOMAINS['ac_unit']: TYPE_AC_UNIT,
    DOMAINS['bathtub']: TYPE_BATHTUB,
    DOMAINS['blinds']: TYPE_BLINDS,
    DOMAINS['blindsinv']: TYPE_BLINDS,
    DOMAINS['camera']: TYPE_CAMERA,
    DOMAINS['coffeemaker']: TYPE_COFFEE,
    DOMAINS['color']: TYPE_LIGHT,
    DOMAINS['cooktop']: TYPE_COOKTOP,
    DOMAINS['dishwasher']: TYPE_DISHWASHER,
    DOMAINS['door']: TYPE_DOOR,
    DOMAINS['doorbell']: TYPE_DOORBELL,
    DOMAINS['dryer']: TYPE_DRYER,
    DOMAINS['fan']: TYPE_FAN,
    DOMAINS['garage']: TYPE_GARAGE,
    DOMAINS['gate']: TYPE_GATE,
    DOMAINS['group']: TYPE_SWITCH,
    DOMAINS['heater']: TYPE_HEATER,
    DOMAINS['kettle']: TYPE_KETTLE,
    DOMAINS['light']: TYPE_LIGHT,
    DOMAINS['lock']: TYPE_LOCK,
    DOMAINS['lockinv']: TYPE_LOCK,
    DOMAINS['media']: TYPE_MEDIA,
    DOMAINS['microwave']: TYPE_MICRO,
    DOMAINS['mower']: TYPE_MOWER,
    DOMAINS['outlet']: TYPE_OUTLET,
    DOMAINS['oven']: TYPE_OVEN,
    DOMAINS['push']: TYPE_SWITCH,
    DOMAINS['scene']: TYPE_SCENE,
    DOMAINS['screen']: TYPE_SCREEN,
    DOMAINS['security']: TYPE_SECURITY,
    DOMAINS['selector']: TYPE_SWITCH,
    DOMAINS['sensor']: TYPE_SENSOR,
    DOMAINS['smokedetector']: TYPE_SMOKE_DETECTOR,
    DOMAINS['speaker']: TYPE_SPEAKER,
    DOMAINS['switch']: TYPE_SWITCH,
    DOMAINS['temperature']: TYPE_SENSOR,
    DOMAINS['thermostat']: TYPE_THERMOSTAT,
    DOMAINS['vacuum']: TYPE_VACUUM,
    DOMAINS['valve']: TYPE_VALVE,
    DOMAINS['washer']: TYPE_WASHER,
    DOMAINS['waterheater']: TYPE_WATERHEATER,
    DOMAINS['window']: TYPE_WINDOW,
}
