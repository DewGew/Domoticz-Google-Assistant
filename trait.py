# -*- coding: utf-8 -*-

import requests
import json

from config import (DOMOTICZ_URL, U_NAME_DOMOTICZ, U_PASSWD_DOMOTICZ, DOMOTICZ_SWITCH_PROTECTION_PASSWD,
    groupDOMAIN, sceneDOMAIN, lightDOMAIN, switchDOMAIN, blindsDOMAIN, screenDOMAIN, climateDOMAIN, tempDOMAIN, colorDOMAIN,
    mediaDOMAIN, securityDOMAIN, lockDOMAIN, invlockDOMAIN, outletDOMAIN, pushDOMAIN, ATTRS_COLOR, ATTRS_BRIGHTNESS, ATTRS_THERMSTATSETPOINT,
    ERR_ALREADY_IN_STATE, ERR_WRONG_PIN)

from helpers import SmartHomeError
    
PREFIX_TRAITS = 'action.devices.traits.'
TRAIT_ONOFF = PREFIX_TRAITS + 'OnOff'
TRAIT_DOCK = PREFIX_TRAITS + 'Dock'
TRAIT_STARTSTOP = PREFIX_TRAITS + 'StartStop'
TRAIT_BRIGHTNESS = PREFIX_TRAITS + 'Brightness'
TRAIT_COLOR_SETTING = PREFIX_TRAITS + 'ColorSetting'
TRAIT_SCENE = PREFIX_TRAITS + 'Scene'
TRAIT_TEMPERATURE_CONTROL = PREFIX_TRAITS + 'TemperatureControl'
TRAIT_TEMPERATURE_SETTING = PREFIX_TRAITS + 'TemperatureSetting'
TRAIT_LOCKUNLOCK = PREFIX_TRAITS + 'LockUnlock'
TRAIT_FANSPEED = PREFIX_TRAITS + 'FanSpeed'
TRAIT_MODES = PREFIX_TRAITS + 'Modes'
TRAIT_OPEN_CLOSE = PREFIX_TRAITS + 'OpenClose'
TRAIT_ARM_DISARM = PREFIX_TRAITS + 'ArmDisarm'

PREFIX_COMMANDS = 'action.devices.commands.'
COMMAND_ONOFF = PREFIX_COMMANDS + 'OnOff'
COMMAND_DOCK = PREFIX_COMMANDS + 'Dock'
COMMAND_STARTSTOP = PREFIX_COMMANDS + 'StartStop'
COMMAND_PAUSEUNPAUSE = PREFIX_COMMANDS + 'PauseUnpause'
COMMAND_BRIGHTNESS_ABSOLUTE = PREFIX_COMMANDS + 'BrightnessAbsolute'
COMMAND_COLOR_ABSOLUTE = PREFIX_COMMANDS + 'ColorAbsolute'
COMMAND_ACTIVATE_SCENE = PREFIX_COMMANDS + 'ActivateScene'
COMMAND_THERMOSTAT_TEMPERATURE_SETPOINT = (
    PREFIX_COMMANDS + 'ThermostatTemperatureSetpoint')
COMMAND_THERMOSTAT_TEMPERATURE_SET_RANGE = (
    PREFIX_COMMANDS + 'ThermostatTemperatureSetRange')
COMMAND_THERMOSTAT_SET_MODE = PREFIX_COMMANDS + 'ThermostatSetMode'
COMMAND_LOCKUNLOCK = PREFIX_COMMANDS + 'LockUnlock'
COMMAND_FANSPEED = PREFIX_COMMANDS + 'SetFanSpeed'
COMMAND_MODES = PREFIX_COMMANDS + 'SetModes'
COMMAND_OPEN_CLOSE = PREFIX_COMMANDS + 'OpenClose'
COMMAND_ARM_DISARM = PREFIX_COMMANDS + 'ArmDisarm'

TRAITS = []


def register_trait(trait):
    """Decorate a function to register a trait."""
    TRAITS.append(trait)
    return trait   
    
class _Trait:
    """Represents a Trait inside Google Assistant skill."""

    commands = []

    def __init__(self, state):
        """Initialize a trait for a state."""
        self.state = state

    def sync_attributes(self):
        """Return attributes for a sync request."""
        raise NotImplementedError

    def query_attributes(self):
        """Return the attributes of this trait for this entity."""
        raise NotImplementedError

    def can_execute(self, command, params):
        """Test if command can be executed."""
        return command in self.commands

    async def execute(self, command, params):
        """Execute a trait command."""
        raise NotImplementedError


@register_trait
class OnOffTrait(_Trait):
    """Trait to offer basic on and off functionality.
    https://developers.google.com/actions/smarthome/traits/onoff
    """

    name = TRAIT_ONOFF
    commands = [
        COMMAND_ONOFF
    ]

    @staticmethod
    def supported(domain, features):
        """Test if state is supported."""

        return domain in (
            groupDOMAIN,
            switchDOMAIN,
            lightDOMAIN,
            colorDOMAIN,
            mediaDOMAIN,
            outletDOMAIN,
            pushDOMAIN,
        )

    def sync_attributes(self):
        """Return OnOff attributes for a sync request."""
        return {}

    def query_attributes(self):
        """Return OnOff query attributes."""
        domain = self.state.domain
        if domain == pushDOMAIN:
            return {'on': False}
        else:
            return {'on': self.state.state != 'Off'}
    
    def execute(self, command, params):
        """Execute an OnOff command."""
        domain = self.state.domain
        protected = self.state.protected

        if domain == groupDOMAIN:
            url = DOMOTICZ_URL + '/json.htm?type=command&param=switchscene&idx=' + self.state.id + '&switchcmd=' + ('On' if params['on'] else 'Off')
        else:
            url = DOMOTICZ_URL + '/json.htm?type=command&param=switchlight&idx=' + self.state.id + '&switchcmd=' + ('On' if params['on'] else 'Off')
        
        if protected:
            url = url + '&passcode=' + DOMOTICZ_SWITCH_PROTECTION_PASSWD
            
        # print(url)
        r = requests.get(url, auth=(U_NAME_DOMOTICZ, U_PASSWD_DOMOTICZ))
        if protected:
            status = r.json()
            err = status.get('status')
            if err == 'ERROR':
                raise SmartHomeError(ERR_WRONG_PIN,
                    'Unable to execute {} for {} check your settings'.format(command, self.state.entity_id))
        
@register_trait
class SceneTrait(_Trait):
    """Trait to offer scene functionality.
    https://developers.google.com/actions/smarthome/traits/scene
    """

    name = TRAIT_SCENE
    commands = [
        COMMAND_ACTIVATE_SCENE
    ]

    @staticmethod
    def supported(domain, features):
        """Test if state is supported."""
        return domain in sceneDOMAIN

    def sync_attributes(self):
        """Return scene attributes for a sync request."""
        # Neither supported domain can support sceneReversible
        return {}

    def query_attributes(self):
        """Return scene query attributes."""
        return {}

    def execute(self, command, params):
        """Execute a scene command."""
        protected = self.state.protected
        
        url = DOMOTICZ_URL + '/json.htm?type=command&param=switchscene&idx=' + self.state.id + '&switchcmd=On'
        
        if protected:
            url = url + '&passcode=' + DOMOTICZ_SWITCH_PROTECTION_PASSWD
            
        # print(url)
        r = requests.get(url, auth=(U_NAME_DOMOTICZ, U_PASSWD_DOMOTICZ))
        if protected:
            status = r.json()
            err = status.get('status')
            if err == 'ERROR':
                raise SmartHomeError(ERR_WRONG_PIN,
                    'Unable to execute {} for {} check your settings'.format(command, self.state.entity_id))

@register_trait
class BrightnessTrait(_Trait):
    """Trait to control brightness of a device.
    https://developers.google.com/actions/smarthome/traits/brightness
    """

    name = TRAIT_BRIGHTNESS
    commands = [
        COMMAND_BRIGHTNESS_ABSOLUTE
    ]

    @staticmethod
    def supported(domain, features):
        """Test if state is supported."""
        if domain in (lightDOMAIN, colorDOMAIN, outletDOMAIN):
            return features & ATTRS_BRIGHTNESS
 
        return False

    def sync_attributes(self):
        """Return brightness attributes for a sync request."""
        return {}

    def query_attributes(self):
        """Return brightness query attributes."""
        domain = self.state.domain
        response = {}

        if domain == lightDOMAIN or domain == outletDOMAIN:
            brightness = self.state.level
            response['brightness'] = int(brightness * 100 / self.state.maxdimlevel)
        if domain == colorDOMAIN:
            brightness = self.state.level
            response['brightness'] = int(brightness * 100 / self.state.maxdimlevel)

        return response

    def can_execute(self, command, params):
        """Test if command can be executed."""
        protected = self.state.protected
        if protected:
            raise SmartHomeError('notSupported',
                'Unable to execute {} for {} check your settings'.format(command, self.state.entity_id))
        return command in self.commands
        
    def execute(self, command, params):
        """Execute a brightness command."""
        #domain = self.state.domain
        protected = self.state.protected
                    
        url = DOMOTICZ_URL + '/json.htm?type=command&param=switchlight&idx=' + self.state.id + '&switchcmd=Set%20Level&level=' + str(int(params['brightness'] * self.state.maxdimlevel / 100))
        
        if protected:
            url = url + '&passcode=' + DOMOTICZ_SWITCH_PROTECTION_PASSWD
            
        # print(url)
        r = requests.get(url, auth=(U_NAME_DOMOTICZ, U_PASSWD_DOMOTICZ))
        if protected:
            status = r.json()
            err = status.get('status')
            if err == 'ERROR':
                raise SmartHomeError(ERR_WRONG_PIN,
                    'Unable to execute {} for {} check your settings'.format(command, self.state.entity_id))
                
            
            
@register_trait
class OpenCloseTrait(_Trait):
    """Trait to offer open/close control functionality.
    https://github.com/actions-on-google/smart-home-nodejs/issues/253
    """

    name = TRAIT_OPEN_CLOSE
    commands = [
        COMMAND_OPEN_CLOSE
    ]

    @staticmethod
    def supported(domain, features):
        """Test if state is supported."""
        return domain in (blindsDOMAIN,
                            screenDOMAIN)

    def sync_attributes(self):
        """Return OpenClose attributes for a sync request."""
        # Neither supported domain can support sceneReversible
        return {}

    def query_attributes(self):
        """Return OpenClose query attributes."""
        return {}

    def execute(self, command, params):
        """Execute a OpenClose command."""
        protected = self.state.protected
        p = params.get('openPercent', 50)
        
        url = DOMOTICZ_URL + '/json.htm?type=command&param=switchlight&idx=' + self.state.id + '&switchcmd='
        
        if p == 100:
            #open
            url += 'Off'
        elif p == 0:
            #close
            url += 'On'
        else:
            #stop
            url += 'Stop'
            
        if protected:
            url = url + '&passcode=' + DOMOTICZ_SWITCH_PROTECTION_PASSWD
            
        # print(url)
        r = requests.get(url, auth=(U_NAME_DOMOTICZ, U_PASSWD_DOMOTICZ))
        if protected:
            status = r.json()
            err = status.get('status')
            if err == 'ERROR':
                raise SmartHomeError(ERR_WRONG_PIN,
                    'Unable to execute {} for {} check your settings'.format(command, self.state.entity_id))
        
@register_trait 
class TemperatureSettingTrait(_Trait):
    """Trait to offer handling both temperature point and modes functionality.

    https://developers.google.com/actions/smarthome/traits/temperaturesetting
    """

    name = TRAIT_TEMPERATURE_SETTING
    commands = [
        COMMAND_THERMOSTAT_TEMPERATURE_SETPOINT,
        COMMAND_THERMOSTAT_TEMPERATURE_SET_RANGE,
        COMMAND_THERMOSTAT_SET_MODE,
    ]

    @staticmethod
    def supported(domain, features):
        """Test if state is supported."""
        if domain == climateDOMAIN:
            return features & ATTRS_THERMSTATSETPOINT
        else:    
            return domain in tempDOMAIN

    def sync_attributes(self):
        """Return temperature point and modes attributes for a sync request."""       
        if self.state.tempunit:
            return {'thermostatTemperatureUnit': 'F'}
        else:
            return {'thermostatTemperatureUnit': 'C'}

    def query_attributes(self):
        """Return temperature point and modes query attributes."""
        domain = self.state.domain
        response = {}
        
        if domain == tempDOMAIN:
            response['thermostatMode'] = 'heat'
            current_temp = self.state.temp
            if current_temp is not None:
                response['thermostatTemperatureAmbient'] = current_temp
                response['thermostatTemperatureSetpoint'] = current_temp
            current_humidity = self.state.humidity
            if current_humidity is not None:
                response['thermostatHumidityAmbient'] = current_humidity
            
        if domain == climateDOMAIN:
            response['thermostatMode'] = 'heat'
            current_temp = self.state.state
            if current_temp is not None:
                response['thermostatTemperatureAmbient'] = float(current_temp)
            setpoint = self.state.setpoint
            if setpoint is not None:
                response['thermostatTemperatureSetpoint'] = float(setpoint)
            
        return response
        
    def execute(self, command, params):
        """Execute a temperature point or mode command."""
        # All sent in temperatures are always in Celsius
        if command == COMMAND_THERMOSTAT_TEMPERATURE_SETPOINT:
            url = DOMOTICZ_URL + '/json.htm?type=command&param=setsetpoint&idx=' + self.state.id + '&setpoint=' + str(params['thermostatTemperatureSetpoint'])

        # print(url)
        r = requests.get(url, auth=(U_NAME_DOMOTICZ, U_PASSWD_DOMOTICZ))
        # print(r.status_code)
          
@register_trait
class LockUnlockTrait(_Trait):
    """Trait to lock or unlock a lock.
    https://developers.google.com/actions/smarthome/traits/lockunlock
    """

    name = TRAIT_LOCKUNLOCK
    commands = [
        COMMAND_LOCKUNLOCK
    ]
    

    @staticmethod
    def supported(domain, features):
        """Test if state is supported."""
        return domain in (lockDOMAIN,
                            invlockDOMAIN)

    def sync_attributes(self):
        """Return LockUnlock attributes for a sync request."""     
        return {}

    def query_attributes(self):
        """Return LockUnlock query attributes."""
        return {'isLocked' : self.state.state == 'Locked'}
        
    def execute(self, command, params):
        """Execute an LockUnlock command."""
        domain = self.state.domain
        state = self.state.state
        protected = self.state.protected
        print(state)
        if domain == lockDOMAIN:
            if params['lock'] == True and state == 'Unlocked':
                url = DOMOTICZ_URL + '/json.htm?type=command&param=switchlight&idx=' + self.state.id + '&switchcmd=On'
            elif params['lock'] == False and state == 'Locked':
                url = DOMOTICZ_URL + '/json.htm?type=command&param=switchlight&idx=' + self.state.id + '&switchcmd=Off'
            else:             
                raise SmartHomeError(ERR_ALREADY_IN_STATE,
                    'Unable to execute {} for {}. Already in state '.format(command, self.state.entity_id))
        else:
            if params['lock'] == True and state == 'Unlocked':
                url = DOMOTICZ_URL + '/json.htm?type=command&param=switchlight&idx=' + self.state.id + '&switchcmd=Off'
            elif params['lock'] == False and state == 'Locked':
                url = DOMOTICZ_URL + '/json.htm?type=command&param=switchlight&idx=' + self.state.id + '&switchcmd=On'
            else:             
                raise SmartHomeError(ERR_ALREADY_IN_STATE,
                    'Unable to execute {} for {}. Already in state '.format(command, self.state.entity_id))
        
        if protected:
            url = url + '&passcode=' + DOMOTICZ_SWITCH_PROTECTION_PASSWD
            
        # print(url)
        r = requests.get(url, auth=(U_NAME_DOMOTICZ, U_PASSWD_DOMOTICZ))
        if protected:
            status = r.json()
            err = status.get('status')
            if err == 'ERROR':
                raise SmartHomeError(ERR_WRONG_PIN,
                    'Unable to execute {} for {} check your settings'.format(command, self.state.entity_id))

@register_trait
class ColorSettingTrait(_Trait):
    """Trait to offer color setting functionality.
    https://developers.google.com/actions/smarthome/traits/colorsetting
    """

    name = TRAIT_COLOR_SETTING
    commands = [
        COMMAND_COLOR_ABSOLUTE
    ]

    @staticmethod
    def supported(domain, features):
        """Test if state is supported."""
        if domain == colorDOMAIN:
            return features & ATTRS_COLOR

        return False

    def sync_attributes(self):
        """Return color setting attributes for a sync request."""
        # Other colorModel is hsv
        return {'colorModel': 'rgb',
                'colorTemperatureRange': {
                    'temperatureMinK': 1700,
                    'temperatureMaxK': 6500}
                ,}

    def query_attributes(self):
        """Return color setting query attributes."""
        response = {}

        color_rgb = json.loads(self.state.color)
        
        if color_rgb is not None:
            #Convert RGB to decimal
            color_decimal = color_rgb["r"] * 65536 + color_rgb["g"] * 256 + color_rgb["b"]
            
            response['color'] = {'spectrumRGB': color_decimal}

        return response

    def can_execute(self, command, params):
        """Test if command can be executed."""
        return (command in self.commands and
                'spectrumRGB' in params.get('color', {}))

    def execute(self, command, params):
        """Execute a color setting command."""
        
        #Convert decimal to hex
        setcolor = params['color']
        color_hex = hex(setcolor['spectrumRGB'])[2:]
        
        url = DOMOTICZ_URL + '/json.htm?type=command&param=setcolbrightnessvalue&idx=' + self.state.id + '&hex=' + str(color_hex)
        
        #print(url)
        r = requests.get(url, auth=(U_NAME_DOMOTICZ, U_PASSWD_DOMOTICZ))
        #print(r.status_code)
        
@register_trait
class ArmDisarmTrait(_Trait):
    """Trait to offer basic on and off functionality.
    https://developers.google.com/actions/smarthome/traits/ArmDisarm
    """

    name = TRAIT_ARM_DISARM
    commands = [
        COMMAND_ARM_DISARM
    ]

    @staticmethod
    def supported(domain, features):
        """Test if state is supported."""
        return domain in securityDOMAIN

    def sync_attributes(self):
        """Return ArmDisarm attributes for a sync request."""
        return {}

    def query_attributes(self):
        """Return ArmDisarm query attributes."""
        return {'isArmed': self.state.state != 'Normal'}
        
    def execute(self, command, params):
        """Execute an ArmDisarm command."""
        state = self.state.state
        seccode = self.state.seccode
        if params['arm'] ==  False or (params['arm'] ==  True and params['cancel'] == True):
            if state == 'Normal':
                raise SmartHomeError(ERR_ALREADY_IN_STATE,
                    'Unable to execute {} for {} '.format(command, self.state.entity_id))
            else:
                url = DOMOTICZ_URL + '/json.htm?type=command&param=setsecstatus&secstatus=0&seccode=' + seccode
        elif params['arm'] == True:
            if state != 'Normal':
                raise SmartHomeError(ERR_ALREADY_IN_STATE,
                    'Unable to execute {} for {} '.format(command, self.state.entity_id))
            else:
                url = DOMOTICZ_URL + '/json.htm?type=command&param=setsecstatus&secstatus=1&seccode=' + seccode
            
        r = requests.get(url, auth=(U_NAME_DOMOTICZ, U_PASSWD_DOMOTICZ))
