# -*- coding: utf-8 -*-
import os
import yaml

FILE_PATH = os.path.abspath(__file__)
FILE_DIR = os.path.split(FILE_PATH)[0]
CONFIGFILE = 'config.yaml'

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

try:
    print('Loading configuration...')
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
    
                    
"""Constants for Google Assistant."""
HOMEGRAPH_URL = 'https://homegraph.googleapis.com/'
REQUEST_SYNC_BASE_URL = HOMEGRAPH_URL + 'v1/devices:requestSync'

SESSION_TIMEOUT = 3600
AUTH_CODE_TIMEOUT = 600

DOMOTICZ_URL = configuration['Domoticz']['ip'] + ':' + configuration['Domoticz']['port']
DOMOTICZ_GET_ALL_DEVICES_URL = DOMOTICZ_URL + '/json.htm?type=devices&plan=' + configuration['Domoticz']['roomplan'] + '&filter=all&used=true'
DOMOTICZ_GET_ONE_DEVICE_URL = DOMOTICZ_URL + '/json.htm?type=devices&rid='
DOMOTICZ_GET_SCENES_URL = DOMOTICZ_URL + '/json.htm?type=scenes'
DOMOTICZ_GET_SETTINGS_URL = DOMOTICZ_URL + '/json.htm?type=settings'
DOMOTICZ_GET_CAMERAS_URL = DOMOTICZ_URL + '/json.htm?type=cameras'

#https://developers.google.com/actions/smarthome/guides/
PREFIX_TYPES = 'action.devices.types.'
TYPE_AC_UNIT = PREFIX_TYPES + 'AC_UNIT'
TYPE_BLINDS = PREFIX_TYPES + 'BLINDS'
TYPE_CAMERA = PREFIX_TYPES + 'CAMERA'
TYPE_COFFEE = PREFIX_TYPES + 'COFFEE_MAKER'
TYPE_DISHWASHER = PREFIX_TYPES + 'DISHWASHER'
TYPE_DOOR = PREFIX_TYPES + 'DOOR'
TYPE_DRYER = PREFIX_TYPES + 'DRYER'
TYPE_FAN = PREFIX_TYPES + 'FAN'
TYPE_GATE = PREFIX_TYPES + 'GATE'
TYPE_HEATER = PREFIX_TYPES + 'HEATER'
TYPE_LIGHT = PREFIX_TYPES + 'LIGHT'
TYPE_LOCK = PREFIX_TYPES + 'LOCK'
TYPE_OUTLET = PREFIX_TYPES + 'OUTLET'
TYPE_SCENE = PREFIX_TYPES + 'SCENE'
TYPE_SCREEN = PREFIX_TYPES + 'SCREEN'
TYPE_SECURITY = PREFIX_TYPES + 'SECURITYSYSTEM'
TYPE_SENSOR = PREFIX_TYPES + 'SENSOR'
TYPE_SPEAKER = PREFIX_TYPES + 'SPEAKER'
TYPE_SPRINKLER = PREFIX_TYPES + 'SPRINKLER'
TYPE_SWITCH = PREFIX_TYPES + 'SWITCH'
TYPE_THERMOSTAT = PREFIX_TYPES + 'THERMOSTAT'
TYPE_MEDIA = PREFIX_TYPES + 'TV'
TYPE_VACUUM = PREFIX_TYPES + 'VACUUM'
TYPE_WATERHEATER = PREFIX_TYPES + 'WATERHEATER'
TYPE_WASHER = PREFIX_TYPES + 'WASHER'
TYPE_WINDOW = PREFIX_TYPES + 'WINDOW'

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
lightDOMAIN = 'Light'
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
sensorDOMAIN = 'Sensor'
doorDOMAIN = 'DoorSensor'
selectorDOMAIN = 'Selector'

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
    sensorDOMAIN: TYPE_SENSOR,
    doorDOMAIN: TYPE_DOOR,
    selectorDOMAIN: TYPE_SWITCH,
}

#Todo... dynamic tokens handling/generation if needed
Auth = {
    'clients': {
        configuration['ClientID']: {
          'clientId':       configuration['ClientID'],
          'clientSecret':   configuration['ClientSectret'],
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
            'name': configuration['auth_user'],
            'password': configuration['auth_pass'],
            'tokens': ['ZsokmCwKjdhk7qHLeYd2'],
        },
    },
    'usernames': {
        configuration['auth_user']: '1234',
    }
}

TEMPLATE = """
<html>
<head>
<title>Control Panel</title>     
<meta charset="utf-8">
{meta}
<meta name="viewport" content="width=device-width, initial-scale=0.86, maximum-scale=3.0, minimum-scale=0.86">
<link rel="stylesheet" href="https://fonts.googleapis.com/icon?family=Material+Icons">
<link rel="stylesheet" href="https://code.getmdl.io/1.3.0/material.indigo-pink.min.css">
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/codemirror/5.48.4/codemirror.css" />
<script src="https://cdnjs.cloudflare.com/ajax/libs/codemirror/5.48.4/codemirror.js"></script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/codemirror/5.48.4/mode/python/python.js"></script>
<script defer src="https://code.getmdl.io/1.3.0/material.min.js"></script>


<style>
.mdl-layout__content {{
    padding: 48px;
    }}
</style>

</head>
<body>
    <dialog class="mdl-dialog">
    <h4 class="mdl-dialog__title">Security Risk!</h4>
    <div class="mdl-dialog__content">
      <p>
       Seems that you are using default username or/and password. Please change username and password.
      </p>
    </div>
    <div class="mdl-dialog__actions">
      <button type="button" class="mdl-button close">Close</button>
    </div>
    </dialog>
    <div class="mdl-layout mdl-js-layout mdl-layout--fixed-header mdl-color--grey-300 mdl-layout--fixed-tabs">
        <header class="mdl-layout__header">
            <!-- Title -->
            <div class="mdl-layout__header-row">          
                <span class="mdl-layout-title">Domoticz Google Assistant</span>
            </div>
            <!-- Tabs -->
            <div class="mdl-layout__tab-bar mdl-js-ripple-effect">
                <a href="#fixed-tab-1" class="mdl-layout__tab is-active">Control Panel</a>
                <a href="#fixed-tab-2" class="mdl-layout__tab">Device List</a>
                <a href="#fixed-tab-3" class="mdl-layout__tab">Config File</a>
                <a href="#fixed-tab-4" class="mdl-layout__tab">Setup Actions on Google</a>
                <a href="#fixed-tab-5" class="mdl-layout__tab">Help</a>
            </div>
        </header>
        <main class="mdl-layout__content">
            <section class="mdl-layout__tab-panel is-active" id="fixed-tab-1">
                <div class="page-content">
                <div class="mdl-grid">
                    <div class="mdl-cell mdl-cell--4-col">
                    <p>This project is based on Pawcio's script at <a href="https://www.domoticz.com/forum/viewtopic.php?f=69&amp;t=27244">domoticz forum</a> and the <a href="https://github.com/home-assistant/home-assistant/tree/dev/homeassistant/components/google_assistant">home assistant implementation</a></p>
                    <p>Domoticz-Google-Assistant delivers:<br />
                    <ul>
                    <li>the oauth authorization and smarthome endpoint for the google assistant</li>
                    <li>Two-factor authentication pin for domoticz protected devices (works best with english language)</li>
                    <li>Acknowledgement with Yes or No. (works best with english language)</li>
                    <li>Arm Disarm Securitypanel (works best with english language)</li>
                    <li>On/Off, Brightness, Thermostat, Color Settings, speaker volume, Lock/Unlock, Scene and Open/Close</li>
                    <li>Stream surveillance camera to chromecast</li></p>
                    <p>Please feel free to modify it, extend and improve</p>
                    <p>Report issues <a href="https://github.com/DewGew/Domoticz-Google-Assistant/issues">here</a></p>
                    </div>
                    <div class="mdl-cell mdl-cell--4-col mdl-typography--text-center">
                        <p><form action="/settings" method="post">
                            <button class="mdl-button mdl-js-button mdl-button--raised mdl-js-ripple-effect mdl-button--colored" name="restart" value="restart">Restart Server</button>
                            <button class="mdl-button mdl-js-button mdl-button--raised mdl-js-ripple-effect mdl-button--colored" name="sync" value="sync">Sync Devices</button>
                        </form></p>
                        <p class="mdl-button mdl-js-button mdl-js-ripple-effect mdl-color-text--light-green-900" id="message">{message}</p>
                        <div class="mdl-card__supporting-text">Sytem Uptime:</br>{uptime}</div>
                    </div>
                    <div class="mdl-cell mdl-cell--4-col">
		    <h5>Quick start</h5>
		    Visit the Actions on Google console at <a href="http://console.actions.google.com">http://console.actions.google.com</a>.<br>Under Develop section, replace the fulfillment URL in Actions with:<br>
                    <a>{public_url}/smarthome</a><br><br>
                    In Account linking, set the Authorization URL to:<br>
                    <a>{public_url}/oauth</a><br><br>
                    Then set the Token URL to:<br>
                    <a>{public_url}/token</a><br><br>
                    Finally press \'SAVE\' and then \'TEST\' button<br>
                    </div>
                </div>
                </div>
            </section>
            <section class="mdl-layout__tab-panel" id="fixed-tab-2">
                <div class="page-content">
                <h5>Device list</h5>
                <span class="mdl-card__supporting-text">List of devices the server recived from domoticz. Room and Nickname is added in domoticz device description.</span><br>
                <span class="mdl-card__supporting-text">If you don't see any device check your connection to domoticz.</span>
				<div class="mdl-grid">
                    <div class="mdl-cell mdl-cell--1-col">
                        <h5>Idx</h5>
                        <div id="deviceList_idx"></div>
					</div>
					<div class="mdl-cell mdl-cell--3-col">
                        <h5>Device Name</h5>
                        <div id="deviceList_name"></div>
					</div>
					<div class="mdl-cell mdl-cell--2-col">
                        <h5>Device Type</h5>
                        <div id="deviceList_type"></div>
					</div>
					<div class="mdl-cell mdl-cell--2-col">
                        <h5>State</h5>
                        <div id="deviceList_state"></div>
                    </div>
					<div class="mdl-cell mdl-cell--2-col">
                        <h5>Room</h5>
                        <div id="deviceList_room"></div>
                    </div>
                    <div class="mdl-cell mdl-cell--2-col">
                        <h5>Nickname</h5>
                        <div id="deviceList_nickname"></div>
                    </div>
                </div>
				</div>
            </section>
            <section class="mdl-layout__tab-panel" id="fixed-tab-3">
                <div class="page-content">
					<h5>Configuration</h5>
                    <textarea id="code">{code}</textarea>
				<div class="mdl-grid">
                    <div class="mdl-cell mdl-cell--4-col">
                    <form action="/settings" method="post">
                        <button class="mdl-button mdl-js-button mdl-button--raised mdl-js-ripple-effect mdl-button--colored" name="save" id="save">Save</button>
			<button class="mdl-button mdl-js-button mdl-button--raised mdl-js-ripple-effect mdl-button--colored" name="backup" value="backup">Backup Config</button>
                    	<button class="mdl-button mdl-js-button mdl-button--raised mdl-js-ripple-effect mdl-button--colored" name="restart" value="restart">Restart Server</button>
		    </form>
                    </div>
                    <div class="mdl-cell mdl-cell--4-col">
                        <p class="mdl-card__supporting-text">Restart server to activate your changes</p>
                    </div>
					<div class="mdl-cell mdl-cell--4-col"></div>
                </div>
                </div>
            </section>
            <section class="mdl-layout__tab-panel" id="fixed-tab-4">
                <div class="page-content">
                <h5>Setup Actions on Google Console Instructions</h5>
                <ul>
                <li><p>Use the <a href="https://console.actions.google.com/">Actions on Google Console</a> to add a new project with a name of your choosing and click     - Create Project.</p>

                <ul>
                <li>Click Home Control, then click Smart Home.</li>
                <li>On the top menu click Develop, then on the left navigation menu click on Invocation.</li>
                <li>Add your App's name. Click Save.</li>
                <li>Click 'Save'.</li>
                </ul></li>
                <li><p>Add Credentials</p>

                <ul>
                <li>Navigate to the <a href="https://console.cloud.google.com/apis/credentials">Google Cloud Console API Manager</a> for your project id.</li>
                <li>Click 'Create credentials'</li>
                <li>Click 'OAuth client ID'</li>
                <li>Choose 'other'</li>
                <li>Add name e.g. 'SmartHomeClientID'</li>
                <li>Copy the client ID shown and insert it in <code>clientID</code> in config.yaml</li>
                <li>Copy the client secret shown and insert it in <code>clientSecret</code> in config.yaml</li>
                </ul></li>
                <li><p>Add Request Sync</p>

                <p>The Request Sync feature allows a cloud integration to send a request to the Home Graph to send a new SYNC request.</p>

                <ul>
                <li>Navigate to the <a href="https://console.cloud.google.com/apis/credentials">Google Cloud Console API Manager</a> for your project id.</li>
                <li>Enable the HomeGraph API. This will be used to request a new sync and to report the state back to the HomeGraph.</li>
                <li>Click Credentials</li>
                <li>Click 'Create credentials'</li>
                <li>Click 'API key'</li>
                <li>Copy the API key shown and insert it in <code>Homegraph_API_Key</code> in config.yaml.</li>
                </ul></li>
                <li><p>Navigate back to the <a href="https://console.actions.google.com/">Actions on Google Console</a>.</p>

                <ul>
                <li>On the top menu click Develop, then on the left navigation menu click on Actions.
                Enter the URL for fulfillment, e.g. <a>{public_url}/smarthome</a>, click Done.</li>
                <li>On the left navigation menu under Account Linking.</li>
                <li>Under Client Information, enter the client ID and secret from earlier.</li>
                <li>Change Authorization URL to <a>{public_url}/oauth</a>.</li>
                <li>Change Token URL to <a>{public_url}/token</a>.</li>
                <li>Do NOT check 'Google to transmit clientID and secret via HTTP basic auth header'.</li>
                <li>Click 'Save' at the top right corner, then click 'Test' to generate a new draft version of the Test App.</li>
                </ul></li>
                </ul>
				</div>
            </section>
            <section class="mdl-layout__tab-panel" id="fixed-tab-5">
                <div class="page-content">
					<h5>Help</h5>
                    
                    <h5>Configuration Settings</h5>

                    <p><b>port_settings:</b><br>Set the local port. Default is <code>port_number: 3030</code></p>                   
                    <p><b>ngrok_tunnel:</b><br>Use Ngrok tunnel true or false. Instantly create a public HTTPS URL.<br>Don't have to open any port on router and do not require a reverse proxy.<br><b>NOTE:</b>Ngrok assigns random urls. When server restart the server gets a new url</p>                   
                    <p><b>auth_user/auth_pass:</b><br>Set the authorization username and password.</p>

                    <p><b>Domoticz:</b><br>Add correct ipaddress, port and credientials to connect to domoticz. </br>You can assign devices in a room in domoticz then set the room idx in <code>roomplan:</code></br>
                    <code>switchProtectionPass:</code> is set equal to 'Light/Switch Protection' in domoticz settings. Required to be in numbers to work properly. Set this to false if ask for pin function is not needed.</p>
                    <p><b>ClientID/ClientSectret:</b><br>Set the Google credientials.</p>
                    <p><b>Homegraph_API_Key:</b><br>Homegraph API key from Google. The Request Sync feature allows a cloud integration to send a request to the Home Graph to send a new SYNC request. Not required</p>
                    <p><b>Low_battery_limit:</b><br>Set threhold for report low battery.</p>
                    <p><b>Image_Override:</b><br>Ligths, switches, media, etc. are using domoticz's "Light/Switch" type. To differentiate them additionaly add image name</p>
                    <p><b>Camera_Stream:</b><br>In domoticz you need to attach a switch to your camera, Add switch idx and camera stream url. Read more below.<p>
                    <p><b>Armhome/Armaway:</b><br>User-friendly name for the arm level in your language.</p>
                    
                    <h5>Device Settings</h5>

                    <p>Nicknames, rooms and ack can be set in the Domoticz user interface. Simply put the device configuration in the device description, in a section between 'voicecontrol' tags like:
                    <code><br />
                    &lt;voicecontrol&gt;<br />
                    nicknames = Kitchen Blind One, Left Blind, Blue Blind<br />
                    room = Kitchen<br />
                    ack = True<br />
                    &lt;/voicecontrol&gt;<br />
                    </code>
                    Other parts of the description are ignored, so you can still leave other useful descriptions.
                    Every variable should be on a separate line.
                    If there is no such configuration in the Domoticz device it will still try the config.</p>

                    <h5>Stream camera to chromecast</h5>

                    <p>Stream security camera to chromecast. Supports hls, dash, smooth streaming, Progressive MP4 urls. More info: https://developers.google.com/actions/smarthome/traits/camerastream#video-formats. You need a to convert your video url to one of above. Try with ffmpeg or with a surveillance software system. Try out http://shinobi.video. <br />
                    In domoticz you need to attach a switch to your camera (create a switch then in Settings/Camera, add the switch to the camera)</p>

                    <p>Example convert rtsp to hls or mp4 using ffmpeg:<br />
                    <code>
                    ffmpeg -rtsp_transport tcp -i rtsp://admin:123456@192.168.0.218/live/ch1 \
                      -acodec copy \
                      -vcodec copy \
                      -hls_wrap 40 \
                      -flags -global_header \
                      /var/www/html/cam/cam.m3u8
                    </code><br />
                    <code>
                    ffmpeg -rtsp_transport tcp -i rtsp://admin:123456@192.168.0.218/live/ch1 \
                      -c:a aac \
                      -vcodec copy \
                      -f mp4 \
                      -y \
                      -flags -global_header \
                      /var/www/html/cam/cam.mp4
                    </code>
                    </p>
                    
                    <h5>Other</h5>
                    
                    <h6>Connect smart home devices to your Google Home device</h6>
                    <ul>
                    <li>On your mobile device, open the Google Home app.</li>
                    <li>On the Home tab, tap the “Add” quick action .</li>
                    <li>Tap Set up a device</li>
                    <li>Tap Have something already set up?</li>
                    <li>Select your device app e.g: "[test]Your Appname"</li>
                    <li>Login with auth credentials from config</li>
                    </ul>
                    
                    <h6>Share devices</h6>

                    <p>If you want to allow other household users to control the devices:<br />
                    <ul>
                    <li>Go to the settings for the project you created in the <a href="https://console.actions.google.com/">Actions on Google Console</a>.</li>
                    <li>Click <code>Test -&gt; Simulator</code>, then click Share icon in the right top corner. Follow the on-screen instruction:</li>
                    <li>Add team members:</li>
                    <li>Got to <code>Settings -&gt; Permission</code>, click Add, type the new user’s e-mail address and choose <code>Project -&gt; Viewer role</code>.</li>
                    <li>Copy and share the link with the new user.</li>
                    <li>When the new user opens the link with their own Google account, it will enable your draft test app under their account.</li>
                    <li>Have the new user go to their Google Home app to add "[test]Your Appname" to their account. Login with Oauth credentials from config.py</li>
                    </ul></p>
                    
                    <h6>Update</h6>

                    <p><code>
                    cd /home/${{USER}}/Domoticz-Google-Assistant/<br />
                    git pull
                    </code><br /><br />
                    If needed, restart service:
                    <code><br />
                    sudo systemctl restart dzga.service
                    </code><br /></p>
                </div>
            </section>
        </main>
    </div>
	
<script>
var config = {conf}
var dialog = document.querySelector('dialog');
var showDialogButton = document.querySelector('#show-dialog');
if (! dialog.showModal) {{
  dialogPolyfill.registerDialog(dialog);
}}
if (config.auth_user == 'admin' || config.auth_password == 'admin') {{
  dialog.showModal();
}};
dialog.querySelector('.close').addEventListener('click', function() {{
  dialog.close();
}});

var devicelist = {list}
var x,y,z,w,v,q,i = "";
for (i in devicelist){{
	x += devicelist[i][1] + "<br>";
	y += devicelist[i][0] + "<br>";
	z += devicelist[i][2] + "<br>";
	w += devicelist[i][3] + "<br>";
    v += devicelist[i][4] + "<br>";
    q += devicelist[i][5] + "<br>";
}}
if (typeof x !== "undefined"){{
    document.getElementById("deviceList_idx").innerHTML = x.replace('undefined','');
    document.getElementById("deviceList_name").innerHTML = y.replace('undefined','');
    document.getElementById("deviceList_type").innerHTML = z.replace('undefined','');
    document.getElementById("deviceList_state").innerHTML = w.replace('undefined','');
    document.getElementById("deviceList_room").innerHTML = v.replace(/undefined|null/g,'');
    document.getElementById("deviceList_nickname").innerHTML = q.replace(/undefined|null/g,'');
}}else{{
    document.getElementById("deviceList_idx").innerHTML = x;
    document.getElementById("deviceList_name").innerHTML = y;
    document.getElementById("deviceList_type").innerHTML = z;
    document.getElementById("deviceList_state").innerHTML = w;
    document.getElementById("deviceList_room").innerHTML = v;
    document.getElementById("deviceList_nickname").innerHTML = q;
    document.getElementById("message").innerHTML = "Connection to Domoticz refused!. Check configuration.";
}}
    
var editor = CodeMirror.fromTextArea(document.getElementById("code"), {{
    lineNumbers: true,
    mode: "python"
}});
editor.setSize("100%", "80%");
editor.on("change", function() {{
    textTosave = editor.getValue();
    console.log(textTosave);
    document.getElementById("save").value = textTosave;
 }});
 
document.getElementById("save").value = document.getElementById("code").value

</script>    
</body>
</html>
"""
