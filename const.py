# -*- coding: utf-8 -*-
from helpers import configuration
                    
"""Constants for Google Assistant."""
VERSION = '1.3.4'
PUBLIC_URL = 'https://[YOUR REVERSE PROXY URL]'
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
fanDOMAIN = 'Fan'

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
    fanDOMAIN: TYPE_FAN,
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
<!doctype html>
<html lang="en">
  <head>
    <!-- Required meta tags -->
    <meta charset="utf-8">
    {meta}
    <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">

    <!-- Material Design for Bootstrap fonts and icons -->
    <link rel="stylesheet" href="https://fonts.googleapis.com/css?family=Roboto:300,400,500,700|Material+Icons">

    <!-- Material Design for Bootstrap CSS -->
    <link rel="stylesheet" href="https://unpkg.com/bootstrap-material-design@4.1.1/dist/css/bootstrap-material-design.min.css" integrity="sha384-wXznGJNEXNG1NFsbm0ugrLFMQPWswR3lds2VeinahP8N0zJw9VWSopbjv2x7WCvX" crossorigin="anonymous">
    
    <!-- Codemirror CSS -->
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/codemirror/5.48.4/codemirror.css" />

    
    <title>Domoticz Google Assistant v""" + VERSION + """</title>
  </head>
  <body>
    <!-- Modal -->
    <div class="modal fade" id="messageModal" tabindex="-1" role="dialog" aria-labelledby="exampleModalLabel" aria-hidden="true">
      <div class="modal-dialog" role="document">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title" id="exampleModalLabel">Security Risk</h5>
            <button type="button" class="close" data-dismiss="modal" aria-label="Close">
              <span aria-hidden="true">&times;</span>
            </button>
          </div>
          <div class="modal-body" id="message">
            Please change the default username and password and restart server!
          </div>
          <div class="modal-footer">
            <button type="button" class="btn btn-secondary" data-dismiss="modal">Close</button>
          </div>
        </div>
      </div>
    </div>
    <nav class="navbar navbar-expand-lg navbar-dark bg-primary">
    <a class="navbar-brand" href="/settings">
        <img src="https://upload.wikimedia.org/wikipedia/commons/5/5a/Google_Assistant_logo.png" width="30" height="30" class="d-inline-block align-top" alt="">
        Domoticz Google Assistant</a>
    <button class="navbar-toggler" type="button" data-toggle="collapse" data-target="#navbarNav" aria-controls="navbarNav" aria-expanded="false" aria-label="Toggle navigation">
    <span class="navbar-toggler-icon"></span>
    </button>
    <div class="collapse navbar-collapse" id="navbarNav">
    <ul class="nav nav-tabs bg-primary">
      <li class="nav-item">
        <a data-toggle="tab" class="nav-link active" href="#home">Home</a>
      </li>
      <li class="nav-item">
        <a data-toggle="tab" class="nav-link" href="#menu1">Devices</a>
      </li>
      <li class="nav-item">
        <a data-toggle="tab" class="nav-link" href="#menu2">Configuration</a>
      </li>
      <li class="nav-item" data-toggle="tooltip" data-placement="bottom" title="Setup Actions on Google">
        <a data-toggle="tab" class="nav-link" href="#menu3"><i class="material-icons">info</i></a>
      </li>
      <li class="nav-item" data-toggle="tooltip" data-placement="bottom" title="Help">
        <a data-toggle="tab" class="nav-link" href="#menu4"><i class="material-icons">help</i></a>
      </li>
      <li class="nav-item" data-toggle="tooltip" data-placement="bottom" title="Log">
        <a data-toggle="tab" class="nav-link" href="#menu5"><i class="material-icons">notes</i></a>
      </li>
    </ul>
    </div>
    </nav>
   <div class="container">
    <div class="tab-content">
        <div id="home" class="tab-pane fade show active" role="tabpanel">
            <div class="row">
              <div class="col-8">
                <p class="lead"><br>This project is based on Pawcio's script at <a href="https://www.domoticz.com/forum/viewtopic.php?f=69&amp;t=27244">domoticz forum</a> and the <a href="https://github.com/home-assistant/home-assistant/tree/dev/homeassistant/components/google_assistant">home assistant implementation</a></p>
                <p class="lead">Domoticz-Google-Assistant delivers:<br />
                <ul>
                <li>The oauth authorization and smarthome endpoint for the google assistant</li>
                <li>Two-factor authentication pin for domoticz protected devices (works best with english language)</li>
                <li>Acknowledgement with Yes or No. (works best with english language)</li>
                <li>Arm Disarm Securitypanel (works best with english language)</li>
                <li>On/Off, Brightness, Thermostat, Color Settings, speaker volume, Lock/Unlock, Scene and Open/Close</li>
                <li>Stream surveillance camera to chromecast</li>
                </ul>
                </p>
                <p class="lead">Please feel free to modify it, extend and improve</p>
                <p class="lead text-info">Before you can use dzga. Setup Action on Google and configure settings in configuration.</p>
                <p class="lead">Report issues <a href="https://github.com/DewGew/Domoticz-Google-Assistant/issues">here</a></p>            
              </div>
              <div class="col-4">
                <p>
                <form action="/settings" method="post">
                    <button class="btn btn-raised btn-primary" name="restart" value="restart"><i class="material-icons" style="vertical-align: middle;">replay</i> Restart Server</button>
                    <button class="btn btn-raised btn-primary" name="sync" value="sync"><i class="material-icons" style="vertical-align: middle;">sync</i> Sync Devices</button>
                </form>
                </p>
                <p class="font-weight-bold text-success">{message}</p>
                <small class="text-muted">
                    <p>Quick start<p>
                    Visit the Actions on Google console at <a href="http://console.actions.google.com">http://console.actions.google.com</a>.<br>Under Develop section, replace the fulfillment URL in Actions with:<br>
                    <kbd>{public_url}/smarthome</kbd><br><br>
                    In Account linking, set the Authorization URL to:<br>
                    <kbd>{public_url}/oauth</kbd><br><br>
                    Then set the Token URL to:<br>
                    <kbd>{public_url}/token</kbd><br><br>
                    Finally press <kbd>SAVE</kbd> and then <kbd>TEST</kbd> button<br>
              </small>
              </div>
            </div>
            <div class="row">
              <div class="col">
                <i class="material-icons" style="vertical-align: middle;">timelapse</i><small class="text-muted"> Sytem Uptime:<br>{uptime}</small>
              </div>
              <div class="col">
                <small class="text-muted">DZGA Version:<br>V""" + VERSION + """</small><br>
                <small class="text-muted" id="updates"></small>
              </div>
              <div class="col" id="buttonUpdate">
              
              </div>
              <div class="col">
                <small class="text-muted"><a href="https://github.com/DewGew/Domoticz-Google-Assistant">Source Code at Github</a></small><br>
                <small class="text-muted"><a href="https://www.domoticz.com/wiki/Google_Assistant#Domoticz_Google_Assistant_Server_python">Domoticz wiki</a></small>
              </div>
            </div>
        </div>
        <div id="menu1" class="tab-pane fade" role="tabpanel">
            <br>
            <h5>Device list</h5>
            <small class="text-muted">List of devices the server recived from domoticz. Room and Nicknames added in configuration. <b>Click on Header to sort asc or desc</b><br><b>NOTE:</b> If you don't see any device check your connection to domoticz.</small>
            <table class="table" id="deviceTable">
              <thead>
                <tr>
                  <th scope="col" onclick="sortIdxTable(0)">Idx</th>
                  <th scope="col" onclick="sortTable(0)">Name <small><i>(Nicknames)</i></small></th>
                  <th scope="col" onclick="sortTable(1)">Type</th>
                  <th scope="col" onclick="sortTable(2)">State</th>
                  <th scope="col" onclick="sortTable(3)">Room</th>
                </tr>
              </thead>
              <tbody id="deviceList_idx" ></tbody>
            </table>
        </div>
        <div id="menu2" class="tab-pane fade" role="tabpanel">
            <br>
            <h5>Configuration</h5>
            <textarea id="code" style="width: 100%;">{code}</textarea>
            <br>
            <div class="row">
              <div class="col">
              <form action="/settings" method="post">
                <button class="btn btn-raised btn-primary" name="save" id="save"><i class="material-icons" style="vertical-align: middle;">save</i> Save</button>
                <button class="btn btn-raised btn-primary" name="backup" value="backup"><i class="material-icons" style="vertical-align: middle;">save_alt</i> Backup Config</button>
                <button class="btn btn-raised btn-primary" name="restart" value="restart"><i class="material-icons" style="vertical-align: middle;">replay</i> Restart Server</button>
                </form>
                <p class="text-muted">Restart server to activate your changes</p>
              </div>
            </div>
        </div>
        <div id="menu3" class="tab-pane fade" role="tabpanel">
            <br>
            <h5>Setup Actions on Google Console Instructions</h5>
            <ul>
            <li><p>Use the <a href="https://console.actions.google.com/">Actions on Google Console</a> to add a new project with a name of your choosing and click     - Create Project.</p>

            <ul>
            <li>Click Home Control, then click Smart Home.</li>
            <li>On the top menu click Develop, then on the left navigation menu click on Invocation.</li>
            <li>Add your App's name. Click Save.</li>
            <li>Click 'Save'.</li>
            </ul></li><br>
            
            <li><p>Add Credentials</p>
            <ul>
            <li>Navigate to the <a href="https://console.cloud.google.com/apis/credentials">Google Cloud Console API Manager</a> for your project id.</li>
            <li>Click 'Create credentials'</li>
            <li>Click 'OAuth client ID'</li>
            <li>Choose 'other'</li>
            <li>Add name e.g. 'SmartHomeClientID'</li>
            <li>Copy the client ID shown and insert it in <code>clientID</code> in config.yaml</li>
            <li>Copy the client secret shown and insert it in <code>clientSecret</code> in config.yaml</li>
            </ul></li><br>
            
            <li><p>Add Request Sync</p>
            <p>The Request Sync feature allows a cloud integration to send a request to the Home Graph to send a new SYNC request.</p>

            <ul>
            <li>Navigate to the <a href="https://console.cloud.google.com/apis/credentials">Google Cloud Console API Manager</a> for your project id.</li>
            <li>Enable the HomeGraph API. This will be used to request a new sync and to report the state back to the HomeGraph.</li>
            <li>Click Credentials</li>
            <li>Click 'Create credentials'</li>
            <li>Click 'API key'</li>
            <li>Copy the API key shown and insert it in <code>Homegraph_API_Key</code> in config.yaml.</li>
            </ul></li><br>
            
            <li><p>Navigate back to the <a href="https://console.actions.google.com/">Actions on Google Console</a>.</p>
            <ul>
            <li>On the top menu click Develop, then on the left navigation menu click on Actions.
            Enter the URL for fulfillment, e.g. <code>{public_url}/smarthome</code>, click Done.</li>
            <li>On the left navigation menu under Account Linking.</li>
            <li>Under Client Information, enter the client ID and secret from earlier.</li>
            <li>Change Authorization URL to <code>{public_url}/oauth</code>.</li>
            <li>Change Token URL to <code>{public_url}/token</code>.</li>
            <li>Do NOT check 'Google to transmit clientID and secret via HTTP basic auth header'.</li>
            <li>Click 'Save' at the top right corner, then click 'Test' to generate a new draft version of the Test App.</li>
            </ul></li>
            </ul>
        </div>
        <div id="menu4" class="tab-pane fade" role="tabpanel">
            <br>
            <h5 id="top">Help</h5>
            <p>
            <a href="#C1">Configuration Settings</a><br>
            <a href="#C2">Device Settings</a><br>
            <a href="#C3">Stream camera to chromecast</a><br>
            <a href="#C4">Other</a><br>
            </p>
            <h5 id="C1">Configuration Settings</h5>
            
            <p><b>port_settings:</b><br>Set the local port. Default is <code>port_number: 3030</code></p>
            <p><b>loglevel:</b><br>Set log level <code>Debug</code>, <code>Info</code> or <code>Error</code>. Default is <code>Info</code></p> 
            <p><b>logtofile:</b><br>Enable or disable write log to file. If 'false' logs will not show in the LOG tab.</p>
            <p><b>userinterface:</b><br>Enable or disable UI</p>
            <p><b>CheckForUpates:</b><br>Enable or disable check for updates</p>
            <p><b>ngrok_tunnel:</b><br>Use Ngrok tunnel true or false. Instantly create a public HTTPS URL.<br>Don't have to open any port on router and do not require a reverse proxy.<br><b>NOTE:</b>Ngrok assigns random urls. When server restart the server gets a new url</p>                   
            <p><b>auth_user/auth_pass:</b><br>Set the authorization username and password.</p>

            <p><b>Domoticz:</b><br>Add correct ipaddress, port and credientials to connect to domoticz. </br>You can assign devices in a room in domoticz then set the room idx in <code>roomplan:</code></br>
            <code>switchProtectionPass:</code> is set equal to 'Light/Switch Protection' in domoticz settings. Required to be in numbers to work properly. Set this to false if ask for pin function is not needed.</p>
            <p><b>ClientID/ClientSectret:</b><br>Set the Google credientials.<br></p>
            <p><b>Homegraph_API_Key:</b><br>Homegraph API key from Google. The Request Sync feature allows a cloud integration to send a request to the Home Graph to send a new SYNC request. Not required.<br>
            </p>
            <p><b>Low_battery_limit:</b><br>Set threhold for report low battery.</p>
            <p><b>Image_Override:</b><br>Ligths, switches, media, etc. are using domoticz's "Light/Switch" type. To differentiate them additionaly add image name</p>
            <p><b>Camera_Stream:</b><br>In domoticz you need to attach a switch to your camera, Add switch idx and camera stream url. Read more below.<p>
            <p><b>Armhome/Armaway:</b><br>User-friendly name for the arm level in your language.</p>
            
            <h5 id="C2">Device Settings</h5>

            <p>Nicknames, rooms and ack can be set in the Domoticz user interface. Simply put the device configuration in the device description, in a section between &lt;voicecontrol&gt; tags like:
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

            <h5 id="C3">Stream camera to chromecast</h5>

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
            
            <h5 id="C4">Other</h5>
            
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

            <p>
            <kbd>bash <(curl -s https://raw.githubusercontent.com/DewGew/dzga-installer/master/install.sh)</kbd><br>
            or <br>
            <code>
            cd /home/${{USER}}/Domoticz-Google-Assistant/<br>
            git pull
            </code><br />
            If needed, restart service:<br />
            <code>
            sudo systemctl restart dzga.service
            </code><br /></p>
            <p><a href="#top">Goto Top</a></p>
        </div>
        <div id="menu5" class="tab-pane fade" role="tabpanel">
            <br>
            <h5>Logs</h5>
            <textarea id="logs" rows="20" style="font-size: 10pt; width: 100%;">{logs}</textarea>
            <br>
            <div class="row">
              <div class="col">
              <form action="/settings" method="post">
                <button class="btn btn-raised btn-primary" name="reload" value="reload"><i class="material-icons" style="vertical-align: middle;">sync</i> Reload logs</button>
                <button class="btn btn-raised btn-primary" name="deletelogs" value="deletelogs"><i class="material-icons" style="vertical-align: middle;">delete</i> Remove logs</button>
               </form>
               <p class="text-muted">Log file will be overwritten when dzga server restarts</p>
              </div>
            </div>
        </div>
    </div>
    </div>
    
    <!-- Optional JavaScript -->
    <!-- jQuery first, then Popper.js, then Bootstrap JS -->
    <script src="https://code.jquery.com/jquery-3.2.1.slim.min.js" integrity="sha384-KJ3o2DKtIkvYIK3UENzmM7KCkRr/rE9/Qpg6aAZGJwFDMVNA/GpGFF93hXpG5KkN" crossorigin="anonymous"></script>
    <script src="https://unpkg.com/popper.js@1.12.6/dist/umd/popper.js" integrity="sha384-fA23ZRQ3G/J53mElWqVJEGJzU0sTs+SvzG8fXVWP+kJQ1lwFAOkcUOysnlKJC33U" crossorigin="anonymous"></script>
    <script src="https://unpkg.com/bootstrap-material-design@4.1.1/dist/js/bootstrap-material-design.js" integrity="sha384-CauSuKpEqAFajSpkdjv3z9t8E7RlpJ1UP0lKM/+NdtSarroVKu069AlsRPKkFBz9" crossorigin="anonymous"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/codemirror/5.48.4/codemirror.js"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/codemirror/5.48.4/mode/yaml/yaml.js"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/codemirror/5.48.4/addon/display/autorefresh.js"></script>
    <script>
    function sortTable(n) {{
      var table, rows, switching, i, x, y, shouldSwitch, dir, switchcount = 0;
      table = document.getElementById("deviceTable");
      switching = true;
      dir = "asc";
      while (switching) {{
        switching = false;
        rows = table.rows;
        for (i = 1; i < (rows.length - 1); i++) {{
          shouldSwitch = false;
          x = rows[i].getElementsByTagName("TD")[n];
          y = rows[i + 1].getElementsByTagName("TD")[n];
          if (dir == "asc") {{
            if (x.innerHTML.toLowerCase() > y.innerHTML.toLowerCase()) {{
              shouldSwitch = true;
              break;
            }}
          }} else if (dir == "desc") {{
            if (x.innerHTML.toLowerCase() < y.innerHTML.toLowerCase()) {{
              shouldSwitch = true;
              break;
            }}
          }}
        }}
        if (shouldSwitch) {{
          rows[i].parentNode.insertBefore(rows[i + 1], rows[i]);
          switching = true;
          switchcount ++;
        }} else {{
          if (switchcount == 0 && dir == "asc") {{
            dir = "desc";
            switching = true;
          }}
        }}
      }}
    }}
    function sortIdxTable(n) {{
      var table, rows, switching, i, x, y, shouldSwitch, dir, switchcount = 0;
      table = document.getElementById("deviceTable");
      switching = true;
      dir = "asc";
      while (switching) {{
        switching = false;
        rows = table.rows;
        for (i = 1; i < (rows.length - 1); i++) {{
          shouldSwitch = false;
          x = rows[i].getElementsByTagName("TH")[n];
          y = rows[i + 1].getElementsByTagName("TH")[n];
          if (dir == "asc") {{
            if (Number(x.innerHTML) > Number(y.innerHTML)) {{
              shouldSwitch = true;
              break;
            }}
          }} else if (dir == "desc") {{
            if (Number(x.innerHTML) < Number(y.innerHTML)) {{
              shouldSwitch = true;
              break;
            }}
          }}
        }}
        if (shouldSwitch) {{
          rows[i].parentNode.insertBefore(rows[i + 1], rows[i]);
          switching = true;
          switchcount ++;
        }} else {{
          if (switchcount == 0 && dir == "asc") {{
            dir = "desc";
            switching = true;
          }}
        }}
      }}
    }}
    $(document).ready(function() {{
    
        var config = {conf}
        var updates = {update}
        if (updates) {{
            document.getElementById("updates").innerHTML = "Updates are Availible.";
            $('#buttonUpdate').append('<br><form action="/settings" method="post"><button class="btn btn-raised btn-primary" name="update" value="update"><i class="material-icons" style="vertical-align: middle;">update</i> Update</button></form>');
            }}
        
        $('body').bootstrapMaterialDesign();
        $(function () {{
          $('[data-toggle="tooltip"]').tooltip()
        }})
        
        if (config.auth_user == 'admin' || config.auth_pass == 'admin'){{
            $('#messageModal').modal('show')
        }}

        var devicelist = {list}
        
        var x,i, nicknames = "";
        for (i in devicelist){{
            if (devicelist[i][4] == undefined) {{
                devicelist[i][4] = " "
            }}
            if (devicelist[i][5] == undefined) {{
                nicknames = " ";
            }}else{{ nicknames = " <small><i>(" + devicelist[i][5] + ")</i></small>"}}
            x += "<tr><th scope='row'>" + devicelist[i][1] + "</th><td>" + devicelist[i][0] +  nicknames + "</td><td>" + devicelist[i][2] + "</td><td>" + devicelist[i][3] + "</td><td>" + devicelist[i][4] + "</td></tr>";

        }}
        if (typeof x !== "undefined"){{
            $('#deviceList_idx').append(x.replace('undefined',''));
        }}else{{
            document.getElementById("exampleModalLabel").innerHTML = "Check configuration.";
            document.getElementById("message").innerHTML = "Connection to Domoticz refused!. Check configuration.";
            $('#messageModal').modal('show')
        }}
            
        var editor = CodeMirror.fromTextArea(document.getElementById("code"), {{
            lineNumbers: true,
            mode: "yaml",
            autoRefresh:true
        }});
        editor.setOption("extraKeys", {{
          Tab: function(cm) {{
            var spaces = Array(cm.getOption("indentUnit") + 1).join(" ");
            cm.replaceSelection(spaces);
          }}
        }});
        editor.on("change", function() {{
            textTosave = editor.getValue();
            document.getElementById("save").value = textTosave;
         }});
         
        document.getElementById("save").value = document.getElementById("code").value
    
    }});</script>    
  </body>
</html>
"""
