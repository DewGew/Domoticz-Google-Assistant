# -*- coding: utf-8 -*-

import hashlib
import os
import re
import subprocess
import sys
import threading
from collections.abc import Mapping
from itertools import product
from pid import PidFile
import requests

import trait
from auth import *
from const import (DOMOTICZ_TO_GOOGLE_TYPES, ERR_FUNCTION_NOT_SUPPORTED, ERR_PROTOCOL_ERROR, ERR_DEVICE_OFFLINE,
                   ERR_UNKNOWN_ERROR, ERR_CHALLENGE_NEEDED, DOMOTICZ_GET_ALL_DEVICES_URL, domains,
                   DOMOTICZ_GET_SETTINGS_URL, DOMOTICZ_GET_ONE_DEVICE_URL, DOMOTICZ_GET_SCENES_URL, CONFIGFILE, LOGFILE,
                   REQUEST_SYNC_BASE_URL, REPORT_STATE_BASE_URL, ATTRS_BRIGHTNESS, ATTRS_FANSPEED, ATTRS_VACUUM_MODES,
                   ATTRS_THERMSTATSETPOINT, ATTRS_COLOR_TEMP, ATTRS_PERCENTAGE, VERSION, DOMOTICZ_GET_VERSION)
from helpers import (configuration, readFile, saveFile, SmartHomeError, SmartHomeErrorNoChallenge, AogState, uptime,
                     getTunnelUrl, FILE_DIR, logger, ReportState, Auth, logfilepath)

try:
    from jinja2 import Environment, FileSystemLoader
except ImportError:
    logger.info('Installing package jinja2')
    subprocess.call(['pip', 'install', 'jinja2'])
    from jinja2 import Environment, FileSystemLoader

DOMOTICZ_URL = configuration['Domoticz']['ip'] + ':' + configuration['Domoticz']['port']
CREDITS = (configuration['Domoticz']['username'], configuration['Domoticz']['password'])

file_loader = FileSystemLoader(FILE_DIR + '/templates')
env = Environment(
    loader=file_loader

    )

if 'PidFile' in configuration:
    pidfile = PidFile(pidname=configuration['PidFile'])
else:
    pidfile = PidFile('dzga')

try:
    logger.info("Connecting to Domoticz on %s" % DOMOTICZ_URL)
    r = requests.get(
        DOMOTICZ_URL + '/json.htm?type=command&param=addlogmessage&message=Connected to Google Assistant with DZGA v' + VERSION,
        auth=CREDITS, timeout=(2, 5))
except Exception as e:
    logger.error('Connection to Domoticz refused with error: %s' % e)

try:
    import git
    repo = git.Repo(FILE_DIR)
    branch = repo.active_branch.name
except:
    repo = None
    branch = ''
    
ReportState = ReportState()
if not ReportState.enable_report_state():
    logger.error("Service account key is not found. Report state will be unavailable")

Update = 0
def checkupdate(n=1800):
    """ Check for updates every 30 min (1800sec) """
    global Update
    while True:
        if repo is not None and 'CheckForUpdates' in configuration and configuration['CheckForUpdates'] == True:
            try:
                r = requests.get(
                    'https://raw.githubusercontent.com/DewGew/Domoticz-Google-Assistant/' + branch + '/const.py')
                response = r.text
                if VERSION not in response:
                    update = 1
                    logger.info("New version is availible on Github!")
                else:
                    update = 0
                
                Update = update    
                time.sleep(n)
            except Exception as e:
                logger.error('Connection to Github refused! Check configuration.')
                Update = 0
                time.sleep(n)
        else:
            Update = 0
            time.sleep(n)
            
thread = threading.Thread(target=checkupdate, daemon=True)
thread.start()         

def AogGetDomain(device):
    """ Convert a domain type: Domoticz to google """
    if device["Type"] in ['Light/Switch', 'Lighting 1', 'Lighting 2', 'Lighting 5', 'RFY', 'Value']:
        if device["SwitchType"] in ['Blinds', 'Venetian Blinds EU', 'Venetian Blinds US',
                                    'Blinds Percentage']:
            return domains['blinds']
        elif device["SwitchType"] in ['Blinds Inverted', 'Blinds Percentage Inverted']:
            return domains['blindsinv']
        elif 'Door Lock' == device["SwitchType"]:
            return domains['lock']
        elif 'Door Lock Inverted' == device["SwitchType"]:
            return domains['lockinv']
        elif "Door Contact" == device["SwitchType"]:
            return domains['door']
        elif device["SwitchType"] in ['Push On Button', 'Push Off Button']:
            return domains['push']
        elif 'Motion Sensor' == device["SwitchType"]:
            return domains['sensor']
        elif 'Selector' == device["SwitchType"]:
            if device['Image'] == 'Fan':
                return domains['fan']
            else:
                return domains['selector']
        elif 'Smoke Detector' == device["SwitchType"]:
            return domains['smokedetector']
        elif 'Camera_Stream' in configuration and True == device["UsedByCamera"] and True == \
                configuration['Camera_Stream']['Enabled']:
            return domains['camera']
        elif device["Image"] == 'Generic':
            return domains['switch']
        elif device["Image"] in ['Media', 'TV']:
            return domains['media']
        elif device["Image"] == 'WallSocket':
            return domains['outlet']
        elif device["Image"] == 'Speaker':
            return domains['speaker']
        elif device["Image"] == 'Fan':
            return domains['fan']
        elif device["Image"] == 'Heating':
            return domains['heater']
        else:
            return domains['light']
    elif 'Blinds' == device["Type"]:	
        return domains['blinds']
    elif 'Group' == device["Type"]:
        return domains['group']
    elif 'Scene' == device["Type"]:
        return domains['scene']
    elif device["Type"] in ['Temp', 'Temp + Humidity', 'Temp + Humidity + Baro']:
        return domains['temperature']
    elif 'Thermostat' == device['Type']:
        return domains['thermostat']
    elif 'Color Switch' == device["Type"]: 
        if "Dimmer" == device["SwitchType"]:
            return domains['color']
        elif "On/Off" == device["SwitchType"]:
            logger.info('%s (Idx: %s) is a color switch. To get all functions, set this device as Dimmer in Domoticz', device["Name"], device[
                "idx"])
            return domains['light']
        elif device["SwitchType"] in ['Push On Button', 'Push Off Button']:
            return domains['push']
    elif 'Security' == device["Type"]:
        return domains['security']
    return None

def getDesc(state):
    if state.domain in [domains['scene'], domains['group']]:
        if 'Scene_Config' in configuration and configuration['Scene_Config'] is not None:
            desc = configuration['Scene_Config'].get(int(state.id), None)
            return desc

    elif 'Device_Config' in configuration and configuration['Device_Config'] is not None:
        desc = configuration['Device_Config'].get(int(state.id), None)
        return desc
    else:
        return None

def getDeviceConfig(descstr):
    ISLIST = ['nicknames']
    rawconfig = re.findall(r'<voicecontrol>(.*?)</voicecontrol>', descstr, re.DOTALL)
    if len(rawconfig) > 0:
        try:
            lines = rawconfig[0].strip().splitlines()
            cfgdict = {}
            for l in lines:
                assign = l.split('=')
                varname = assign[0].strip().lower()
                if varname != "":
                    if varname in ISLIST:
                        allvalues = assign[1].split(',')
                        varvalues = []
                        for val in allvalues:
                            varvalues.append(val.strip())
                        cfgdict[varname] = varvalues
                    else:
                        varvalue = assign[1].strip()
                        if varvalue.lower() == "true":
                            varvalue = True
                        elif varvalue.lower() == "false":
                            varvalue = False
                        cfgdict[varname] = varvalue
        except:
            logger.error('Error parsing device configuration from Domoticz device description:', rawconfig[0])
            return None
        return cfgdict
    return None

def getAog(device):
    domain = AogGetDomain(device)
    if domain is None:
        return None

    aog = AogState()
    aog.name = device["Name"]  # .encode('ascii', 'ignore')
    aog.domain = domain
    aog.id = device["idx"]
    aog.entity_id = domain + aog.id
    aog.plan = device.get("PlanID")                               
    aog.state = device.get("Data", "Scene")
    aog.level = device.get("LevelInt", 0)
    aog.temp = device.get("Temp")
    aog.humidity = device.get("Humidity")
    aog.setpoint = device.get("SetPoint")
    if aog.domain is "Color":
        aog.color = device.get("Color")
    aog.protected = device.get("Protected")
    aog.maxdimlevel = device.get("MaxDimLevel")   
    aog.battery = device.get("BatteryLevel")
    aog.hardware = device.get("HardwareName")
    aog.selectorLevelName = device.get("LevelNames")
    aog.lastupdate = device.get("LastUpdate")
    
    aog.language = settings.get("Language")
    aog.tempunit = settings.get("TempUnit")
    if aog.domain is "Security":
        aog.seccode = settings.get("SecPassword")
        aog.secondelay = settings.get("SecOnDelay")


    # Try to get device specific voice control configuration from Domoticz
    # Read it from the configuration file if not in Domoticz (for backward compatibility)
    desc = getDeviceConfig(device.get("Description"))
    if desc is not None:
        logger.debug('<voicecontrol> tags found for idx %s in domoticz description.', aog.id)
        logger.debug('Device_Config for idx %s will be ignored in config.yaml!', aog.id)
    if desc is None:
        desc = getDesc(aog)

    if desc is not None:
        dt = desc.get('devicetype', None)
        if dt is not None:
            if aog.domain in [domains['blinds']]:
                if dt.lower() in ['window', 'gate', 'garage', 'door']:
                    aog.domain = domains[dt.lower()]
            if aog.domain in [domains['light'], domains['switch']]:
                if dt.lower() in ['window', 'door', 'gate', 'garage', 'light', 'ac_unit', 'bathtub', 'coffeemaker', 'dishwasher', 'dryer', 'fan', 'heater', 'kettle', 'media', 'microwave', 'outlet', 'oven', 'speaker', 'switch', 'vacuum', 'washer', 'waterheater']:
                    aog.domain = domains[dt.lower()]
            if aog.domain in [domains['door']]:
                if dt.lower() in ['window', 'gate', 'garage']:
                    aog.domain = domains[dt.lower()]    
            if aog.domain in [domains['selector']]:
                if dt.lower() in ['vacuum']:
                    aog.domain = domains[dt.lower()]
        pn = desc.get('name', None)
        if pn is not None:
            aog.name = pn
        n = desc.get('nicknames', None)
        if n is not None:
            aog.nicknames = n
        r = desc.get('room', None)
        if r is not None:
            aog.room = r
        ack = desc.get('ack', False)
        if ack:
            aog.ack = ack
        report_state = desc.get('report_state', True)
        if not ReportState.enable_report_state():
            aog.report_state = False
        if not report_state:
            aog.report_state = report_state            
        if domains['thermostat'] == aog.domain:
            at_idx = desc.get('actual_temp_idx', None)
            if at_idx is not None:
                aog.actual_temp_idx = at_idx
                try:
                    aog.state = str(aogDevs[domains['temperature'] + at_idx].temp)
                    aogDevs[domains['temperature'] + at_idx].domain = domains['merged'] + aog.id + ')'
                except:
                    logger.error('Merge Error, Cant find temperature device with idx %s', at_idx)
            modes_idx = desc.get('selector_modes_idx', None)
            if modes_idx is not None:
                aog.modes_idx = modes_idx
                try:
                    aog.level = aogDevs[domains['selector'] + modes_idx].level
                    aog.selectorLevelName = aogDevs[domains['selector'] + modes_idx].selectorLevelName
                    aogDevs[domains['selector'] + modes_idx].domain = domains['merged'] + aog.id + ')'
                except:
                    logger.error('Merge Error, Cant find selector device with idx %s', modes_idx)
        if aog.domain in [domains['heater'], domains['kettle'], domains['waterheater'], domains['oven']]:
            tc_idx = desc.get('merge_thermo_idx', None)
            if tc_idx is not None:
                aog.merge_thermo_idx = tc_idx
                try:
                    aog.temp = aogDevs[domains['thermostat'] + tc_idx].state
                    aog.setpoint = aogDevs[domains['thermostat'] + tc_idx].setpoint
                    aogDevs[domains['thermostat'] + tc_idx].domain = domains['merged'] + aog.id + ')'
                except:
                    logger.error('Merge Error, Cant find thermostat device with idx %s', tc_idx)
        hide = desc.get('hide', False)
        if hide:
            if aog.domain not in [domains['scene'], domains['group']]:
                aog.domain = domains['hidden']
            else:
                logger.error('Scenes and Groups does not support function "hide" yet')
            
    if aog.domain in [domains['camera']]:
        aog.report_state = False
        
    if domains['light'] == aog.domain and "Dimmer" == device["SwitchType"]:
        aog.attributes = ATTRS_BRIGHTNESS
    if domains['fan'] == aog.domain and "Selector" == device["SwitchType"]:
        aog.attributes = ATTRS_FANSPEED
    if domains['outlet'] == aog.domain and "Dimmer" == device["SwitchType"]:
        aog.attributes = ATTRS_BRIGHTNESS
    if domains['color'] == aog.domain and "Dimmer" == device["SwitchType"]:
        aog.attributes = ATTRS_BRIGHTNESS
    if domains['color'] == aog.domain and device["SubType"] in ["RGBWW", "White"]:
        aog.attributes = ATTRS_COLOR_TEMP
    if domains['thermostat'] == aog.domain and "Thermostat" == device["Type"]:
        aog.attributes = ATTRS_THERMSTATSETPOINT
    if domains['blinds'] == aog.domain and "Blinds Percentage" == device["SwitchType"]:
        aog.attributes = ATTRS_PERCENTAGE
    if domains['blindsinv'] == aog.domain and "Blinds Percentage Inverted" == device["SwitchType"]:
        aog.attributes = ATTRS_PERCENTAGE
    if domains['vacuum'] == aog.domain and "Selector" == device["SwitchType"]:
        aog.attributes = ATTRS_VACUUM_MODES
        
    if aog.room == None:
        if aog.domain not in [domains['scene'], domains['group']]:
            if aog.plan is not "0":
                aog.room = getPlans(aog.plan)
        
    return aog

aogDevs = {}
deviceList = {}

def getDevices(devices="all", idx="0"):
    global aogDevs
    global deviceList

    url = ""
    if "all" == devices:
        url = DOMOTICZ_URL + DOMOTICZ_GET_ALL_DEVICES_URL + configuration['Domoticz'][
            'roomplan'] + '&filter=all&used=true'
    elif "scene" == devices:
        url = DOMOTICZ_URL + DOMOTICZ_GET_SCENES_URL
    elif "id" == devices:
        url = DOMOTICZ_URL + DOMOTICZ_GET_ONE_DEVICE_URL + idx

    r = requests.get(url, auth=CREDITS)
    if r.status_code == 200:
        devs = r.json()['result']
        for d in devs:
            aog = getAog(d)
            if aog is None:
                continue

            aogDevs[aog.entity_id] = aog
                            
            if 'loglevel' in configuration and (configuration['loglevel']).lower() == 'debug':

                req = {aog.name: {}}
                req[aog.name]['idx'] = int(aog.id)
                req[aog.name]['type'] = aog.domain
                req[aog.name]['state'] = aog.state
                req[aog.name]['lastupdate'] = aog.lastupdate
                if aog.nicknames is not None:
                    req[aog.name]['nicknames'] = aog.nicknames
                if aog.modes_idx is not None:
                    req[aog.name]['modes_idx'] = aog.modes_idx
                if aog.hide is not False:
                    req[aog.name]['hidden'] = aog.hide
                if aog.actual_temp_idx is not None:
                    req[aog.name]['actual_temp_idx'] = aog.actual_temp_idx
                if aog.merge_thermo_idx is not None:
                    req[aog.name]['merge_thermo_idx'] = aog.merge_thermo_idx
                req[aog.name]['willReportState'] = aog.report_state
                logger.debug(json.dumps(req, indent=2, sort_keys=False, ensure_ascii=False))

    devlist = [(d.name, int(d.id), d.domain, d.state, d.room, d.nicknames, d.report_state) for d in aogDevs.values()]
    devlist.sort(key=takeSecond)
    deviceList = json.dumps(devlist)

def takeSecond(elem):
    return elem[1]

def deep_update(target, source):
    """Update a nested dictionary with another nested dictionary."""
    for key, value in source.items():
        if isinstance(value, Mapping):
            target[key] = deep_update(target.get(key, {}), value)
        else:
            target[key] = value
    return target

settings = {}
settings['dzversion'] = "Unavailable"

def getSettings():
    """Get domoticz settings."""
    global settings

    url = DOMOTICZ_URL + DOMOTICZ_GET_SETTINGS_URL
    r = requests.get(url, auth=CREDITS)

    if r.status_code == 200:
        devs = r.json()
        settings['SecPassword'] = devs['SecPassword']
        settings["SecOnDelay"] = devs["SecOnDelay"]
        settings['TempUnit'] = devs['TempUnit']
        settings['Language'] = devs['Language']
    
    getVersion()

    logger.debug(json.dumps(settings, indent=2, sort_keys=False, ensure_ascii=False))

def getVersion():
    """Get domoticz version."""
    global settings

    url = DOMOTICZ_URL + DOMOTICZ_GET_VERSION
    r = requests.get(url, auth=CREDITS)

    if r.status_code == 200:
        vers = r.json()
        settings['dzversion'] = vers['version']

def getPlans(idx):
    """Get domoticz plan name."""
    global settings
    
    url = DOMOTICZ_URL + '/json.htm?type=plans&order=name&used=true'
    r = requests.get(url, auth=CREDITS)

    if r.status_code == 200:
        rooms = r.json()['result']
        plan = [i for i in rooms if i['idx'] == idx][0]
        return plan['Name']

def restartServer():
    """Restart."""
    logger.info(' ')
    logger.info("Restart server")
    logger.info(' ')
    
    time.sleep(5)
    
    pidfile.close()

    os.execv(sys.executable, ['python'] + sys.argv)

class _GoogleEntity:
    """Adaptation of Entity expressed in Google's terms."""

    def __init__(self, state):
        self.state = state

    @property
    def entity_id(self):
        """Return entity ID."""
        return self.state.entity_id

    def traits(self):
        """Return traits for entity."""
        state = self.state
        domain = state.domain
        features = state.attributes

        t = [Trait(state) for Trait in trait.TRAITS
             if Trait.supported(domain, features)]
        return t

    def sync_serialize(self, agent_user_id):
        """Serialize entity for a SYNC response.
        https://developers.google.com/actions/smarthome/create-app#actiondevicessync
        """
        state = self.state
        enableReport = ReportState.enable_report_state()
        traits = self.traits()

        # Found no supported traits for this entity
        if not traits:
            return None

        if enableReport:
            reportState = state.report_state
        else:
            reportState = enableReport

        device = {
            'id': state.entity_id,
            'name': {
                'name': state.name
            },
            'attributes': {},
            'traits': [trait.name for trait in traits],
            'willReportState': reportState,
            'deviceInfo': {
                'manufacturer': "Domoticz",
                "model": state.hardware
            },
            'type': DOMOTICZ_TO_GOOGLE_TYPES[state.domain],
        }

        # use aliases
        aliases = state.nicknames
        if aliases:
            device['name']['nicknames'] = [state.name] + aliases
        
        for trt in traits:
            device['attributes'].update(trt.sync_attributes())
            
        # Add room hint if annotated                     
        room = state.room
        if room:
            device['roomHint'] = room
               
        return device

    def query_serialize(self):
        """Serialize entity for a QUERY response.
        https://developers.google.com/actions/smarthome/create-app#actiondevicesquery
        """
        state = self.state

        # if state.state == STATE_UNAVAILABLE:
        # return {'online': False}

        attrs = {'online': True}
        for trt in self.traits():
            deep_update(attrs, trt.query_attributes())

        return attrs

    def execute(self, command, params, challenge):
        """Execute a command.
        https://developers.google.com/actions/smarthome/create-app#actiondevicesexecute
        """
        executed = False
        for trt in self.traits():
            if trt.can_execute(command, params):

                acknowledge = self.state.ack  # ack is now stored in state
                pincode = False

                if configuration['Domoticz']['switchProtectionPass']:
                    protect = self.state.protected
                else:
                    protect = False

                if protect or self.state.domain == domains['security']:
                    pincode = configuration['Domoticz']['switchProtectionPass']
                    if self.state.domain == domains['security']:
                        pincode = self.state.seccode
                    acknowledge = False
                    if challenge is None:
                        raise SmartHomeErrorNoChallenge(ERR_CHALLENGE_NEEDED, 'pinNeeded',
                                                        'Unable to execute {} for {} - challenge needed '.format(
                                                            command, self.state.entity_id))
                    elif not challenge.get('pin', False):
                        raise SmartHomeErrorNoChallenge(ERR_CHALLENGE_NEEDED, 'userCancelled',
                                                        'Unable to execute {} for {} - challenge needed '.format(
                                                            command, self.state.entity_id))
                    elif True == protect and pincode != challenge.get('pin'):
                        raise SmartHomeErrorNoChallenge(ERR_CHALLENGE_NEEDED, 'challengeFailedPinNeeded',
                                                        'Unable to execute {} for {} - challenge needed '.format(
                                                            command, self.state.entity_id))
                    elif self.state.domain == domains['security'] and pincode != hashlib.md5(
                            str.encode(challenge.get('pin'))).hexdigest():
                        raise SmartHomeErrorNoChallenge(ERR_CHALLENGE_NEEDED, 'challengeFailedPinNeeded',
                                                        'Unable to execute {} for {} - challenge needed '.format(
                                                            command, self.state.entity_id))

                if acknowledge:
                    if challenge is None:
                        raise SmartHomeErrorNoChallenge(ERR_CHALLENGE_NEEDED, 'ackNeeded',
                                                        'Unable to execute {} for {} - challenge needed '.format(
                                                            command, self.state.entity_id))
                    elif not challenge.get('ack', False):
                        raise SmartHomeErrorNoChallenge(ERR_CHALLENGE_NEEDED, 'userCancelled',
                                                        'Unable to execute {} for {} - challenge needed '.format(
                                                            command, self.state.entity_id))

                trt.execute(command, params)
                executed = True
                break

        if not executed:
            raise SmartHomeError(ERR_FUNCTION_NOT_SUPPORTED,
                                 'Unable to execute {} for {}'.format(command, self.state.entity_id))

    def async_update(self):
        """Update the entity with latest info from Domoticz."""

        if self.state.domain == domains['group'] or self.state.domain == domains['scene']:
            getDevices('scene')
        else:
            getDevices('id', self.state.id)

class SmartHomeReqHandler(OAuthReqHandler):
    global smarthomeControlMappings
    global aogDevs
    global Update

    def __init__(self, *args, **kwargs):
        super(SmartHomeReqHandler, self).__init__(*args, **kwargs)
        self._request_id = None

    def report_state(self, states, token):
        """Send a state report to Google."""

        data = {
            'requestId': self._request_id,
            'agentUserId': token.get('userAgentId', None),
            'payload': {
                'devices': {
                    'states': states,
                }
            }
        }
        ReportState.call_homegraph_api(REPORT_STATE_BASE_URL, data)

    def smarthome_process(self, message, token):
        request_id = self._request_id  # type: str
        inputs = message.get('inputs')  # type: list

        if len(inputs) != 1:
            return {
                'requestId': request_id,
                'payload': {'errorCode': ERR_PROTOCOL_ERROR}
                }

        handler = smarthomeControlMappings.get(inputs[0].get('intent'))

        if handler is None:
            return {'requestId': request_id, 'payload': {'errorCode': ERR_PROTOCOL_ERROR}}

        try:
            result = handler(self, inputs[0].get('payload'), token)
            return {'requestId': request_id, 'payload': result}

        except SmartHomeError as err:
            return {'requestId': request_id, 'payload': {'errorCode': err.code}}

        except Exception as e:
            logger.error(e)
            return {'requestId': request_id, 'payload': {'errorCode': ERR_UNKNOWN_ERROR}}

    def smarthome_post(self, s):
        logger.debug(s.headers)
        a = s.headers.get('Authorization', None)

        token = None
        if a is not None:
            types, tokenH = a.split()
            if types.lower() == 'bearer':
                token = Auth['tokens'].get(tokenH, None)

        if token is None:
            raise SmartHomeError(ERR_PROTOCOL_ERROR, 'not authorized access!!')

        message = json.loads(s.body)

        self._request_id = message.get('requestId')

        logger.info("Request " + json.dumps(message, indent=2, sort_keys=True, ensure_ascii=False))
        response = self.smarthome_process(message, token)

        try:
            if 'errorCode' in response['payload']:
                logger.error('Error handling message %s: %s' % (message, response['payload']))
        except:
            pass
        s.send_json(200, json.dumps(response, ensure_ascii=False).encode('utf-8'), True)

    def smarthome(self, s):
        s.send_message(500, "not supported")

    def forceDevicesSync(self):
        userAgent = self.getUserAgent()
        enableReport = ReportState.enable_report_state()
        if userAgent is None:
            return 500  # internal error

        data = {"agentUserId": userAgent}
        if enableReport:
            r = ReportState.call_homegraph_api(REQUEST_SYNC_BASE_URL, data)
            logger.info('Device syncronization sent')
        elif 'Homegraph_API_Key' in configuration and configuration['Homegraph_API_Key'] != 'ADD_YOUR HOMEGRAPH_API_KEY_HERE':
            r = ReportState.call_homegraph_api_key(REQUEST_SYNC_BASE_URL, data)
            logger.info('Device syncronization sent')
        else:
            logger.error("No configuration for request_sync available")

        return r

    def syncDevices(self, s):
        user = self.getSessionUser()
        if user is None or user.get('uid', '') == '':
            s.redirect('login?redirect_uri={0}'.format('sync'))
            return

        r = self.forceDevicesSync()
        s.send_message(200, 'Synchronization request sent, status_code: ' + str(r))

    def restartServer(self, s):
        user = self.getSessionUser()
        if user is None or user.get('uid', '') == '':
            s.redirect('login?redirect_uri={0}'.format('restart'))
            return

        s.send_message(200, 'Restart request sent, status_code: True')
        restartServer()
        
    def log(self, s):
        user = self.getSessionUser()
        if user is None or user.get('uid', '') == '':
            s.redirect('login?redirect_uri={0}'.format('log'))
            return
            
        latestlogs = readFile(os.path.join(logfilepath, LOGFILE))
            
        s.send_message(200, latestlogs)
        
    def states(self, s):
        user = self.getSessionUser()
        if user is None or user.get('uid', '') == '':
            s.redirect('login?redirect_uri={0}'.format('log'))
            return
            
        deviceList
            
        s.send_message(200, deviceList)
        
    def test(self, s):

        s.send_message(200, templatepage.render())
        
    def settings(self, s):
        user = self.getSessionUser()
        if user is None or user.get('uid', '') == '':
            s.redirect('login?redirect_uri={0}'.format('settings'))
            return

        update = Update
        confJSON = json.dumps(configuration)
        public_url = getTunnelUrl()
        message = ''
        meta = '<!-- <meta http-equiv="refresh" content="5"> -->'
        code = readFile(os.path.join(FILE_DIR, CONFIGFILE))

        templatepage = env.get_template('home.html')
        s.send_message(200, templatepage.render(message=message, uptime=uptime(), meta=meta, code=code,
                                       conf=confJSON, public_url=public_url, update=update,
                                       branch=branch, dzversion=settings['dzversion'], dzgaversion=VERSION))
                                       
    def settings_post(self, s):
        enableReport = ReportState.enable_report_state()
        update = Update
        confJSON = json.dumps(configuration)
        public_url = getTunnelUrl()
        code = readFile(os.path.join(FILE_DIR, CONFIGFILE))
        meta = '<!-- <meta http-equiv="refresh" content="5"> -->'

        if s.form.get("save"):
            textToSave = s.form.get("save", None)
            codeToSave = textToSave.replace("+", " ")
            saveFile(CONFIGFILE, codeToSave)
            message = 'Config saved'
            logger.info(message)
            logs = readFile(os.path.join(logfilepath, LOGFILE))
            templatepage = env.get_template('home.html')
            s.send_message(200, templatepage.render(message=message, uptime=uptime(), meta=meta, code=code,
                                       conf=confJSON, public_url=public_url, update=update,
                                       branch=branch, dzversion=settings['dzversion'], dzgaversion=VERSION))

        if s.form.get("backup"):
            codeToSave = readFile(os.path.join(FILE_DIR, CONFIGFILE))
            saveFile('config/config.yaml.bak', codeToSave)
            message = 'Backup saved'
            logger.info(message)
            templatepage = env.get_template('home.html')
            s.send_message(200, templatepage.render(message=message, uptime=uptime(), meta=meta, code=code,
                                       conf=confJSON, public_url=public_url, update=update,
                                       branch=branch, dzversion=settings['dzversion'], dzgaversion=VERSION))

        if s.form.get("restart"):
            meta = '<meta http-equiv="refresh" content="10">'
            message = 'Restarts DZGA server'

            templatepage = env.get_template('home.html')
            s.send_message(200, templatepage.render(message=message, uptime=uptime(), meta=meta, code=code,
                                       conf=confJSON, public_url=public_url, update=update,
                                       branch=branch, dzversion=settings['dzversion'], dzgaversion=VERSION))
            restartServer()

        if s.form.get("sync"):
            if 'Homegraph_API_Key' in configuration and configuration['Homegraph_API_Key'] != 'ADD_YOUR HOMEGRAPH_API_KEY_HERE' or enableReport == True:
                r = self.forceDevicesSync()
                time.sleep(0.5)
                if r:
                    message = 'Devices syncronized'
                else:
                    message = 'Homegraph api key not valid!'
            else:
                message = 'Add Homegraph api key or a Homegraph Service Account json file to sync devices in the UI! You can still sync by voice eg. "Hey Google, Sync my devices".'
            templatepage = env.get_template('home.html')
            s.send_message(200, templatepage.render(message=message, uptime=uptime(), meta=meta, code=code,
                                       conf=confJSON, public_url=public_url, update=update,
                                       branch=branch, dzversion=settings['dzversion'], dzgaversion=VERSION))

        if s.form.get("reload"):
            message = ''

            templatepage = env.get_template('home.html')
            s.send_message(200, templatepage.render(message=message, uptime=uptime(), meta=meta, code=code,
                                       conf=confJSON, public_url=public_url, update=update,
                                       branch=branch, dzversion=settings['dzversion'], dzgaversion=VERSION))

        if s.form.get("deletelogs"):
            logfile = os.path.join(logfilepath, LOGFILE)
            if os.path.exists(logfile):
                f = open(logfile, 'w')
                f.close()
            logger.info('Logs removed by user')
            message = 'Logs removed'
            templatepage = env.get_template('home.html')
            s.send_message(200, templatepage.render(message=message, uptime=uptime(), meta=meta, code=code,
                                       conf=confJSON, public_url=public_url, update=update,
                                       branch=branch, dzversion=settings['dzversion'], dzgaversion=VERSION))

        if s.form.get("update"):
            repo.git.reset('--hard')
            repo.remotes.origin.pull()
            message = 'Updating to latest ' + branch + ', please wait a minute!'
            meta = '<meta http-equiv="refresh" content="20">'

            templatepage = env.get_template('home.html')
            s.send_message(200, templatepage.render(message=message, uptime=uptime(), meta=meta, code=code,
                                       conf=confJSON, public_url=public_url, update=update,
                                       branch=branch, dzversion=settings['dzversion'], dzgaversion=VERSION))
            
            subprocess.call(['pip3', 'install','-r', os.path.join(FILE_DIR, 'requirements/pip-requirements.txt')])
            restartServer()


    def smarthome_sync(self, payload, token):
        """Handle action.devices.SYNC request.
        https://developers.google.com/actions/smarthome/create-app#actiondevicessync
        """
        devices = []
        aogDevs.clear()
        getDevices()  # sync all devices
        getSettings()
        enableReport = ReportState.enable_report_state()
        agent_user_id = token.get('userAgentId', None)

        for state in aogDevs.values():

            entity = _GoogleEntity(state)
            serialized = entity.sync_serialize(agent_user_id)

            if serialized is None:
                continue

            devices.append(serialized)

        response = {'agentUserId': agent_user_id, 'devices': devices}
                
        return response

    def smarthome_query(self, payload, token):
        """Handle action.devices.QUERY request.
        https://developers.google.com/actions/smarthome/create-app#actiondevicesquery
        """
        enableReport = ReportState.enable_report_state()
        response = {}
        devices = {}
        getDevices()
        
        for device in payload.get('devices', []):
            devid = device['id']
            #_GoogleEntity(aogDevs.get(devid, None)).async_update()
            state = aogDevs.get(devid, None)           
            if not state:
                # If we can't find a state, the device is offline
                devices[devid] = {'online': False}
                continue

            e = _GoogleEntity(state)
            devices[devid] = e.query_serialize()
                        
        response = {'devices': devices}
        logger.info("Response " + json.dumps(response, indent=2, sort_keys=True, ensure_ascii=False))
        
        if state.report_state == True and enableReport == True:
            self.report_state(devices, token)
               
        return {'devices': devices}

    def smarthome_exec(self, payload, token):
        """Handle action.devices.EXECUTE request.
        https://developers.google.com/actions/smarthome/create-app#actiondevicesexecute
        """
        entities = {}
        results = {}

        for command in payload['commands']:
            for device, execution in product(command['devices'],
                                             command['execution']):
                entity_id = device['id']
                # Happens if error occurred. Skip entity for further processing
                if entity_id in results:
                    continue

                if entity_id not in entities:
                    if len(aogDevs) == 0:
                        getDevices()
                        getSettings()

                    state = aogDevs.get(entity_id, None)
                    if state is None:
                        results[entity_id] = {'ids': [entity_id], 'status': 'ERROR', 'errorCode': ERR_DEVICE_OFFLINE}
                        continue

                    entities[entity_id] = _GoogleEntity(state)

                try:
                    entities[entity_id].execute(execution['command'], execution.get('params', {}),
                                                execution.get('challenge', None))

                except SmartHomeError as err:
                    results[entity_id] = {'ids': [entity_id], 'status': 'ERROR', 'errorCode': err.code}
                    logger.error(err)
                except SmartHomeErrorNoChallenge as err:
                    results[entity_id] = {'ids': [entity_id], 'status': 'ERROR', 'errorCode': err.code,
                                          'challengeNeeded': {'type': err.desc}}
                    logger.error(err)

        final_results = list(results.values())
        for entity in entities.values():
            if entity.entity_id in results:
                continue
            entity.async_update()
            final_results.append({'ids': [entity.entity_id], 'status': 'SUCCESS', 'states': entity.query_serialize()})
    
        return {'commands': final_results}

    def smarthome_disconnect(self, payload, token):
        """Handle action.devices.DISCONNECT request.
        https://developers.google.com/assistant/smarthome/develop/process-intents#DISCONNECT
        """
        return None

if 'userinterface' in configuration and configuration['userinterface'] == True:
    smarthomeGetMappings = {"/smarthome": SmartHomeReqHandler.smarthome,
                            "/sync": SmartHomeReqHandler.syncDevices,
                            "/settings": SmartHomeReqHandler.settings,
                            "/log": SmartHomeReqHandler.log,
                            "/states": SmartHomeReqHandler.states,
                            "/restart": SmartHomeReqHandler.restartServer}

    smarthomePostMappings = {"/smarthome": SmartHomeReqHandler.smarthome_post,
                             "/settings": SmartHomeReqHandler.settings_post}
else:
    smarthomeGetMappings = {"/smarthome": SmartHomeReqHandler.smarthome,
                            "/sync": SmartHomeReqHandler.syncDevices,
                            "/restart": SmartHomeReqHandler.restartServer}

    smarthomePostMappings = {"/smarthome": SmartHomeReqHandler.smarthome_post}

smarthomeControlMappings = {'action.devices.SYNC': SmartHomeReqHandler.smarthome_sync,
                            'action.devices.QUERY': SmartHomeReqHandler.smarthome_query,
                            'action.devices.EXECUTE': SmartHomeReqHandler.smarthome_exec,
                            'action.devices.DISCONNECT': SmartHomeReqHandler.smarthome_disconnect}
