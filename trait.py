# -*- coding: utf-8 -*-

import base64
import json
import requests

from datetime import datetime
from helpers import SmartHomeError, configuration, logger, tempConvert
from const import (
    ATTRS_BRIGHTNESS,
    ATTRS_THERMSTATSETPOINT,
    ATTRS_COLOR,
    ATTRS_COLOR_TEMP,
    ATTRS_PERCENTAGE,
    ATTRS_VACUUM_MODES,
    DOMAINS,
    ERR_ALREADY_IN_STATE,
    ERR_WRONG_PIN,
    ERR_NOT_SUPPORTED,
    ATTRS_FANSPEED
)

DOMOTICZ_URL = configuration['Domoticz']['ip'] + ':' + configuration['Domoticz']['port']

PREFIX_TRAITS = 'action.devices.traits.'
TRAIT_ONOFF = f'{PREFIX_TRAITS}OnOff'
TRAIT_DOCK = f'{PREFIX_TRAITS}Dock'
TRAIT_STARTSTOP = f'{PREFIX_TRAITS}StartStop'
TRAIT_BRIGHTNESS = f'{PREFIX_TRAITS}Brightness'
TRAIT_COLOR_SETTING = f'{PREFIX_TRAITS}ColorSetting'
TRAIT_SCENE = f'{PREFIX_TRAITS}Scene'
TRAIT_TEMPERATURE_CONTROL = f'{PREFIX_TRAITS}TemperatureControl'
TRAIT_TEMPERATURE_SETTING = f'{PREFIX_TRAITS}TemperatureSetting'
TRAIT_LOCKUNLOCK = f'{PREFIX_TRAITS}LockUnlock'
TRAIT_FANSPEED = f'{PREFIX_TRAITS}FanSpeed'
TRAIT_MODES = f'{PREFIX_TRAITS}Modes'
TRAIT_OPEN_CLOSE = f'{PREFIX_TRAITS}OpenClose'
TRAIT_ARM_DISARM = f'{PREFIX_TRAITS}ArmDisarm'
TRAIT_VOLUME = f'{PREFIX_TRAITS}Volume'
TRAIT_CAMERA_STREAM = f'{PREFIX_TRAITS}CameraStream'
TRAIT_TOGGLES = f'{PREFIX_TRAITS}Toggles'
TRAIT_TIMER = f'{PREFIX_TRAITS}Timer'
TRAIT_ENERGY = f'{PREFIX_TRAITS}EnergyStorage'
TRAIT_HUMIDITY = f'{PREFIX_TRAITS}HumiditySetting'
TRAIT_OBJECTDETECTION = f'{PREFIX_TRAITS}ObjectDetection'
TRAIT_SENSOR_STATE = f'{PREFIX_TRAITS}SensorState'

PREFIX_COMMANDS = 'action.devices.commands.'
COMMAND_ONOFF = f'{PREFIX_COMMANDS}OnOff'
COMMAND_DOCK = f'{PREFIX_COMMANDS}Dock'
COMMAND_STARTSTOP = f'{PREFIX_COMMANDS}StartStop'
COMMAND_PAUSEUNPAUSE = f'{PREFIX_COMMANDS}PauseUnpause'
COMMAND_BRIGHTNESS_ABSOLUTE = f'{PREFIX_COMMANDS}BrightnessAbsolute'
COMMAND_COLOR_ABSOLUTE = f'{PREFIX_COMMANDS}ColorAbsolute'
COMMAND_ACTIVATE_SCENE = f'{PREFIX_COMMANDS}ActivateScene'
COMMAND_THERMOSTAT_TEMPERATURE_SETPOINT = (
        f'{PREFIX_COMMANDS}ThermostatTemperatureSetpoint'
        )
COMMAND_THERMOSTAT_TEMPERATURE_SET_RANGE = (
        f'{PREFIX_COMMANDS}ThermostatTemperatureSetRange'
        )
COMMAND_THERMOSTAT_SET_MODE = f'{PREFIX_COMMANDS}ThermostatSetMode'
COMMAND_THERMOSTAT_TEMPERATURE_RELATIVE = f'{PREFIX_COMMANDS}TemperatureRelative'
COMMAND_SET_TEMPERATURE = f'{PREFIX_COMMANDS}SetTemperature'
COMMAND_LOCKUNLOCK = f'{PREFIX_COMMANDS}LockUnlock'
COMMAND_FANSPEED = f'{PREFIX_COMMANDS}SetFanSpeed'
COMMAND_MODES = f'{PREFIX_COMMANDS}SetModes'
COMMAND_OPEN_CLOSE = f'{PREFIX_COMMANDS}OpenClose'
COMMAND_ARM_DISARM = f'{PREFIX_COMMANDS}ArmDisarm'
COMMAND_SET_VOLUME = f'{PREFIX_COMMANDS}setVolume'
COMMAND_VOLUME_RELATIVE = f'{PREFIX_COMMANDS}volumeRelative'
COMMAND_GET_CAMERA_STREAM = f'{PREFIX_COMMANDS}GetCameraStream'
COMMAND_TOGGLES = f'{PREFIX_COMMANDS}SetToggles'
COMMAND_TIMER_START = f'{PREFIX_COMMANDS}TimerStart'
COMMAND_TIMER_CANCEL = f'{PREFIX_COMMANDS}TimerCancel'
COMMAND_CHARGE = f'{PREFIX_COMMANDS}Charge'
COMMAND_SET_HUMIDITY = f'{PREFIX_COMMANDS}SetHumidity'
COMMAND_SET_HUMIDITY_RELATIVE = f'{PREFIX_COMMANDS}HumidityRelative'

TRAITS = []

CREDITS = (configuration['Domoticz']['username'], configuration['Domoticz']['password'])


def register_trait(trait):
    """Decorate a function to register a trait."""
    TRAITS.append(trait)
    return trait


def _google_temp_unit(units):
    """Return Google temperature unit."""
    if units:
        return "F"
    return "C"


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
            DOMAINS['ac_unit'],
            DOMAINS['bathtub'],
            DOMAINS['coffeemaker'],
            DOMAINS['color'],
            DOMAINS['cooktop'],
            DOMAINS['dishwasher'],
            DOMAINS['doorbell'],
            DOMAINS['dryer'],
            DOMAINS['fan'],
            DOMAINS['group'],
            DOMAINS['heater'],
            DOMAINS['kettle'],
            DOMAINS['light'],
            DOMAINS['media'],
            DOMAINS['microwave'],
            DOMAINS['mower'],
            DOMAINS['outlet'],
            DOMAINS['oven'],
            DOMAINS['push'],
            DOMAINS['sensor'],
            DOMAINS['smokedetector'],
            DOMAINS['speaker'],
            DOMAINS['switch'],
            #DOMAINS['vacuum'],
            DOMAINS['washer'],
            DOMAINS['waterheater'],
        )

    def sync_attributes(self):
        """Return OnOff attributes for a sync request."""
        domain = self.state.domain
        response = {}
        if domain in [DOMAINS['sensor'], DOMAINS['smokedetector'], DOMAINS['doorbell']]:
            response['queryOnlyOnOff'] = True
        
        return response

    def query_attributes(self):
        """Return OnOff query attributes."""
        domain = self.state.domain

        response = {}
        if domain == DOMAINS['push']:
            response['on'] = False
        else:
            response['on'] = self.state.state != 'Off'
        if domain != DOMAINS['group'] and self.state.battery <= configuration['Low_battery_limit']:
            response['exceptionCode'] = 'lowBattery'

        return response

    def execute(self, command, params):
        """Execute an OnOff command."""
        domain = self.state.domain
        protected = self.state.protected

        if domain not in [DOMAINS['sensor'], DOMAINS['smokedetector']]:
            if domain == DOMAINS['group']:
                url = DOMOTICZ_URL + '/json.htm?type=command&param=switchscene&idx=' + self.state.id + '&switchcmd=' + (
                    'On' if params['on'] else 'Off')
            else:
                url = DOMOTICZ_URL + '/json.htm?type=command&param=switchlight&idx=' + self.state.id + '&switchcmd=' + (
                    'On' if params['on'] else 'Off')

            if protected:
                url = url + '&passcode=' + configuration['Domoticz']['switchProtectionPass']

            r = requests.get(url, auth=CREDITS)
            if protected:
                status = r.json()
                err = status.get('status')
                if err == 'ERROR':
                    raise SmartHomeError(ERR_WRONG_PIN,
                                         'Unable to execute {} for {} check your settings'.format(command,
                                                                                                  self.state.entity_id))


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
        return domain in DOMAINS['scene']

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
            url = url + '&passcode=' + configuration['Domoticz']['switchProtectionPass']

        r = requests.get(url, auth=CREDITS)
        if protected:
            status = r.json()
            err = status.get('status')
            if err == 'ERROR':
                raise SmartHomeError(ERR_WRONG_PIN,
                                     'Unable to execute {} for {} check your settings'.format(command,
                                                                                              self.state.entity_id))


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
        if domain in (DOMAINS['light'], DOMAINS['color'], DOMAINS['outlet']):
            return features & ATTRS_BRIGHTNESS

        return False

    def sync_attributes(self):
        """Return brightness attributes for a sync request."""
        return {}

    def query_attributes(self):
        """Return brightness query attributes."""
        domain = self.state.domain
        response = {}

        brightness = self.state.level
        response['brightness'] = int(brightness * 100 / self.state.maxdimlevel)
        
        if self.state.battery <= configuration['Low_battery_limit']:
            response['exceptionCode'] = 'lowBattery'

        return response

    def can_execute(self, command, params):
        """Test if command can be executed."""
        protected = self.state.protected
        if protected:
            raise SmartHomeError('notSupported',
                                 'Unable to execute {} for {} check your settings'.format(command,
                                                                                          self.state.entity_id))
        return command in self.commands

    def execute(self, command, params):
        """Execute a brightness command."""
        protected = self.state.protected

        url = DOMOTICZ_URL + '/json.htm?type=command&param=switchlight&idx=' + self.state.id + '&switchcmd=Set%20Level&level=' + str(
            int(params['brightness'] * self.state.maxdimlevel / 100))

        if protected:
            url = url + '&passcode=' + configuration['Domoticz']['switchProtectionPass']

        r = requests.get(url, auth=CREDITS)
        if protected:
            status = r.json()
            err = status.get('status')
            if err == 'ERROR':
                raise SmartHomeError(ERR_WRONG_PIN,
                                     'Unable to execute {} for {} check your settings'.format(command,
                                                                                              self.state.entity_id))


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
        return domain in (
                DOMAINS['blinds'],
                DOMAINS['door'],
                DOMAINS['window'],
                DOMAINS['gate'],
                DOMAINS['garage'],
                DOMAINS['valve']
            )

    def sync_attributes(self):
        """Return OpenClose attributes for a sync request."""
        features = self.state.attributes
        response = {}
        
        if features & ATTRS_PERCENTAGE != True:
            response['discreteOnlyOpenClose'] = True
            
        return response

    def query_attributes(self):
        """Return OpenClose query attributes."""
        features = self.state.attributes
        domain = self.state.domain
        response = {}

        if features & ATTRS_PERCENTAGE:
            response['openPercent'] = self.state.level
        else:
            if self.state.state in ['Open', 'Off']:
                response['openPercent'] = 100
            else:
                response['openPercent'] = 0

        if self.state.battery <= configuration['Low_battery_limit']:
            response['exceptionCode'] = 'lowBattery'

        return response

    def execute(self, command, params):
        """Execute a OpenClose command."""
        features = self.state.attributes
        protected = self.state.protected
        state = self.state.state
        domain = self.state.domain
        
        if features & ATTRS_PERCENTAGE:
            if domain == DOMAINS['blinds']:
              url = DOMOTICZ_URL + '/json.htm?type=command&param=switchlight&idx=' + self.state.id + '&switchcmd=Set%20Level&level=' + str(
                params['openPercent'])
        else:
            p = params.get('openPercent', 50)

            url = DOMOTICZ_URL + '/json.htm?type=command&param=switchlight&idx=' + self.state.id + '&switchcmd='
            
        if p == 100 and state in ['Closed', 'Stopped', 'On']:
          # open
          url += 'Open'
        elif p == 0 and state in ['Open', 'Stopped', 'Off']:
          # close
          url += 'Close'
        else:
          raise SmartHomeError(ERR_ALREADY_IN_STATE,
                               'Unable to execute {} for {}. Already in state '.format(command,
                                                                                       self.state.entity_id))

        if protected:
            url = url + '&passcode=' + configuration['Domoticz']['switchProtectionPass']

        r = requests.get(url, auth=CREDITS)
        if protected:
            status = r.json()
            err = status.get('status')
            if err == 'ERROR':
                raise SmartHomeError(ERR_WRONG_PIN,
                                     'Unable to execute {} for {} check your settings'.format(command,
                                                                                              self.state.entity_id))

@register_trait
class StartStopTrait(_Trait):
    """Trait to offer StartStop functionality.
    https://developers.google.com/actions/smarthome/traits/startstop
    """

    name = TRAIT_STARTSTOP
    commands = [COMMAND_STARTSTOP, COMMAND_PAUSEUNPAUSE]

    @staticmethod
    def supported(domain, features):
        """Test if state is supported."""
        if domain == DOMAINS['blinds']:
            if features & ATTRS_PERCENTAGE:
                return False
            else:
                return domain in DOMAINS['blinds']
        else:
            return domain in DOMAINS['vacuum']

    def sync_attributes(self):
        """Return StartStop attributes for a sync request."""
        return {}

    def query_attributes(self):
        """Return StartStop query attributes."""
        domain = self.state.domain 
        response = {}
        if domain == DOMAINS['blinds']:
            response['isRunning'] = True
        else:
            response['isRunning'] = self.state.state != 'Off'
            
        if self.state.battery <= configuration['Low_battery_limit']:
            response['exceptionCode'] = 'lowBattery'
        
        return response

    def execute(self, command, params):
        """Execute a StartStop command."""
        domain = self.state.domain
        protected = self.state.protected
        
        if command == COMMAND_STARTSTOP: 
            if domain == DOMAINS['blinds']:
                if params['start'] is False:
                    url = DOMOTICZ_URL + '/json.htm?type=command&param=switchlight&idx=' + self.state.id + '&switchcmd=Stop'
            else:
                url = DOMOTICZ_URL + '/json.htm?type=command&param=switchlight&idx=' + self.state.id + '&switchcmd=' + (
                    'On' if params['start'] else 'Off')
 
            if protected:
                url = url + '&passcode=' + configuration['Domoticz']['switchProtectionPass']

            r = requests.get(url, auth=CREDITS)
            if protected:
                status = r.json()
                err = status.get('status')
                if err == 'ERROR':
                    raise SmartHomeError(ERR_WRONG_PIN,
                                         'Unable to execute {} for {} check your settings'.format(command,
                                                                                                  self.state.entity_id))
            

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
        if domain == DOMAINS['thermostat']:
            return features & ATTRS_THERMSTATSETPOINT
        else:
            return domain in [DOMAINS['temperature']]

    def sync_attributes(self):
        """Return temperature point and modes attributes for a sync request."""
        domain = self.state.domain
        units = self.state.tempunit
        minThree = self.state.minThreehold
        maxThree = self.state.maxThreehold
            
        response = {"thermostatTemperatureUnit": _google_temp_unit(units)}
        response["thermostatTemperatureRange"] = { 
            'minThresholdCelsius': minThree,
            'maxThresholdCelsius': maxThree}
        
        if domain in [DOMAINS['temperature']]:
            response["queryOnlyTemperatureSetting"] = True
            response["availableThermostatModes"] = 'heat, cool'

        if domain == DOMAINS['thermostat']:
            if self.state.modes_idx is not None:
                response["availableThermostatModes"] = 'off,heat,cool,auto,eco'
            else:
                response["availableThermostatModes"] = 'heat'

        return response

    def query_attributes(self):
        """Return temperature point and modes query attributes."""
        domain = self.state.domain
        units = self.state.tempunit
        response = {}
        if self.state.battery <= configuration['Low_battery_limit']:
            response['exceptionCode'] = 'lowBattery'

        if domain in [DOMAINS['temperature']]:           
            current_temp = float(self.state.temp)
            if current_temp is not None:
                if round(tempConvert(current_temp, _google_temp_unit(units)),1) <= 3:
                    response['thermostatMode'] = 'cool'
                else:
                    response['thermostatMode'] = 'heat'
                response['thermostatTemperatureAmbient'] = round(tempConvert(current_temp, _google_temp_unit(units)), 1)
                response['thermostatTemperatureSetpoint'] = round(tempConvert(current_temp, _google_temp_unit(units)), 1)
            # current_humidity = self.state.humidity
            # if current_humidity is not None:
                # response['thermostatHumidityAmbient'] = current_humidity

        if domain == DOMAINS['thermostat']:
            if self.state.modes_idx is not None:
                levelName = base64.b64decode(self.state.selectorLevelName).decode('UTF-8').split("|")
                level = self.state.level
                index = int(level / 10)
                response['thermostatMode'] = levelName[index].lower()
            else:
                response['thermostatMode'] = 'heat'
            current_temp = float(self.state.state)
            if current_temp is not None:
                response['thermostatTemperatureAmbient'] = round(tempConvert(current_temp, _google_temp_unit(units)), 1)
            setpoint = float(self.state.setpoint)
            if setpoint is not None:
                response['thermostatTemperatureSetpoint'] = round(tempConvert(setpoint, _google_temp_unit(units)), 1)
            current_humidity = self.state.humidity
            if current_humidity is not None:
                response['thermostatHumidityAmbient'] = current_humidity
            

        return response

    def execute(self, command, params):
        """Execute a temperature point or mode command."""
        # All sent in temperatures are always in Celsius

        if command == COMMAND_THERMOSTAT_SET_MODE:
            if self.state.modes_idx is not None:
                levels = base64.b64decode(self.state.selectorLevelName).decode('UTF-8').split("|")
                levelName = [x.lower() for x in levels]

                if params['thermostatMode'] in levelName:
                    level = str(levelName.index(params['thermostatMode']) * 10)
                url = DOMOTICZ_URL + '/json.htm?type=command&param=switchlight&idx=' + self.state.modes_idx + '&switchcmd=Set%20Level&level=' + level
                r = requests.get(url, auth=CREDITS)
            else:
                raise SmartHomeError('notSupported',
                                     'Unable to execute {} for {} check your settings'.format(command, self.state.entity_id))
                
        if command == COMMAND_THERMOSTAT_TEMPERATURE_SETPOINT:
            if self.state.modes_idx is not None:
                levelName = base64.b64decode(self.state.selectorLevelName).decode('UTF-8').split("|")
                level = self.state.level
                index = int(level / 10)
                if levelName[index].lower() == 'off':
                    raise SmartHomeError('inOffMode',
                                     'Unable to execute {} for {} check your settings'.format(command, self.state.entity_id))
                elif levelName[index].lower() == 'auto':
                    raise SmartHomeError('inAutoMode',
                                     'Unable to execute {} for {} check your settings'.format(command, self.state.entity_id))
                elif levelName[index].lower() == 'eco':
                    raise SmartHomeError('inEcoMode',
                                     'Unable to execute {} for {} check your settings'.format(command, self.state.entity_id))                   

            url = DOMOTICZ_URL + '/json.htm?type=command&param=setsetpoint&idx=' + self.state.id + '&setpoint=' + str(
                    params['thermostatTemperatureSetpoint'])

            r = requests.get(url, auth=CREDITS)


@register_trait
class TemperatureControlTrait(_Trait):
    """Trait to offer handling temperature point functionality.

    https://developers.google.com/actions/smarthome/traits/temperaturecontrol
    """

    name = TRAIT_TEMPERATURE_CONTROL
    commands = [
        COMMAND_SET_TEMPERATURE,
    ]
    
    
    @staticmethod
    def supported(domain, features):
        """Test if state is supported."""
        return domain in [DOMAINS['heater'], DOMAINS['kettle'], DOMAINS['waterheater'], DOMAINS['oven']]

    def sync_attributes(self):
        """Return temperature point attributes for a sync request."""
        domain = self.state.domain
        units = self.state.tempunit
        minThree = -100
        maxThree = 100
        response = {}
        response = {"temperatureUnitForUX": _google_temp_unit(units)}
        response["temperatureRange"] = {
                'minThresholdCelsius': minThree,
                'maxThresholdCelsius': maxThree}
            
        if self.state.merge_thermo_idx is not None:
            response = {"temperatureStepCelsius": 1}
            
        return response

    def query_attributes(self):
        """Return temperature point query attributes."""
        domain = self.state.domain
        units = self.state.tempunit
        response = {}
                
        if self.state.merge_thermo_idx is not None:
            if self.state.battery <= configuration['Low_battery_limit']:
                response['exceptionCode'] = 'lowBattery'

            current_temp = float(self.state.temp)
            if current_temp is not None:
                response['temperatureAmbientCelsius'] = current_temp
            setpoint = float(self.state.setpoint)
            if setpoint is not None:
                response['temperatureSetpointCelsius'] = setpoint

        return response

    def execute(self, command, params):
        """Execute a temperature point command."""
        # All sent in temperatures are always in Celsius
        if self.state.merge_thermo_idx is not None:
            if command == COMMAND_SET_TEMPERATURE:               

                url = DOMOTICZ_URL + '/json.htm?type=command&param=setsetpoint&idx=' + self.state.merge_thermo_idx + '&setpoint=' + str(
                        params['temperature'])

                r = requests.get(url, auth=CREDITS)
            
            
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
        return domain in (DOMAINS['lock'],
                          DOMAINS['lockinv'])

    def sync_attributes(self):
        """Return LockUnlock attributes for a sync request."""
        return {}

    def query_attributes(self):
        """Return LockUnlock query attributes."""
        response = {}
        if self.state.battery <= configuration['Low_battery_limit']:
            response['exceptionCode'] = 'lowBattery'

        response['isLocked'] = self.state.state == 'Locked'

        return response

    def execute(self, command, params):
        """Execute an LockUnlock command."""
        domain = self.state.domain
        state = self.state.state
        protected = self.state.protected

        if domain == DOMAINS['lock']:
            if params['lock'] == True and state == 'Unlocked':
                url = DOMOTICZ_URL + '/json.htm?type=command&param=switchlight&idx=' + self.state.id + '&switchcmd=On'
            elif params['lock'] == False and state == 'Locked':
                url = DOMOTICZ_URL + '/json.htm?type=command&param=switchlight&idx=' + self.state.id + '&switchcmd=Off'
            else:
                raise SmartHomeError(ERR_ALREADY_IN_STATE,
                                     'Unable to execute {} for {}. Already in state '.format(command,
                                                                                             self.state.entity_id))
        else:
            if params['lock'] == True and state == 'Unlocked':
                url = DOMOTICZ_URL + '/json.htm?type=command&param=switchlight&idx=' + self.state.id + '&switchcmd=Off'
            elif params['lock'] == False and state == 'Locked':
                url = DOMOTICZ_URL + '/json.htm?type=command&param=switchlight&idx=' + self.state.id + '&switchcmd=On'
            else:
                raise SmartHomeError(ERR_ALREADY_IN_STATE,
                                     'Unable to execute {} for {}. Already in state '.format(command,
                                                                                             self.state.entity_id))

        if protected:
            url = url + '&passcode=' + configuration['Domoticz']['switchProtectionPass']

        r = requests.get(url, auth=CREDITS)
        if protected:
            status = r.json()
            err = status.get('status')
            if err == 'ERROR':
                raise SmartHomeError(ERR_WRONG_PIN,
                                     'Unable to execute {} for {} check your settings'.format(command,
                                                                                              self.state.entity_id))


@register_trait
class ColorSettingTrait(_Trait):
    """Trait to offer color setting functionality.
    https://developers.google.com/actions/smarthome/traits/colorsetting
    """

    name = TRAIT_COLOR_SETTING
    commands = [
        COMMAND_COLOR_ABSOLUTE
    ]
    kelvinTempMin = 1700
    kelvinTempMax = 6500

    @staticmethod
    def supported(domain, features):
        """Test if state is supported."""
        if domain == DOMAINS['color']:
            return (features & ATTRS_COLOR or
                    features & ATTRS_COLOR_TEMP)

        return False

    def sync_attributes(self):
        """Return color setting attributes for a sync request."""
        # Other colorModel is hsv
        return {'colorModel': 'rgb',
                'colorTemperatureRange': {
                    'temperatureMinK': self.kelvinTempMin,
                    'temperatureMaxK': self.kelvinTempMax}
            }

    def query_attributes(self):
        """Return color setting query attributes."""
        response = {}
        try:
            color_rgb = json.loads(self.state.color)
            if color_rgb is not None:
                # Convert RGB to decimal
                color_decimal = color_rgb["r"] * 65536 + color_rgb["g"] * 256 + color_rgb["b"]

                response['color'] = {'spectrumRGB': color_decimal}

                if color_rgb["m"] == 2:
                    colorTemp = (color_rgb["t"] * (255 / 100)) * 10
                    response['color'] = {'temperatureK': round(colorTemp)}
        except ValueError:
            response = {}

        return response

    def execute(self, command, params):
        """Execute a color setting command."""
        if "temperature" in params["color"]:
            tempRange = self.kelvinTempMax - self.kelvinTempMin
            kelvinTemp = params['color']['temperature']
            setTemp = 100 - (((kelvinTemp - self.kelvinTempMin) / tempRange) * 100)

            url = DOMOTICZ_URL + '/json.htm?type=command&param=setkelvinlevel&idx=' + self.state.id + '&kelvin=' + str(
                round(setTemp))

        elif "spectrumRGB" in params["color"]:
            # Convert decimal to hex
            setcolor = params['color']
            color_hex = hex(setcolor['spectrumRGB'])[2:]
            lost_zeros = 6 - len(color_hex)
            color_hex_str = ""
            for x in range(lost_zeros):
                color_hex_str += "0"
            color_hex_str += str(color_hex)

            url = DOMOTICZ_URL + '/json.htm?type=command&param=setcolbrightnessvalue&idx=' + self.state.id + '&hex=' + color_hex_str

        r = requests.get(url, auth=CREDITS)


@register_trait
class ArmDisarmTrait(_Trait):
    """Trait to offer basic on and off functionality.
    https://developers.google.com/actions/smarthome/traits/armdisarm
    """

    name = TRAIT_ARM_DISARM
    commands = [
        COMMAND_ARM_DISARM
    ]

    @staticmethod
    def supported(domain, features):
        """Test if state is supported."""
        return domain in DOMAINS['security']

    def sync_attributes(self):
        """Return ArmDisarm attributes for a sync request."""
        Armhome = {}
        if 'Armhome' in configuration:
            Armhome = configuration['Armhome']

        Armaway = {}
        if 'Armaway' in configuration:
            Armaway = configuration['Armaway']
        return {
            "availableArmLevels": {
                "levels": [{
                    "level_name": "Arm Home",
                    "level_values": [{
                        "level_synonym": ["armed home", "low security", "home and guarding", "level 1", "home", "SL1"],
                        "lang": "en"
                    }, Armhome
                    ]
                }, {
                    "level_name": "Arm Away",
                    "level_values": [{
                        "level_synonym": ["armed away", "high security", "away and guarding", "level 2", "away", "SL2"],
                        "lang": "en"
                    }, Armaway
                    ]
                }],
                "ordered": True
            }
        }

    def query_attributes(self):
        """Return ArmDisarm query attributes."""
        response = {}
        state = self.state.state
        delay = self.state.secondelay

        response["isArmed"] = state != "Normal"
        response['exitAllowance'] = int(delay)

        if response["isArmed"]:
            response["currentArmLevel"] = state

        return response

    def execute(self, command, params):
        """Execute an ArmDisarm command."""
        state = self.state.state
        seccode = self.state.seccode

        if params["arm"]:
            if params["armLevel"] == "Arm Home":
                if state == "Arm Home":
                    raise SmartHomeError(ERR_ALREADY_IN_STATE,
                                         'Unable to execute {} for {} '.format(command, self.state.entity_id))
                else:
                    self.state.state = "Arm Home"
                    url = DOMOTICZ_URL + "/json.htm?type=command&param=setsecstatus&secstatus=1&seccode=" + seccode
            if params["armLevel"] == "Arm Away":
                if state == "Arm Away":
                    raise SmartHomeError(ERR_ALREADY_IN_STATE,
                                         'Unable to execute {} for {} '.format(command, self.state.entity_id))
                else:
                    self.state.state = "Arm Away"
                    url = DOMOTICZ_URL + "/json.htm?type=command&param=setsecstatus&secstatus=2&seccode=" + seccode
        else:
            if state == "Normal":
                raise SmartHomeError(ERR_ALREADY_IN_STATE,
                                     'Unable to execute {} for {} '.format(command, self.state.entity_id))
            else:
                self.state.state = "Normal"
                url = DOMOTICZ_URL + "/json.htm?type=command&param=setsecstatus&secstatus=0&seccode=" + seccode

        r = requests.get(url, auth=CREDITS)


@register_trait
class VolumeTrait(_Trait):
    """Trait to control volume of a device.
    https://developers.google.com/actions/smarthome/traits/volume
    """

    name = TRAIT_VOLUME
    commands = [
        COMMAND_SET_VOLUME,
        COMMAND_VOLUME_RELATIVE
    ]

    @staticmethod
    def supported(domain, features):
        """Test if state is supported."""
        return domain in DOMAINS['speaker']

    def sync_attributes(self):
        """Return volume attributes for a sync request."""
        return {}

    def query_attributes(self):
        """Return volume query attributes."""
        response = {}
        level = self.state.level

        if level is not None:
            response['currentVolume'] = int(level * 100 / self.state.maxdimlevel)

        return response

    def _execute_set_volume(self, params):
        level = params['volumeLevel']

        url = DOMOTICZ_URL + '/json.htm?type=command&param=switchlight&idx=' + self.state.id + '&switchcmd=Set%20Level&level=' + str(
            int(level * self.state.maxdimlevel / 100))
        r = requests.get(url, auth=CREDITS)

    def _execute_volume_relative(self, params):
        # This could also support up/down commands using relativeSteps
        relative = params['volumeRelativeLevel']
        current = level = self.state.level

        url = DOMOTICZ_URL + '/json.htm?type=command&param=switchlight&idx=' + self.state.id + '&switchcmd=Set%20Level&level=' + str(
            int(current + relative * self.state.maxdimlevel / 100))
        r = requests.get(url, auth=CREDITS)

    def execute(self, command, params):
        """Execute a volume command."""
        if command == COMMAND_SET_VOLUME:
            self._execute_set_volume(params)
        elif command == COMMAND_VOLUME_RELATIVE:
            self._execute_volume_relative(params)
        else:
            raise SmartHomeError(ERR_NOT_SUPPORTED,
                                 'Unable to execute {} for {} '.format(command, self.state.entity_id))                         


@register_trait
class CameraStreamTrait(_Trait):
    """Trait to stream from cameras.
    https://developers.google.com/actions/smarthome/traits/camerastream
    """

    name = TRAIT_CAMERA_STREAM
    commands = [
        COMMAND_GET_CAMERA_STREAM
    ]

    stream_info = None

    @staticmethod
    def supported(domain, features):
        """Test if state is supported."""
        if configuration['Camera_Stream']['Enabled']:
            return domain in [DOMAINS['camera'], DOMAINS['doorbell']]
            
        return False

    def sync_attributes(self):
        """Return stream attributes for a sync request."""
        return {
            'cameraStreamSupportedProtocols': ['hls'],
            'cameraStreamNeedAuthToken': False,
            'cameraStreamNeedDrmEncryption': False,
        }

    def query_attributes(self):
        """Return camera stream attributes."""
        for camUrl, idx in enumerate(configuration['Camera_Stream']['Cameras']['Idx']):
            if idx in self.state.id:
                url = configuration['Camera_Stream']['Cameras']['Camera_URL'][camUrl]
        self.stream_info = {'cameraStreamAccessUrl': url}
        return self.stream_info or {}

    def execute(self, command, params):
        """Execute a get camera stream command."""
        return


@register_trait
class TooglesTrait(_Trait):
    """Trait to set toggles.
    https://developers.google.com/actions/smarthome/traits/modes
    """

    name = TRAIT_TOGGLES
    commands = [COMMAND_TOGGLES]

    @staticmethod
    def supported(domain, features):
        """Test if state is supported."""
        if domain == DOMAINS['vacuum']:
            return features & ATTRS_VACUUM_MODES
        else:
            return domain in DOMAINS['selector']

    def sync_attributes(self):
        """Return mode attributes for a sync request."""
        levelName = base64.b64decode(self.state.selectorLevelName).decode('UTF-8').split("|")
        levels = []

        if levelName:
            for s in levelName:
                levels.append(
                    {
                        "name": s,
                        "name_values": [
                            {"name_synonym": [s],
                             "lang": "en"},
                            {"name_synonym": [s],
                             "lang": self.state.language},
                        ],
                    }
                )

        return {"availableToggles": levels}

    def query_attributes(self):
        """Return current modes."""
        levelName = base64.b64decode(self.state.selectorLevelName).decode('UTF-8').split("|")
        level = self.state.level
        index = int(level / 10)
        response = {}
        toggle_settings = {
            levelName[index]: self.state.state != 'Off'}

        if toggle_settings:
            response["on"] = self.state.state != 'Off'
            response["currentToggleSettings"] = toggle_settings

        return response

    def execute(self, command, params):
        """Execute an SetModes command."""
        levelName = base64.b64decode(self.state.selectorLevelName).decode('UTF-8').split("|")
        protected = self.state.protected
        for key in params['updateToggleSettings']:
            if key in levelName:
                level = str(levelName.index(key) * 10)

        url = DOMOTICZ_URL + '/json.htm?type=command&param=switchlight&idx=' + self.state.id + '&switchcmd=Set%20Level&level=' + level

        if protected:
            url = url + '&passcode=' + configuration['Domoticz']['switchProtectionPass']

        r = requests.get(url, auth=CREDITS)

        if protected:
            status = r.json()
            err = status.get('status')
            if err == 'ERROR':
                raise SmartHomeError(ERR_WRONG_PIN,
                                     'Unable to execute {} for {} check your settings'.format(command,
                                                                                              self.state.entity_id))

@register_trait
class Timer(_Trait):
    """Trait to offer StartStop functionality.
    https://developers.google.com/actions/smarthome/traits/timer
    """

    name = TRAIT_TIMER
    commands = [COMMAND_TIMER_START,
                COMMAND_TIMER_CANCEL
                ]

    @staticmethod
    def supported(domain, features):
        """Test if state is supported."""
        return domain in [DOMAINS['light'],
                          DOMAINS['color'],
                          DOMAINS['switch'],
                          DOMAINS['heater'],
                          DOMAINS['kettle'],
                          DOMAINS['fan'],
                          ]

    def sync_attributes(self):
        """Return Timer attributes for a sync request."""
        return {"maxTimerLimitSec": 7200,
                "commandOnlyTimer": True}

    def query_attributes(self):
        """Return Timer query attributes."""    
        response = {}
        # response['timerRemainingSec'] = -1
        
        return response

    def execute(self, command, params):
        """Execute a Timer command."""
        
        if command == COMMAND_TIMER_START:
            logger.info('Make sure you have dzVents Dzga_Timer script installed and active')
            url = DOMOTICZ_URL + '/json.htm?type=command&param=customevent&event=TIMER&data={"idx":' + self.state.id + ',"time":' + str(params['timerTimeSec']) + ',"on":true}'

            r = requests.get(url, auth=CREDITS)

    
        if command == COMMAND_TIMER_CANCEL:
            url = DOMOTICZ_URL + '/json.htm?type=command&param=customevent&event=TIMER&data={"idx":' + self.state.id + ',"cancel":true}'

            r = requests.get(url, auth=CREDITS)
            
@register_trait
class EnergyStorageTrait(_Trait):
    """Trait to offer EnergyStorge functionality.
    https://developers.google.com/actions/smarthome/traits/energystorage
    """

    name = TRAIT_ENERGY
    commands = [COMMAND_CHARGE]

    @staticmethod
    def supported(domain, features):
        """Test if state is supported."""
        return domain in (
                DOMAINS['vacuum'],
                DOMAINS['blinds'],
                DOMAINS['smokedetector'],
                DOMAINS['sensor'],
                DOMAINS['mower'],
                DOMAINS['thermostat'],
                DOMAINS['temperature']
                )
  
    def sync_attributes(self):
        """Return EnergyStorge attributes for a sync request."""
        battery = self.state.battery
        response = {}
        if battery is not None or battery != 255:
            response['queryOnlyEnergyStorage'] = True
            response['isRechargeable'] = False
        
        return response

    def query_attributes(self):
        """Return EnergyStorge query attributes."""
        battery = self.state.battery
        response = {}
        if battery == 255:
            return {}
        if battery == 100:
            descriptive_capacity_remaining = "FULL"
        elif 75 <= battery < 100:
            descriptive_capacity_remaining = "HIGH"
        elif 50 <= battery < 75:
            descriptive_capacity_remaining = "MEDIUM"
        elif 25 <= battery < 50:
            descriptive_capacity_remaining = "LOW"
        elif 0 <= battery < 25:
            descriptive_capacity_remaining = "CRITICALLY_LOW"
        if battery is not None:
            response['descriptiveCapacityRemaining'] = descriptive_capacity_remaining
            response['capacityRemaining'] = [{
                'unit': 'PERCENTAGE',
                'rawValue': battery
              }]
           
        return response

    def execute(self, command, params):
        """Execute a EnergyStorge command."""
        # domain = self.state.domain
        # protected = self.state.protected
        
        # if domain in (DOMAINS['vacuum'], DOMAINS['mower']):
            # url = DOMOTICZ_URL + '/json.htm?type=command&param=switchlight&idx=' + self.state.id + '&switchcmd=' + (
                # 'On' if params['charge'] else 'Off')

            # if protected:
                # url = url + '&passcode=' + configuration['Domoticz']['switchProtectionPass']

            # r = requests.get(url, auth=CREDITS)
            # if protected:
                # status = r.json()
                # err = status.get('status')
                # if err == 'ERROR':
                    # raise SmartHomeError(ERR_WRONG_PIN,
                                         # 'Unable to execute {} for {} check your settings'.format(command,
                                                                                                  # self.state.entity_id))

@register_trait
class HumiditySettingTrait(_Trait):
    """Trait to offer scene functionality.
    https://developers.google.com/actions/smarthome/traits/scene
    """

    name = TRAIT_HUMIDITY
    commands = [
        COMMAND_SET_HUMIDITY,
        COMMAND_SET_HUMIDITY_RELATIVE
    ]

    @staticmethod
    def supported(domain, features):
        """Test if state is supported."""
        if domain == DOMAINS['temperature']:
            return features & ATTRS_THERMSTATSETPOINT

    def sync_attributes(self):
        """Return humidity attributes for a sync request."""
        response = {}
        response["humiditySetpointRange"] = {
            "minPercent": 25,
            "maxPercent": 75
            }
        response['queryOnlyHumiditySetting'] = True
        
        return response

    def query_attributes(self):
        """Return humidity query attributes."""
        current_humidity = self.state.humidity
        response = {}
        response['humidityAmbientPercent'] = current_humidity
        #response['humiditySetpointPercent'] = current_humidity
        
        return response

    def execute(self, command, params):
        """Execute a humidity command."""
        # domain = self.state.domain
        # protected = self.state.protected
        
        # if domain == DOMAINS['humidity']:
            # url = DOMOTICZ_URL + '/json.htm?type=command&param=setsetpoint&idx=' + self.state.id + '&setpoint=' + str(params['humidity'])

        # if protected:
            # url = url + '&passcode=' + configuration['Domoticz']['switchProtectionPass']

        # r = requests.get(url, auth=CREDITS)
        # if protected:
            # status = r.json()
            # err = status.get('status')
            # if err == 'ERROR':
                # raise SmartHomeError(ERR_WRONG_PIN,
                                     # 'Unable to execute {} for {} check your settings'.format(command,
                                                                                              # self.state.entity_id))
                                                                                              
@register_trait
class SensorStateTrait(_Trait):
    """Trait to get sensor state.
    https://developers.google.com/actions/smarthome/traits/sensorstate
    """

    name = TRAIT_SENSOR_STATE
    commands = []

    @staticmethod
    def supported(domain, features):
        """Test if state is supported."""
        return domain in [DOMAINS['smokedetector']]

    def sync_attributes(self):
        """Return attributes for a sync request."""
        domain = self.state.domain
        if domain == DOMAIN['smokedetector']:
            return {
                "sensorStatesSupported": [
                    {
                      "name": "SmokeLevel",
                      "descriptiveCapabilities": {
                        "availableStates": [
                          "smoke detected",
                          "no smoke detected"
                        ]
                      }
                    }
                  ]
                }

    def query_attributes(self):
        """Return the attributes of this trait for this entity."""
        domain = self.state.domain
        if self.state.state is not None:
            return {
                "currentSensorStateData": [
                    {
                        "name": "SmokeLevel",
                        "currentSensorState": "smoke detected",
                        }
                ]
            }

# @register_trait
# class FanSpeedTrait(_Trait):
    # """Trait to control speed of Fan.
    # https://developers.google.com/actions/smarthome/traits/fanspeed
    # """

    # name = TRAIT_FANSPEED
    # commands = [COMMAND_FANSPEED]

    # speed_synonyms = {
        # 'off': ["stop", "off"],
        # 'speed_low': ["slow", "low", "slowest", "lowest"],
        # 'speed_medium': ["medium", "mid", "middle"],
        # 'speed_high': ["high", "max", "fast", "highest", "fastest", "maximum"],
    # }
    
    # modes = ['off', 'speed_low', 'speed_medium','speed_high']

    # @staticmethod
    # def supported(domain, features):
        # """Test if state is supported."""
        # if domain in [
            # DOMAINS['fan']
            # ]:
            # return features & ATTRS_FANSPEED

        # return False

    # def sync_attributes(self):
        # """Return speed point and modes attributes for a sync request."""
        # modes = self.modes
        # speeds = []
        # for mode in modes:
            # if mode not in self.speed_synonyms:
                # continue
            # speed = {
                # "speed_name": mode,
                # "speed_values": [
                    # {"speed_synonym": self.speed_synonyms.get(mode), "lang": "en"}
                # ],
            # }
            # speeds.append(speed)

        # return {
            # "availableFanSpeeds": {"speeds": speeds, "ordered": True},
        # }

    # def query_attributes(self):
        # """Return speed point and modes query attributes."""
        # response = {}

        # speed = self.state.state
        # if speed is not None:
            # response["on"] = speed != 'Off'
            # response["online"] = True
            # response["currentFanSpeedSetting"] = speed.lower()

        # return response

    # def execute(self, command, params):
        # """Execute an SetFanSpeed command."""
        # modes = self.modes
        # protected = self.state.protected
        # for key in params['fanSpeed']:
            # if key in modes:
                # level = str(modes.index(key) * 10)

        # url = DOMOTICZ_URL + '/json.htm?type=command&param=switchlight&idx=' + self.state.id + '&switchcmd=Set%20Level&level=' + level

        # if protected:
            # url = url + '&passcode=' + configuration['Domoticz']['switchProtectionPass']

        # r = requests.get(url, auth=CREDITS)

        # if protected:
            # status = r.json()
            # err = status.get('status')
            # if err == 'ERROR':
                # raise SmartHomeError(ERR_WRONG_PIN,
                                     # 'Unable to execute {} for {} check your settings'.format(command,
                                                                                              # self.state.entity_id))
