# -*- coding: utf-8 -*-

from auth import *
import requests
import json
import hashlib
from itertools import product
import trait
from collections.abc import Mapping
import re
import os
import sys
import time, threading
from pip._internal import main as pip

from helpers import (configuration, readFile, saveFile, SmartHomeError, SmartHomeErrorNoChallenge, AogState, uptime, getTunnelUrl, FILE_DIR, logger, ReportState, Auth, LOGFILEPATH)
   
from const import (DOMOTICZ_TO_GOOGLE_TYPES, ERR_FUNCTION_NOT_SUPPORTED, ERR_PROTOCOL_ERROR, ERR_DEVICE_OFFLINE,TEMPLATE, ERR_UNKNOWN_ERROR, ERR_CHALLENGE_NEEDED, REQUEST_SYNC_BASE_URL,
    DOMOTICZ_GET_ALL_DEVICES_URL, DOMOTICZ_GET_SETTINGS_URL, DOMOTICZ_GET_ONE_DEVICE_URL, DOMOTICZ_GET_SCENES_URL, DOMOTICZ_GET_CAMERAS_URL, groupDOMAIN, sceneDOMAIN, CONFIGFILE, LOGFILE, KEYFILE,
    lightDOMAIN, switchDOMAIN, blindsDOMAIN, screenDOMAIN, pushDOMAIN, climateDOMAIN, tempDOMAIN, lockDOMAIN, invlockDOMAIN, colorDOMAIN, mediaDOMAIN, speakerDOMAIN, cameraDOMAIN, REQUEST_SYNC_BASE_URL,
    REPORT_STATE_BASE_URL, securityDOMAIN, outletDOMAIN, sensorDOMAIN, doorDOMAIN, selectorDOMAIN, fanDOMAIN, ATTRS_BRIGHTNESS,ATTRS_THERMSTATSETPOINT,ATTRS_COLOR, ATTRS_COLOR_TEMP, ATTRS_PERCENTAGE, VERSION)
    
DOMOTICZ_URL = configuration['Domoticz']['ip'] + ':' + configuration['Domoticz']['port']

try:
    logger.debug("Connecting to Domoticz on %s" % (DOMOTICZ_URL))
    r = requests.get(DOMOTICZ_URL + '/json.htm?type=command&param=addlogmessage&message=Connected to Google Assistant with DZGA v' + VERSION,
        auth=(configuration['Domoticz']['username'], configuration['Domoticz']['password']))
except Exception as e:
    logger.error('Connection to Domoticz refused with error: %s' % (e))
      
try:
    import git
except ImportError:
    logger.info('Installing package GitPython')
    pip.main(['install', 'gitpython'])
    import git        
try:    
    repo = git.Repo(FILE_DIR)
except:
    repo = None
ReportState = ReportState()
if ReportState.enable_report_state() == False:
    logger.error("Service account key is not found.")
    logger.error("Report state will be unavailable")
    
def checkupdate():
    if 'CheckForUpdates' in configuration and configuration['CheckForUpdates'] == True:
        try:
            r = requests.get('https://raw.githubusercontent.com/DewGew/Domoticz-Google-Assistant/' + repo.active_branch.name + '/const.py')
            text = r.text
            if VERSION not in text:
                update = 1
                logger.info("========")
                logger.info("   New version is availible on Github!")
            else:
                update = 0
            return update
        except Exception as e:
            logger.error('Connection to Github refused! Check configuration.')
            return 0
    else:
        return 0
    
update = checkupdate()
         
#some way to convert a domain type: Domoticz to google
def AogGetDomain(device):
    if device["Type"] in ['Light/Switch', 'Lighting 1', 'Lighting 2', 'RFY']:
        if device["SwitchType"] in ['Blinds', 'Blinds Inverted', 'Venetian Blinds EU', 'Venetian Blinds US', 'Blinds Percentage', 'Blinds Percentage Inverted'] :
            return blindsDOMAIN
        elif 'Door Lock' == device["SwitchType"]:
            return lockDOMAIN
        elif 'Door Lock Inverted' == device["SwitchType"]:
            return invlockDOMAIN
        elif "Door Contact" == device["SwitchType"]:
            return doorDOMAIN
        elif device["SwitchType"] in ['Push On Button', 'Push Off Button']:
            return pushDOMAIN
        elif 'Motion Sensor' == device["SwitchType"]:
            return sensorDOMAIN
        elif 'Selector' == device["SwitchType"]:
            return selectorDOMAIN
        elif 'Camera_Stream' in configuration and True == device["UsedByCamera"] and True == configuration['Camera_Stream']['Enabled']:
            return cameraDOMAIN
        elif 'Image_Override' in configuration and 'Switch' in configuration['Image_Override'] and device["Image"] in configuration['Image_Override']['Switch']:
            return switchDOMAIN
        elif 'Image_Override' in configuration and 'Light' in configuration['Image_Override'] and device["Image"] in configuration['Image_Override']['Light']:
            return lightDOMAIN
        elif 'Image_Override' in configuration and 'Media' in configuration['Image_Override'] and device["Image"] in configuration['Image_Override']['Media']:
            return mediaDOMAIN
        elif 'Image_Override' in configuration and 'Outlet' in configuration['Image_Override'] and device["Image"] in configuration['Image_Override']['Outlet']:
            return outletDOMAIN
        elif 'Image_Override' in configuration and 'Speaker' in configuration['Image_Override'] and device["Image"] in configuration['Image_Override']['Speaker']:
            return speakerDOMAIN
        elif 'Image_Override' in configuration and 'Fan' in configuration['Image_Override'] and device["Image"] in configuration['Image_Override']['Fan']:
            return fanDOMAIN
        else:
            return lightDOMAIN
    elif 'Group' == device["Type"]:
        return groupDOMAIN
    elif 'Scene' == device["Type"]:
        return sceneDOMAIN
    elif 'Temp' == device["Type"]:
        return tempDOMAIN
    elif 'Thermostat' == device['Type']:
        return climateDOMAIN
    elif 'Temp + Humidity' == device['Type']:
        return tempDOMAIN
    elif 'Temp + Humidity + Baro' == device['Type']:
        return tempDOMAIN
    elif 'Color Switch' == device["Type"] and "Dimmer" == device["SwitchType"]:
        return colorDOMAIN
    elif 'Color Switch' == device["Type"] and "On/Off" == device["SwitchType"]:
        logger.info(device["Name"] + " (Idx: " + device["idx"] + ") is a color switch. To get all functions, set this device as Dimmer in Domoticz")
        return lightDOMAIN
    elif 'Security' == device["Type"]:
        return securityDOMAIN
    return None

def getDesc(state):
    if state.domain == sceneDOMAIN or state.domain == groupDOMAIN:
        if 'Scene_Config' in configuration:
            desc = configuration['Scene_Config'].get(int(state.id), None)
            return desc
        
    elif 'Device_Config' in configuration:
            desc = configuration['Device_Config'].get(int(state.id), None)
            return desc
    else:
        return None
           
def getDeviceConfig(descstr):
    ISLIST = ['nicknames']
    rawconfig = re.findall(r'<voicecontrol>(.*?)</voicecontrol>',descstr,re.DOTALL)
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
                        cfgdict[varname]=varvalues
                    else:
                        varvalue = assign[1].strip()
                        if varvalue.lower() == "true":
                            varvalue = True
                        elif varvalue.lower() == "false":
                            varvalue = False
                        cfgdict[varname]=varvalue
        except:
            logger.error('Error parsing device configuration from Domoticz device description:', rawconfig[0])
            return None
        return cfgdict
    return None
            
def getAog(device):
    
    domain = AogGetDomain(device)
    if domain == None:
        return None
        
    aog = AogState()
    aog.name = device["Name"] #.encode('ascii', 'ignore')
    aog.domain = domain
    aog.id = device["idx"]
    aog.entity_id = domain + aog.id
    aog.state = device.get("Data", "Scene")
    aog.level = device.get("LevelInt", 0)
    aog.temp = device.get("Temp")
    aog.humidity = device.get("Humidity")
    aog.setpoint = device.get("SetPoint")
    aog.color = device.get("Color")
    aog.protected = device.get("Protected")
    aog.maxdimlevel = device.get("MaxDimLevel")
    aog.seccode = settings.get("SecPassword")
    aog.secondelay = settings.get("SecOnDelay")
    aog.tempunit = settings.get("TempUnit")
    aog.battery = device.get("BatteryLevel")
    aog.hardware = device.get("HardwareName")
    aog.selectorLevelName = device.get("LevelNames")
    aog.language = settings.get("Language")
    
    if lightDOMAIN == aog.domain and "Dimmer" == device["SwitchType"]:
        aog.attributes = ATTRS_BRIGHTNESS
    if outletDOMAIN == aog.domain and "Dimmer" == device["SwitchType"]:
        aog.attributes = ATTRS_BRIGHTNESS
    if colorDOMAIN == aog.domain and "Dimmer" == device["SwitchType"]:
        aog.attributes = ATTRS_BRIGHTNESS
    if colorDOMAIN == aog.domain and "RGBWW" == device["SubType"]:
        aog.attributes = ATTRS_COLOR_TEMP
    if climateDOMAIN == aog.domain and "Thermostat" == device["Type"]:
        aog.attributes = ATTRS_THERMSTATSETPOINT
    if blindsDOMAIN == aog.domain and "Blinds Percentage" == device["SwitchType"]:
        aog.attributes = ATTRS_PERCENTAGE
    if blindsDOMAIN == aog.domain and "Blinds Percentage Inverted" == device["SwitchType"]:
        aog.attributes = ATTRS_PERCENTAGE
    
    # Try to get device specific voice control configuration from Domoticz
    # Read it from the configuration file if not in Domoticz (for backward compatibility)
    desc = getDeviceConfig(device.get("Description"))
    if desc == None:
        desc = getDesc(aog)
    
    if desc != None:
        n = desc.get('nicknames', None)
        if n != None:
            aog.nicknames = n
        r = desc.get('room', None)
        if r != None:
            aog.room = r
        ack = desc.get('ack', False)
        if ack:
            aog.ack = ack
        report_state = desc.get('report_state', True)
        if ReportState.enable_report_state() == False:
            aog.report_state = False
        if report_state != True:
            aog.report_state = report_state
    if aog.domain == cameraDOMAIN:
        aog.report_state = False
    return aog;
 
aogDevs = {}
deviceList = {}
def getDevices(type = "all", id = "0"):
    global aogDevs
    global deviceList

    url = ""
    if "all" == type:  
        url = DOMOTICZ_URL + DOMOTICZ_GET_ALL_DEVICES_URL + configuration['Domoticz']['roomplan'] + '&filter=all&used=true'
    elif "scene" == type:
        url = DOMOTICZ_URL + DOMOTICZ_GET_SCENES_URL
    elif "id" == type:  
        url = DOMOTICZ_URL + DOMOTICZ_GET_ONE_DEVICE_URL + id
        
    r = requests.get(url, auth=(configuration['Domoticz']['username'], configuration['Domoticz']['password']))
    if r.status_code == 200:
        devs = r.json()['result']
        for d in devs:
            aog = getAog(d)
            if aog == None:
                continue

            aogDevs[aog.entity_id] = aog
            req = {}
            req[aog.name] = {}
            req[aog.name]['idx'] = int(aog.id)
            req[aog.name]['type'] = aog.domain
            req[aog.name]['state'] = aog.state
            req[aog.name]['nicknames'] = aog.nicknames
            req[aog.name]['willReportState'] = aog.report_state
            logger.debug(json.dumps(req, indent=2, sort_keys=False, ensure_ascii=False))
            
    list = [(d.name, int(d.id), d.domain, d.state, d.room, d.nicknames, d.report_state) for d in aogDevs.values()]
    list.sort(key=takeSecond)
    deviceList = json.dumps(list)
            
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
def getSettings():
    """Get domoticz settings."""
    global settings
    
    url = DOMOTICZ_URL + DOMOTICZ_GET_SETTINGS_URL
    r = requests.get(url, auth=(configuration['Domoticz']['username'], configuration['Domoticz']['password']))
    
    if r.status_code == 200:
        devs = r.json()
        settings['SecPassword'] = devs['SecPassword']
        settings["SecOnDelay"] = devs["SecOnDelay"]
        settings['TempUnit'] = devs['TempUnit']
        settings['Language'] = devs['Language']
        
    logger.debug(json.dumps(settings, indent=2, sort_keys=False, ensure_ascii=False))
        
def restartServer():
    """Restart.""" 
    logger.info(' ')
    logger.info("Restart server")
    logger.info(' ')

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

    def sync_serialize(self):
        """Serialize entity for a SYNC response.
        https://developers.google.com/actions/smarthome/create-app#actiondevicessync
        """
        state = self.state
        enableReport = ReportState.enable_report_state()
        traits = self.traits()

        # Found no supported traits for this entity
        if not traits:
            return None
        
        if enableReport == True:
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
            device['name']['nicknames'] = aliases

        # add room hint if annotated
        room = state.room
        if room:
            device['roomHint'] = room

        for trt in traits:
            device['attributes'].update(trt.sync_attributes())

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
 
                ack = self.state.ack #ack is now stored in state
                pin = False
                
                if configuration['Domoticz']['switchProtectionPass'] != False:
                    protect = self.state.protected
                else:
                    protect = False

                if protect or self.state.domain == securityDOMAIN:
                    pin = configuration['Domoticz']['switchProtectionPass']
                    if self.state.domain == securityDOMAIN:
                        pin = self.state.seccode 
                    ack = False
                    if challenge == None:
                        raise SmartHomeErrorNoChallenge(ERR_CHALLENGE_NEEDED, 'pinNeeded',
                            'Unable to execute {} for {} - challenge needed '.format(command, self.state.entity_id))
                    elif False == challenge.get('pin', False):
                        raise SmartHomeErrorNoChallenge(ERR_CHALLENGE_NEEDED, 'userCancelled',
                            'Unable to execute {} for {} - challenge needed '.format(command, self.state.entity_id))
                    elif True == protect and pin != challenge.get('pin'):
                        raise SmartHomeErrorNoChallenge(ERR_CHALLENGE_NEEDED, 'challengeFailedPinNeeded',
                            'Unable to execute {} for {} - challenge needed '.format(command, self.state.entity_id))
                    elif self.state.domain == securityDOMAIN and pin != hashlib.md5(str.encode(challenge.get('pin'))).hexdigest():
                        raise SmartHomeErrorNoChallenge(ERR_CHALLENGE_NEEDED, 'challengeFailedPinNeeded',
                            'Unable to execute {} for {} - challenge needed '.format(command, self.state.entity_id))
                            
                if ack:
                    if challenge == None:
                        raise SmartHomeErrorNoChallenge(ERR_CHALLENGE_NEEDED, 'ackNeeded',
                            'Unable to execute {} for {} - challenge needed '.format(command, self.state.entity_id))
                    elif False == challenge.get('ack', False):
                        raise SmartHomeErrorNoChallenge(ERR_CHALLENGE_NEEDED, 'userCancelled',
                            'Unable to execute {} for {} - challenge needed '.format(command, self.state.entity_id))
                    
                trt.execute(command, params)
                executed = True
                break
 
        if not executed:
            raise SmartHomeError(ERR_FUNCTION_NOT_SUPPORTED,
                'Unable to execute {} for {}'.format(command, self.state.entity_id))

    def async_update(self):
        """Update the entity with latest info from Domoticz."""                                        
        
        if self.state.domain == groupDOMAIN or self.state.domain == sceneDOMAIN:
            getDevices('scene')
        else:
            getDevices('id', self.state.id)   
        
        
class SmartHomeReqHandler(OAuthReqHandler):
    global smarthomeControlMappings    
    global aogDevs
    
    
    def __init__(self, *args, **kwargs):
        super(SmartHomeReqHandler, self).__init__(*args, **kwargs)
        self._request_id = None
        
    def report_state(self, states, token):
        """Send a state report to Google."""
        
        data = {
            'requestId': self._request_id,
            'agentUserId': token.get('userAgentId', None),
            'payload': {
                'devices':{
                    'states': states,
                }
            }     
        }
        ReportState.call_homegraph_api(REPORT_STATE_BASE_URL, data)
            
    def smarthome_process(self, message, token):
        request_id = self._request_id  # type: str
        inputs = message.get('inputs')  # type: list
    
        if len(inputs) != 1:
            return {'requestId': request_id, 'payload': {'errorCode': ERR_PROTOCOL_ERROR}}

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
        if a != None:
            type, tokenH = a.split()
            if type.lower() == 'bearer':
                token = Auth['tokens'].get(tokenH, None)
           
        if token == None:
            raise SmartHomeError(ERR_PROTOCOL_ERROR, 'not authorized access!!')
            return
    
        message = json.loads(s.body)
        
        self._request_id = message.get('requestId')
        
        logger.info("Request " + json.dumps(message, indent=2, sort_keys=False, ensure_ascii=False))
        response = self.smarthome_process(message, token)
               
        try:
            if 'errorCode' in response['payload']:
                logger.info('Error handling message %s: %s' % (message, response['payload']))
        except:
            pass
        s.send_json(200, json.dumps(response, ensure_ascii=False).encode('utf-8'), True)
        
        logger.info("Response " + json.dumps(response, indent=2, sort_keys=False, ensure_ascii=False))
    
    def smarthome(self, s):
        s.send_message(500, "not supported")
        
    def forceDevicesSync(self):
        userAgent = self.getUserAgent()
        enableReport = ReportState.enable_report_state()
        if userAgent == None:
            return 500 #internal error
            
        data = {"agentUserId": userAgent}
        if enableReport == True:
            r = ReportState.call_homegraph_api(REQUEST_SYNC_BASE_URL, data)
        elif 'Homegraph_API_Key' in configuration and configuration['Homegraph_API_Key'] != 'ADD_YOUR HOMEGRAPH_API_KEY_HERE':
            r = ReportState.call_homegraph_api_key(REQUEST_SYNC_BASE_URL, data)
        else:
            logger.error("No configuration for request_sync available")
            
        return r

    def syncDevices(self, s):
        user = self.getSessionUser()
        if user == None or user.get('uid', '') == '':
            s.redirect('/login?redirect_uri={0}'.format('/sync'))
            return
        
        r = self.forceDevicesSync()
        s.send_message(200, 'Synchronization request sent, status_code: ' + str(r))
         
    def settings(self, s):                            
        user = self.getSessionUser()
        if user == None or user.get('uid', '') == '':
            s.redirect('/login?redirect_uri={0}'.format('/settings'))
            return
            
        update = checkupdate()
        confJSON = json.dumps(configuration)
        public_url = getTunnelUrl()            
        message = ''
        meta = '<!-- <meta http-equiv="refresh" content="5"> -->'
        code = readFile(os.path.join(FILE_DIR, CONFIGFILE))
        logs = readFile(os.path.join(LOGFILEPATH, LOGFILE))
        template = TEMPLATE.format(message=message, uptime=uptime(), list=deviceList, meta=meta, code=code, conf=confJSON, public_url=public_url, logs=logs, update=update)

        s.send_message(200, template)     

    def settings_post(self, s):
        enableReport = ReportState.enable_report_state()
        update = checkupdate()
        confJSON = json.dumps(configuration)
        public_url = getTunnelUrl()
        logs = readFile(os.path.join(LOGFILEPATH, LOGFILE))
        code = readFile(os.path.join(FILE_DIR, CONFIGFILE))
        meta = '<!-- <meta http-equiv="refresh" content="5"> -->'
       
        if (s.form.get("save")):
            textToSave = s.form.get("save", None)
            codeToSave = textToSave.replace("+", " ")
            saveFile(CONFIGFILE, codeToSave)
            message = 'Config saved'
            logger.info(message) 
            logs = readFile(os.path.join(LOGFILEPATH, LOGFILE))
            code = readFile(os.path.join(FILE_DIR, CONFIGFILE))
            template = TEMPLATE.format(message=message, uptime=uptime(), list=deviceList, meta=meta, code=code, conf=confJSON, public_url=public_url, logs=logs, update=update)

            s.send_message(200, template)

        if (s.form.get("backup")):
            codeToSave = readFile(os.path.join(FILE_DIR, CONFIGFILE))
            saveFile('config.yaml.bak', codeToSave)
            message = 'Backup saved'
            logger.info(message)
            logs = readFile(os.path.join(LOGFILEPATH, LOGFILE))
            template = TEMPLATE.format(message=message, uptime=uptime(), list=deviceList, meta=meta, code=code, conf=confJSON, public_url=public_url, logs=logs, update=update)

            s.send_message(200, template)
        
        if (s.form.get("restart")):
            message = 'Restart Server, please wait a minute!'
            meta = '<meta http-equiv="refresh" content="20">'
            code = ''
            logs = ''
            
            template = TEMPLATE.format(message=message, uptime=uptime(), list=deviceList, meta=meta, code=code, conf=confJSON, public_url=public_url, logs=logs, update=update)
            
            s.send_message(200, template)
            restartServer()

        if (s.form.get("sync")):
            if 'Homegraph_API_Key' in configuration and configuration['Homegraph_API_Key'] != 'ADD_YOUR HOMEGRAPH_API_KEY_HERE' or enableReport == True:
                r = self.forceDevicesSync()
                time.sleep(0.5)
                if r == True:
                    message = 'Devices syncronized'
                else:
                    message = 'Homegraph api key not valid!'
            else:
                message = 'Add Homegraph api key or a Homegraph Service Account json file to sync devices here!'
            logs = readFile(os.path.join(LOGFILEPATH, LOGFILE))
            template = TEMPLATE.format(message=message, uptime=uptime(), list=deviceList, meta=meta, code=code, conf=confJSON, public_url=public_url, logs=logs, update=update)
            s.send_message(200, template)
        
        if (s.form.get("reload")):
            message = ''

            template = TEMPLATE.format(message=message, uptime=uptime(), list=deviceList, meta=meta, code=code, conf=confJSON, public_url=public_url, logs=logs, update=update)
            s.send_message(200, template)
            
        if (s.form.get("deletelogs")):
            logfile = os.path.join(LOGFILEPATH, LOGFILE)    
            if os.path.exists(logfile):
                f = open(logfile, 'w')
                f.close()
            logger.info('Logs removed by user')
            message = 'Logs removed'
            logs = readFile(os.path.join(LOGFILEPATH, LOGFILE))
            template = TEMPLATE.format(message=message, uptime=uptime(), list=deviceList, meta=meta, code=code, conf=confJSON, public_url=public_url, logs=logs, update=update)
            s.send_message(200, template)
            
        if (s.form.get("update")):
            repo.git.reset('--hard')
            repo.remotes.origin.pull()
            message = 'Updating to latest ' + repo.active_branch.name + ', please wait a minute!'
            meta = '<meta http-equiv="refresh" content="20">'

            template = TEMPLATE.format(message=message, uptime=uptime(), list=deviceList, meta=meta, code=code, conf=confJSON, public_url=public_url, logs=logs, update=update)
            s.send_message(200, template)
            restartServer()
            
    def delay_report_state(self, states, token):
        time.sleep(3)
        self.report_state(states, token)
                
    def smarthome_sync(self, payload, token):
        """Handle action.devices.SYNC request.
        https://developers.google.com/actions/smarthome/create-app#actiondevicessync
        """
        devices = []
        states = {}
        aogDevs.clear() 
        getDevices() #sync all devices
        getSettings()
        enableReport = ReportState.enable_report_state()
        
        for state in aogDevs.values():

            entity = _GoogleEntity(state)
            serialized = entity.sync_serialize()
            
            if serialized is None:
                continue

            devices.append(serialized)
            if state.report_state == True:
                try:                   
                    states[entity.entity_id] = entity.query_serialize()
                except:
                    continue          
            
        if enableReport == True:
            t = threading.Thread(target=self.delay_report_state, args=(states, token)).start()
        
        return {
            'agentUserId': token.get('userAgentId', None),
            'devices': devices,
        }
        
    def smarthome_query(self, payload, token):
        """Handle action.devices.QUERY request.
        https://developers.google.com/actions/smarthome/create-app#actiondevicesquery
        """
        devices = {}
        
        for device in payload.get('devices', []):
            devid = device['id']
            _GoogleEntity(aogDevs.get(devid, None)).async_update()
            state = aogDevs.get(devid, None)
            
            if not state:
                # If we can't find a state, the device is offline
                devices[devid] = {'online': False}
                continue

            e = _GoogleEntity(state)
            devices[devid] = e.query_serialize()
   
        return {'devices': devices}

    def smarthome_exec(self, payload, token):
        """Handle action.devices.EXECUTE request.
        https://developers.google.com/actions/smarthome/create-app#actiondevicesexecute
        """
        entities = {}
        results = {}
        states = {}
        enableReport = ReportState.enable_report_state()
        
        for command in payload['commands']:
            for device, execution in product(command['devices'],
                                             command['execution']):
                entity_id = device['id']
                new_state = execution.get('params')
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
                    entities[entity_id].execute(execution['command'], execution.get('params', {}), execution.get('challenge', None))
                    
                except SmartHomeError as err:
                    results[entity_id] = {'ids': [entity_id], 'status': 'ERROR', 'errorCode': err.code}
                    logger.error(err)
                except SmartHomeErrorNoChallenge as err:
                    results[entity_id] = {'ids': [entity_id], 'status': 'ERROR', 'errorCode': err.code, 'challengeNeeded': {'type': err.desc}}
                    logger.error(err)
                    
        final_results = list(results.values())

        for entity in entities.values():
            if entity.entity_id in results:
                continue
            entity.async_update()
            # final_results.append({'ids': [entity.entity_id], 'status': 'SUCCESS', 'states': entity.query_serialize()})
            final_results.append({'ids': [entity.entity_id], 'status': 'SUCCESS', 'states': new_state})
            if state.report_state == True:
                try:
                    # states[entity.entity_id] = entity.query_serialize()
                    states[entity.entity_id] = new_state
                except:
                    continue
   
        if state.report_state == True and enableReport == True:
            self.report_state(states, token)
      
        return {'commands': final_results}
   
    def smarthome_disconnect(self, payload, token):
        """Handle action.devices.DISCONNECT request.
        https://developers.google.com/assistant/smarthome/develop/process-intents#DISCONNECT
        """
        return None
    
if 'userinterface' in configuration and configuration['userinterface'] == True:
    smarthomeGetMappings = {"/smarthome": SmartHomeReqHandler.smarthome,
                            "/sync": SmartHomeReqHandler.syncDevices,
                            "/settings":SmartHomeReqHandler.settings}
                            
    smarthomePostMappings = {"/smarthome": SmartHomeReqHandler.smarthome_post,
                             "/settings": SmartHomeReqHandler.settings_post}
else:
    smarthomeGetMappings = {"/smarthome": SmartHomeReqHandler.smarthome,
                            "/sync": SmartHomeReqHandler.syncDevices}
                        
    smarthomePostMappings = {"/smarthome": SmartHomeReqHandler.smarthome_post}

smarthomeControlMappings = {'action.devices.SYNC': SmartHomeReqHandler.smarthome_sync,
                            'action.devices.QUERY': SmartHomeReqHandler.smarthome_query,
                            'action.devices.EXECUTE': SmartHomeReqHandler.smarthome_exec,
                            'action.devices.DISCONNECT': SmartHomeReqHandler.smarthome_disconnect}
                            
