"""Helper classes for Google Assistant integration."""

import os
import yaml
from pyngrok import ngrok
import logging

FILE_PATH = os.path.abspath(__file__)
FILE_DIR = os.path.split(FILE_PATH)[0]
CONFIGFILE = 'config.yaml'

try:
    print ('Loading configuration...')
    with open(os.path.join(FILE_DIR,CONFIGFILE), 'r') as conf:
        configuration = yaml.safe_load(conf)      
except yaml.YAMLError as exc:
    print('ERROR: Please check config.yaml')
except FileNotFoundError as err:
    print('No config.yaml found...')
    print('Loading default configuration...')
    content = readFile('default_config')
    print('Create config.yaml...')
    saveFile(CONFIGFILE, content)
    with open(os.path.join(FILE_DIR,CONFIGFILE), 'r') as conf:
        configuration = yaml.safe_load(conf)
        
if 'loglevel' in configuration:
    if (configuration['loglevel']).lower() == 'debug':
        loglevel = logging.DEBUG
    elif (configuration['loglevel']).lower() == 'error':
        loglevel = logging.ERROR
    else:
        loglevel = logging.INFO
else:
        loglevel = logging.INFO

# Create a custom logger
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)
# Log in terminal
ch = logging.StreamHandler()
ch.setLevel(loglevel)
logger.addHandler(ch)
# Log to file
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s', "%Y-%m-%d %H:%M:%S")
fh = logging.FileHandler(os.path.join(FILE_DIR, 'dzga.log'), mode='w')
fh.setLevel(loglevel)
fh.setFormatter(formatter)
logger.addHandler(fh)

class SmartHomeError(Exception):
    """Google Assistant Smart Home errors.
    https://developers.google.com/actions/smarthome/create-app#error_responses
    """
    def __init__(self, code, msg):
        """Log error code."""
        super().__init__(msg)
        self.code = code 

class SmartHomeErrorNoChallenge(Exception):
    def __init__(self, code, desc, msg):
        """Log error code."""
        super().__init__(msg)
        self.code = code 
        self.desc = desc
 
class AogState:
    def __init__(self):
        self.state = ''
        self.domain = ''
        self.attributes = 0
        self.name = ''
        self.entity_id = ''
        self.id = ''
        self.nicknames = None
        self.room = None
        self.level = 0
        self.temp = 0
        self.humidity = 0
        self.setpoint = ''
        self.color = ''
        self.protected = None
        self.maxdimlevel = 0
        self.seccode = ''
        self.tempunit = None
        self.battery = 0
        self.ack = False

def uptime():
    """Get systems uptime"""
    try:
        f = open( "/proc/uptime" )
        contents = f.read().split()
        f.close()
    except:
        return "Cannot open uptime file: /proc/uptime"

    total_seconds = float(contents[0])

    # Helper vars:
    MINUTE  = 60
    HOUR    = MINUTE * 60
    DAY     = HOUR * 24

    # Get the days, hours, etc:
    days    = int( total_seconds / DAY )
    hours   = int( ( total_seconds % DAY ) / HOUR )
    minutes = int( ( total_seconds % HOUR ) / MINUTE )
    seconds = int( total_seconds % MINUTE )

    # Build up the pretty string (like this: "N days, N hours, N minutes, N seconds")
    string = ""
    if days > 0:
        string += str(days) + " " + (days == 1 and "day" or "days" ) + ", "
    if len(string) > 0 or hours > 0:
        string += str(hours) + " " + (hours == 1 and "hour" or "hours" ) + ", "
    if len(string) > 0 or minutes > 0:
        string += str(minutes) + " " + (minutes == 1 and "minute" or "minutes" ) + ", "
        string += str(seconds) + " " + (seconds == 1 and "second" or "seconds" )

    return string;
            
def getTunnelUrl():
    """Get ngrok tunnel url"""
    tunnels = ngrok.get_tunnels()
    return tunnels
 
def readFile(filename):
    """Read file."""
    file = open(os.path.join(FILE_DIR, filename), 'r+')
    code = file.read()
    file.close()
    return code
        
def saveFile(filename, content):
    """Read file."""
    file = open(os.path.join(FILE_DIR, filename), 'w+')
    code = file.read()
    file.write(content)
    file.close()
    return code 
