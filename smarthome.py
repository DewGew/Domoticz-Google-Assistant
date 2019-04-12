# -*- coding: utf-8 -*-

from auth import *
import requests
import json
from itertools import product
import states
import trait
from collections.abc import Mapping

from config import (DOMOTICZ_GET_ALL_DEVICES_URL, U_NAME_DOMOTICZ, U_PASSWD_DOMOTICZ, 
    DOMOTICZ_GET_ONE_DEVICE_URL, DOMOTICZ_GET_SCENES_URL, DOMOTICZ_SWITCH_PROTECTION_PASSWD,
    Auth, REQUEST_SYNC_BASE_URL, SMARTHOMEPROVIDERAPIKEY,
    TYPE_LIGHT, TYPE_LOCK, TYPE_SCENE, TYPE_SWITCH, TYPE_VACUUM, TYPE_DOOR,TYPE_MEDIA,
    TYPE_THERMOSTAT, TYPE_FAN, TYPE_BLINDS, TYPE_SCREEN, TYPE_SECURITY,
    ERR_FUNCTION_NOT_SUPPORTED, ERR_PROTOCOL_ERROR, ERR_DEVICE_OFFLINE,
    ERR_UNKNOWN_ERROR, ERR_CHALLENGE_NEEDED,
    groupDOMAIN, sceneDOMAIN, lightDOMAIN, switchDOMAIN, blindsDOMAIN, screenDOMAIN,
    climateDOMAIN, tempDOMAIN, lockDOMAIN, invlockDOMAIN, colorDOMAIN, mediaDOMAIN,
    securityDOMAIN, ATTRS_BRIGHTNESS,ATTRS_THERMSTATSETPOINT,ATTRS_COLOR,
    DEVICE_CONFIG, SCENE_CONFIG,
    IMAGE_SWITCH, IMAGE_LIGHT, IMAGE_MEDIA)

from helpers import SmartHomeError, SmartHomeErrorNoChallenge    
    
DOMOTICZ_TO_GOOGLE_TYPES = {
    groupDOMAIN: TYPE_SWITCH,
    sceneDOMAIN: TYPE_SCENE,
    lightDOMAIN: TYPE_LIGHT,
    switchDOMAIN: TYPE_SWITCH,
    blindsDOMAIN: TYPE_BLINDS,
    screenDOMAIN: TYPE_SCREEN,
    climateDOMAIN: TYPE_THERMOSTAT,
    tempDOMAIN: TYPE_THERMOSTAT,
    lockDOMAIN: TYPE_LOCK,
    invlockDOMAIN: TYPE_LOCK,
    colorDOMAIN: TYPE_LIGHT,
    mediaDOMAIN: TYPE_MEDIA,
    securityDOMAIN: TYPE_SECURITY,
} 
 
#some way to convert a domain type: Domoticz to google
def AogGetDomain(device):
    if device["Type"] in ['Light/Switch', 'Lighting 1', 'Lighting 2']:
        if device["SwitchType"] in ['Blinds', 'Venetian Blinds EU', 'Venetian Blinds US'] :
            return blindsDOMAIN
        elif 'Door Lock' == device["SwitchType"]:
            return lockDOMAIN
        elif 'Door Lock Inverted' == device["SwitchType"]:
            return invlockDOMAIN
        elif device["Image"] in IMAGE_SWITCH:
            return switchDOMAIN
        elif device["Image"] in IMAGE_LIGHT:
            return lightDOMAIN
        elif device["Image"] in IMAGE_MEDIA:
            return mediaDOMAIN
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
    elif 'Color Switch' == device["Type"]:
        return colorDOMAIN
    elif 'Security' == device["Type"]:
        return securityDOMAIN
    return None
    
def getDesc(state):
    desc = SCENE_CONFIG.get(state.id, None) if state.domain == sceneDOMAIN or state.domain == groupDOMAIN else DEVICE_CONFIG.get(state.id, None)    
    return desc
        
def getAog(device):
    getSettings()
    domain = AogGetDomain(device)
    if domain == None:
        return None
        
    aog = states.AogState()
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
    
    if lightDOMAIN == aog.domain and "Dimmer" == device["SwitchType"]:
        aog.attributes = ATTRS_BRIGHTNESS
    if colorDOMAIN == aog.domain and "Color Switch" == device["Type"]:
        aog.attributes = ATTRS_COLOR
    if climateDOMAIN == aog.domain and "Thermostat" == device["Type"]:
        aog.attributes = ATTRS_THERMSTATSETPOINT
        
    desc = getDesc(aog)
    
    if desc != None:
        n = desc.get('nicknames', None)
        if n != None:
            aog.nicknames = n
        r = desc.get('room', None)
        if r != None:
            aog.room = r
    return aog;
 
 
aogDevs = {} 
def getDevices(type = "all", id = "0"):
    global aogDevs

    url = ""
    if "all" == type:  
        url = DOMOTICZ_GET_ALL_DEVICES_URL
    elif "scene" == type:  
        url = DOMOTICZ_GET_SCENES_URL
    elif "id" == type:  
        url = DOMOTICZ_GET_ONE_DEVICE_URL + id
        
    r = requests.get(url, auth=(U_NAME_DOMOTICZ, U_PASSWD_DOMOTICZ))
    if r.status_code == 200:
        devs = r.json()['result']
        for d in devs:
            aog = getAog(d)
            if aog == None:
                continue

            aogDevs[aog.entity_id] = aog
            
    #print([(d.name.encode('utf-8', 'ignore'), d.id, d.domain) for d in aogDevs.values()])        
        
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
    
    url = DOMOTICZ_GET_SETTINGS_URL
    r = requests.get(url, auth=(U_NAME_DOMOTICZ, U_PASSWD_DOMOTICZ))
    
    if r.status_code == 200:
        devs = r.json()
        settings['SecPassword'] = devs['SecPassword']
        settings['ProtectionPassword'] = devs['ProtectionPassword']
        
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

        # When a state is unavailable, the attributes that describe
        # capabilities will be stripped. For example, a light entity will miss
        # the min/max mireds. Therefore they will be excluded from a sync.
        # if state.state == STATE_UNAVAILABLE:
            # return None

        traits = self.traits()

        # Found no supported traits for this entity
        if not traits:
            return None

        device = {
            'id': state.entity_id,
            'name': {
                'name': state.name
            },
            'attributes': {},
            'traits': [trait.name for trait in traits],
            'willReportState': False,
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
                    
                ack = False
                pin = False
                desc = getDesc(self.state)
                if desc != None:
                    ack = desc.get('ack', False)
                
                if DOMOTICZ_SWITCH_PROTECTION_PASSWD != False:
                    protect = self.state.protected
                else:
                    protect = False

                if protect or self.state.domain == securityDOMAIN:
                    pin = DOMOTICZ_SWITCH_PROTECTION_PASSWD
                    if self.state.domain == securityDOMAIN:
                        pin = DOMOTICZ_SECCODE
                    ack = False
                    if challenge == None:
                        raise SmartHomeErrorNoChallenge(ERR_CHALLENGE_NEEDED, 'pinNeeded',
                            'Unable to execute {} for {} - challenge needed '.format(command, self.state.entity_id))
                    elif False == challenge.get('pin', False):
                        raise SmartHomeErrorNoChallenge(ERR_CHALLENGE_NEEDED, 'userCancelled',
                            'Unable to execute {} for {} - challenge needed '.format(command, self.state.entity_id))
                    elif pin != challenge.get('pin'):
                        raise SmartHomeErrorNoChallenge(ERR_CHALLENGE_NEEDED, 'challengeFailedPinNeeded',
                            'Unable to execute {} for {} - challenge needed '.format(command, self.state.entity_id))
                            
                if ack:
                    print(challenge)
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
        
    def smarthome_process(self, message, token):
        request_id = message.get('requestId')  # type: str
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
            print(e)
            return {'requestId': request_id, 'payload': {'errorCode': ERR_UNKNOWN_ERROR}}
        
        
    def smarthome_post(self, s):
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
        print(message)
        response = self.smarthome_process(message, token)
        
        try:
            if 'errorCode' in response['payload']:
                print('Error handling message %s: %s' % (message, response['payload']))
        except:
            pass
        s.send_json(200, json.dumps(response, ensure_ascii=False).encode('utf-8'), True)
    
    def smarthome(self, s):
        s.send_message(500, "not supported")
        
    def forceDevicesSync(self):
        userAgent = self.getUserAgent()
        
        if userAgent == None:
            return 500 #internal error
        
        url = REQUEST_SYNC_BASE_URL + '?key=' + SMARTHOMEPROVIDERAPIKEY
        j = {"agentUserId": userAgent}
        
        r = requests.post(url, json=j)

        return r.status_code

    def syncDevices(self, s):
        user = self.getSessionUser()
        if user == None or user.get('uid', '') == '':
            s.redirect('/login?redirect_uri={0}'.format('/sync'))
            return
        
        # authCode = s.query_components.get("code", "")
        # authCode = self.authCode(authCode)
        # if authCode == None:
            # s.send_message(400, "incorrect client data")
            # return
        
        r = self.forceDevicesSync()
        s.send_message(200, 'Synchronization request sent, status_code: ' + str(r))
       

    def smarthome_sync(self, payload, token):
        """Handle action.devices.SYNC request.
        https://developers.google.com/actions/smarthome/create-app#actiondevicessync
        """
        devices = []
        getDevices() #sync all devices
        
        for state in aogDevs.values():
            # if state.entity_id in CLOUD_NEVER_EXPOSED_ENTITIES:
                # continue

            # if not config.should_expose(state):
                # continue

            entity = _GoogleEntity(state)
            serialized = entity.sync_serialize()

            if serialized is None:
                continue

            devices.append(serialized)
        
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
            state = aogDevs.get(devid, None)

            if not state:
                # If we can't find a state, the device is offline
                devices[devid] = {'online': False}
                continue

            e = _GoogleEntity(state)
            e.async_update()
            devices[devid] = e.query_serialize()

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
                     
                    state = aogDevs.get(entity_id, None)
                    if state is None:
                        results[entity_id] = {'ids': [entity_id], 'status': 'ERROR', 'errorCode': ERR_DEVICE_OFFLINE}
                        continue

                    entities[entity_id] = _GoogleEntity(state)

                try:
                    entities[entity_id].execute(execution['command'], execution.get('params', {}), execution.get('challenge', None))
                    
                except SmartHomeError as err:
                    results[entity_id] = {'ids': [entity_id], 'status': 'ERROR', 'errorCode': err.code}
                    print(err)
                except SmartHomeErrorNoChallenge as err:
                    results[entity_id] = {'ids': [entity_id], 'status': 'ERROR', 'errorCode': err.code, 'challengeNeeded': {'type': err.desc}}
                    print(err)
                    
        final_results = list(results.values())

        for entity in entities.values():
            if entity.entity_id in results:
                continue
            entity.async_update()
            final_results.append({'ids': [entity.entity_id], 'status': 'SUCCESS', 'states': entity.query_serialize()})
            
        return {'commands': final_results}  
           
           
def turned_off_response(message):
    """Return a device turned off response."""
    return {'requestId': message.get('requestId'), 'payload': {'errorCode': 'deviceTurnedOff'}}   


smarthomeGetMappings = {"/smarthome": SmartHomeReqHandler.smarthome,
                        "/sync": SmartHomeReqHandler.syncDevices}

smarthomePostMappings = {"/smarthome": SmartHomeReqHandler.smarthome_post}

smarthomeControlMappings = {'action.devices.SYNC': SmartHomeReqHandler.smarthome_sync,
                            'action.devices.QUERY': SmartHomeReqHandler.smarthome_query,
                            'action.devices.EXECUTE': SmartHomeReqHandler.smarthome_exec}
                            
