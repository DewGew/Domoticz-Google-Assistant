"""Helper classes for Google Assistant integration."""

import os
import io
import json
import yaml
import logging
from pip._internal import main as pip
import time
import requests
from const import (CONFIGFILE, LOGFILE, KEYFILE, HOMEGRAPH_SCOPE, HOMEGRAPH_TOKEN_URL, REQUEST_SYNC_BASE_URL)
try:
    import google.auth.crypt
    import google.auth.jwt
except ImportError as e:
    pip.main(['install', 'google-auth'])
    import google.auth.crypt
    import google.auth.jwt

FILE_PATH = os.path.abspath(__file__)
FILE_DIR = os.path.split(FILE_PATH)[0]

def readFile(filename):
    """Read file."""
    try:
        file = open(os.path.join(FILE_DIR, filename), 'r+')
        content = file.read()
        file.close()
        return content
    except:
        if filename == LOGFILE:
            content = " ** If you want to show the logs here, set 'logtofile: true' in configuration **"
        else:
            content = "Problem opening this file"
        return content
        
def saveFile(filename, content):
    """Read file."""
    file = open(os.path.join(FILE_DIR, filename), 'w+')
    code = file.read()
    file.write(content)
    file.close()
    return code

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
if 'logtofile' in configuration:
    if configuration['logtofile'] == True or configuration['logtofile'] == 'Overwrite' or configuration['logtofile'] == 'Append':
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s', "%Y-%m-%d %H:%M:%S")
        if configuration['logtofile'] == 'Append':
            fh = logging.FileHandler(os.path.join(FILE_DIR, LOGFILE), mode='a')
        else:
            fh = logging.FileHandler(os.path.join(FILE_DIR, LOGFILE), mode='w')
        fh.setLevel(loglevel)
        fh.setFormatter(formatter)
        logger.addHandler(fh)
if 'logtofile' not in configuration or configuration['logtofile'] == False:
    logfile = os.path.join(FILE_DIR, LOGFILE)
    if os.path.exists(logfile):
        logger.info('Delete log file')
        os.remove(logfile)
if 'ngrok_tunnel' in configuration and configuration['ngrok_tunnel'] == True:
    try:
        from pyngrok import ngrok
    except ImportError:
        logger.info('Installing package pyngrok')
        pip.main(['install', 'pyngrok'])
        from pyngrok import ngrok
        
Auth = {
    'clients': {
        configuration['ClientID']: {
          'clientId': configuration['ClientID'],
          'clientSecret': configuration['ClientSectret'],
        },
    },
    'tokens': {
        'ZsokmCwKjdhk7qHLeYd2': {
            'uid': '1234',
            'accessToken': 'ZsokmCwKjdhk7qHLeYd2',
            'refreshToken': 'ZsokmCwKjdhk7qHLeYd2',
            'userAgentId': '1234',
        },
        'bfrrLnxxWdULSh3Y9IU2cA5pw8s4ub': {
            'uid': '2345',
            'accessToken': 'bfrrLnxxWdULSh3Y9IU2cA5pw8s4ub',
            'refreshToken': 'bfrrLnxxWdULSh3Y9IU2cA5pw8s4ub',
            'userId': '2345'
        },
    },
    'users': {
        '1234': {
            'uid': '1234',
            'name': configuration['auth_user'],
            'password': configuration['auth_pass'],
            'tokens': ['ZsokmCwKjdhk7qHLeYd2'],
        },
        # '2345': {
            # 'uid': '2345',
            # 'name': configuration['auth_user_2'],
            # 'password': configuration['auth_pass_2'],
            # 'tokens': ['bfrrLnxxWdULSh3Y9IU2cA5pw8s4ub'],
        # },
    },
    'usernames': {
        configuration['auth_user']: '1234',
        #configuration['auth_user_2']: '2345',
    }
}
        
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
        self.report_state = True

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
    if 'ngrok_tunnel' in configuration and configuration['ngrok_tunnel'] == True:
        tunnels = ngrok.get_tunnels()
        if tunnels != []:
           tunnel = tunnels[0].public_url
           if 'https' not in tunnel:
               public_url = tunnel.replace('http', 'https')
           else:
               public_url = tunnel
    else:
        public_url = 'https://[YOUR REVERSE PROXY URL]'
        
    return public_url
    
class ReportState:
    """Google Report State implementation."""
    
    def __init__(self):
        """Log error code."""
        self._access_token = None
        self._access_token_expires = None

    def enable_report_state(self):
        try:
            file = open(os.path.join(FILE_DIR, KEYFILE), 'r')
            file.close()
            return True
        except:
            return False
        
    
    def generate_jwt(self, sa_keyfile):
        """Generates a signed JSON Web Token using a Google API Service Account."""
        now = int(time.time())
        expires = now + 3600
        self._access_token_expires = expires

        with io.open(sa_keyfile, 'r', encoding='utf-8') as json_file:
            data = json.load(json_file)
            iss = data['client_email']          

        # build payload
        payload = {
                'iss': iss,
                'scope': HOMEGRAPH_SCOPE,
                'aud': HOMEGRAPH_TOKEN_URL,
                'iat': now,
                "exp": expires,
            }

        # sign with keyfile
        signer = google.auth.crypt.RSASigner.from_service_account_file(sa_keyfile)
        jwt = google.auth.jwt.encode(signer, payload)

        return jwt
        
    def get_access_token(self):
        """Generates a signed JSON Web Token using a Google API Service Account."""
        signed_jwt = self.generate_jwt(os.path.join(FILE_DIR, KEYFILE))
        if signed_jwt == None:
            return False
        url = HOMEGRAPH_TOKEN_URL
        headers = {'Content-Type': 'application/x-www-form-urlencoded'}
        data = 'grant_type=urn%3Aietf%3Aparams%3Aoauth%3Agrant-type%3Ajwt-bearer&assertion=' + signed_jwt.decode('utf-8')

        r = requests.post(url, headers=headers, data=data)

        if r.status_code == requests.codes.ok:
            token_data = json.loads(r.text)
            self._access_token = token_data['access_token']
            return token_data['access_token']

        r.raise_for_status()
        return
        
    def call_homegraph_api_key(self, url, data):
   
        url = url + '?key=' + configuration['Homegraph_API_Key']
        
        r = requests.post(url, json=data)
        
        if 'error' in r.text:
            logger.error(r.text)
        
        return r.status_code == requests.codes.ok
        
    def call_homegraph_api(self, url, data):
        """Makes an authorized request to the endpoint"""
        now = int(time.time())
        if not self._access_token or now > self._access_token_expires:
            self.get_access_token()
        elif self._access_token == False:
            return   

        headers = {
            'X-GFE-SSL': 'yes',
            'Authorization': 'Bearer ' + self._access_token
        }

        r = requests.post(url, headers=headers, json=data)

        r.raise_for_status()

        logger.info("Device state reported %s" % (json.dumps(data, indent=2, sort_keys=False)))
        return r.status_code == requests.codes.ok
