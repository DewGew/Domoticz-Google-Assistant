# -*- coding: utf-8 -*-
                    
"""Constants for Google Assistant."""
VERSION = '1.8.8'
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

domains = {
    'ac_unit': 'AcUnit',
    'bathtub': 'Bathtub',
    'blinds': 'Blind',
    'blindsinv': 'BlindInverted',
    'camera': 'Camera',
    'coffeemaker': 'Coffeemaker',
    'color': 'ColorSwitch',
    'cooktop': 'Cooktop',
    'door': 'DoorSensor',
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
ATTRS_VACCUM_MODES = 1

DOMOTICZ_TO_GOOGLE_TYPES = {
    domains['ac_unit']: TYPE_AC_UNIT,
    domains['bathtub']: TYPE_BATHTUB,
    domains['blinds']: TYPE_BLINDS,
    domains['blindsinv']: TYPE_BLINDS,
    domains['camera']: TYPE_CAMERA,
    domains['coffemaker']: TYPE_COFFEE,
    domains['color']: TYPE_LIGHT,
    domains['cooktop']: TYPE_COOKTOP,
    domains['dishwasher']: TYPE_DISHWASHER,
    domains['door']: TYPE_DOOR,
    domains['dryer']: TYPE_DRYER,
    domains['fan']: TYPE_FAN,
    domains['garage']: TYPE_GARAGE,
    domains['gate']: TYPE_GATE,
    domains['group']: TYPE_SWITCH,
    domains['heater']: TYPE_HEATER,
    domains['kettle']: TYPE_KETTLE,
    domains['light']: TYPE_LIGHT,
    domains['lock']: TYPE_LOCK,
    domains['lockinv']: TYPE_LOCK,
    domains['media']: TYPE_MEDIA,
    domains['microwave']: TYPE_MICRO,
    domains['mower']: TYPE_MOWER,
    domains['outlet']: TYPE_OUTLET,
    domains['oven']: TYPE_OVEN,
    domains['push']: TYPE_SWITCH,
    domains['scene']: TYPE_SCENE,
    domains['screen']: TYPE_SCREEN,
    domains['security']: TYPE_SECURITY,
    domains['selector']: TYPE_SWITCH,
    domains['sensor']: TYPE_SENSOR,
    domains['smokedetektor']: TYPE_SMOKE_DETECTOR,
    domains['speaker']: TYPE_SPEAKER,
    domains['switch']: TYPE_SWITCH,
    domains['temperature']: TYPE_THERMOSTAT,
    domains['thermostat']: TYPE_THERMOSTAT,
    domains['vacuum']: TYPE_VACUUM,
    domains['valve']: TYPE_VALVE,
    domains['washer']: TYPE_WASHER,
    domains['waterheater']: TYPE_WATERHEATER,
    domains['window']: TYPE_WINDOW,
}

TEMPLATE = """
<!doctype html>
<html lang="en">
  <head>
    <title>Domoticz Google Assistant v""" + VERSION + """</title>
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
  </head>
  <body>
    <!-- Modal -->
    <div class="modal fade" id="messageModal" tabindex="-1" role="dialog" aria-labelledby="modalLabel" aria-hidden="true">
      <div class="modal-dialog" role="document">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title" id="modalLabel">Security Risk</h5>
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
    <!-- Navbar -->
    <nav class="navbar navbar-expand-lg navbar-dark bg-primary">
    <a class="navbar-brand" href="settings">
        <img src="https://upload.wikimedia.org/wikipedia/commons/5/5a/Google_Assistant_logo.png" width="30" height="30" class="d-inline-block align-top" alt="">
        Domoticz Google Assistant</a>
    <button class="navbar-toggler" type="button" data-toggle="collapse" data-target="#navbarNav" aria-controls="navbarNav" aria-expanded="false" aria-label="Toggle navigation">
    <span class="navbar-toggler-icon"></span>
    </button>
    <div class="collapse navbar-collapse" id="navbarNav">
    <ul class="nav nav-tabs bg-primary">
      <li class="nav-item" data-toggle="tooltip" data-placement="bottom" title="Home">
        <a data-toggle="tab" class="nav-link active" href="#home"><i class="material-icons">home</i></a>
      </li>
      <li class="nav-item" data-toggle="tooltip" data-placement="bottom" title="Devices">
        <a data-toggle="tab" class="nav-link" href="#menu1"><i class="material-icons">devices_other</i></a>
      </li>
      <li class="nav-item" data-toggle="tooltip" data-placement="bottom" title="Configuration">
        <a data-toggle="tab" class="nav-link" href="#menu2"><i class="material-icons">settings_ethernet</i></a>
      </li>
      <li class="nav-item" data-toggle="tooltip" data-placement="bottom" title="Help">
        <a data-toggle="tab" class="nav-link" href="#menu3"><i class="material-icons">help_outline</i></a>
      </li>
      <li class="nav-item" data-toggle="tooltip" data-placement="bottom" title="Log">
        <a data-toggle="tab" class="nav-link" href="#menu4"><i class="material-icons">notes</i></a>
      </li>
    </ul>
        <ul class="navbar-nav flex-row ml-md-auto d-none d-md-flex">
          <li class="nav-item" data-toggle="tooltip" data-placement="bottom" title="Dzga on GitHub">
          <a class="nav-link p-2" href="https://github.com/DewGew/Domoticz-Google-Assistant" target="_blank" rel="noopener" aria-label="GitHub">
          <svg xmlns="http://www.w3.org/2000/svg" x="0px" y="0px"
width="32" height="32"
viewBox="0 0 172 172"
style=" fill:#000000;"><g fill="none" fill-rule="none" stroke="none" stroke-width="1" stroke-linecap="butt" stroke-linejoin="miter" stroke-miterlimit="10" stroke-dasharray="" stroke-dashoffset="0" font-family="none" font-weight="none" font-size="none" text-anchor="none" style="mix-blend-mode: normal"><path d="M0,172v-172h172v172z" fill="none" fill-rule="nonzero"></path><g fill="#ffffff" fill-rule="evenodd"><path d="M86,21.5c-35.63037,0 -64.5,28.86963 -64.5,64.5c0,28.4917 18.47656,52.6792 44.11279,61.20361c3.2334,0.58789 4.40918,-1.38574 4.40918,-3.10742c0,-1.53271 -0.06299,-5.58496 -0.08398,-10.95996c-17.95166,3.88428 -21.73096,-8.65039 -21.73096,-8.65039c-2.93945,-7.45361 -7.15967,-9.44824 -7.15967,-9.44824c-5.85791,-3.98926 0.44092,-3.90528 0.44092,-3.90528c6.4668,0.46192 9.86817,6.63477 9.86817,6.63477c5.75293,9.86817 15.09619,7.0127 18.77051,5.375c0.58789,-4.17822 2.26758,-7.01269 4.09424,-8.62939c-14.31934,-1.6167 -29.37354,-7.15967 -29.37354,-31.87207c0,-7.05469 2.51953,-12.80761 6.63477,-17.32178c-0.65088,-1.6167 -2.87646,-8.18848 0.62989,-17.06982c0,0 5.41699,-1.72168 17.7417,6.61377c5.14404,-1.42773 10.66602,-2.1416 16.14599,-2.16259c5.47998,0.02099 11.00195,0.73486 16.14599,2.16259c12.32471,-8.33545 17.7207,-6.61377 17.7207,-6.61377c3.52734,8.88134 1.32276,15.45313 0.65088,17.06982c4.13623,4.51416 6.61377,10.26709 6.61377,17.32178c0,24.77539 -15.0752,30.21338 -29.43653,31.83008c2.30957,1.97364 4.36719,5.9209 4.36719,11.92578c0,8.6294 -0.06298,15.5791 -0.06298,17.69971c0,1.72168 1.15478,3.7373 4.43017,3.10742c25.61523,-8.54541 44.0708,-32.71192 44.0708,-61.20361c0,-35.63037 -28.86963,-64.5 -64.5,-64.5z"></path></g></g></svg>
          </a>
        </li>
        <li class="nav-item" data-toggle="tooltip" data-placement="bottom" title="Discord">
          <a class="nav-link p-2" href="https://discordapp.com/invite/AmJV6AC" target="_blank" rel="noopener" aria-label="Discord">
          <img src="https://discordapp.com/assets/28174a34e77bb5e5310ced9f95cb480b.png" height="32" width="32">
          </a>
        </li>
      </ul>
    </div>
    </nav>
    <!-- Container -->
    <div class="container">
    <div class="tab-content">
        <!-- Start page -->
        <div id="home" class="tab-pane fade show active" role="tabpanel">
            <div class="row">
              <div class="col-8">
                <p class="lead"><br>This project is based on Pawcio's script at <a href="https://www.domoticz.com/forum/viewtopic.php?f=69&amp;t=27244" target="_blank" rel="noopener" aria-label="Domoticz Forum">domoticz forum</a><br>
                <p class="lead text-info">Before you can use dzga. Setup Action on Google and configure settings in configuration.</p>
                <p class="lead">Domoticz-Google-Assistant delivers:<br />
                <ul class="text-muted">
                    <li>The oauth authorization and smarthome endpoint for the google assistant</li>
                    <li>Two-factor authentication pin for domoticz protected devices (limited language support)</li>
                    <li>Acknowledgement with Yes or No. (limited language support)</li>
                    <li>Arm Disarm Securitypanel (limited language support)</li>
                    <li>Supports Ngrok and SSL</li>
                    <li>Function to change device type, icon and some behavior depending on the device.</i></li>
                </ul>
                <p class="lead">Please feel free to modify, extend and improve it!</p>
                <p class="lead">
                <a href="https://github.com/DewGew/Domoticz-Google-Assistant/issues" target="_blank" rel="noopener" aria-label="Github Issues">
                <img alt="GitHub issues" src="https://img.shields.io/github/issues/DewGew/Domoticz-Google-Assistant?logo=github&style=for-the-badge">
                </a>
                <a href="https://discordapp.com/invite/AmJV6AC" target="_blank" rel="noopener" aria-label="Discord">
                <img alt="Discord" src="https://img.shields.io/discord/664815298284748830?label=Chat%20on%20discord&logo=discord&logoColor=white&style=for-the-badge">
                </a>
                </p>
              </div>
              <div class="col-4">
                <p>
                <form action="settings" method="post">
                    <button class="btn btn-raised btn-primary" name="restart" value="restart"><i class="material-icons" style="vertical-align: middle;">replay</i> Restart Server</button>
                    <button class="btn btn-raised btn-primary" name="sync" value="sync"><i class="material-icons" style="vertical-align: middle;">sync</i> Sync Devices</button>
                </form>
                <small class="text-muted">
                    <b>Quick start</b><br>
                    Visit the Actions on Google console at <a href="http://console.actions.google.com" target="_blank" rel="noopener" aria-label="Actions on Google">http://console.actions.google.com</a>.<br>Under Develop section, replace the fulfillment URL in Actions with:<br>
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
                <small class="text-muted"><b>DZGA Version:</b><br> """ + VERSION + """ {branch} <i class="text-muted; text-info" id="updates"></i><br>
                <b>Domoticz Version:</b><br> {dzversion}</small><br><br>
                
              </div>
              <div class="col" id="buttonUpdate"></div>
              <div class="col-4">
                <form action="https://www.paypal.me/dzga" target="_blank" rel="noopener" aria-label="Paypal">
                <button class="btn btn-raised btn-info" title="Sponsor with PayPal" alt="Sponsor with PayPal">
                <svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" aria-hidden="true" focusable="false" width="32" height="32" style="-ms-transform: rotate(360deg); -webkit-transform: rotate(360deg); transform: rotate(360deg); vertical-align: middle;" preserveAspectRatio="xMidYMid meet" viewBox="0 0 24 24"><path d="M8.32 21.97a.546.546 0 0 1-.26-.32c-.03-.15-.06.11.6-4.09c.6-3.8.59-3.74.67-3.85c.13-.17.11-.17 1.61-.18c1.32-.03 1.6-.03 2.19-.12c3.25-.45 5.26-2.36 5.96-5.66c.04-.22.08-.41.09-.41c0-.01.07.04.15.1c1.03.78 1.38 2.22.99 4.14c-.46 2.29-1.68 3.81-3.58 4.46c-.81.28-1.49.39-2.69.42c-.8.04-.82.04-1.05.19c-.17.17-.16.14-.55 2.55c-.27 1.7-.37 2.25-.41 2.35c-.07.16-.21.3-.37.38l-.11.07H10c-1.29 0-1.62 0-1.68-.03m-4.5-2.23c-.19-.1-.32-.27-.32-.47C3.5 19 6.11 2.68 6.18 2.5c.09-.18.32-.37.5-.44L6.83 2h3.53c3.91 0 3.76 0 4.64.2c2.62.55 3.82 2.3 3.37 4.93c-.5 2.93-1.98 4.67-4.5 5.3c-.87.21-1.48.27-3.14.27c-1.31 0-1.41.01-1.67.15c-.26.15-.47.42-.56.75c-.04.07-.27 1.47-.53 3.1a241.3 241.3 0 0 0-.47 3.02l-.03.06H5.69c-1.58 0-1.8 0-1.87-.04z" fill="#FFF"/><rect x="0" y="0" width="24" height="24" fill="rgba(0, 0, 0, 0)" /></svg>
                Sponsor DZGA</button>
                </form>
              </div>
            </div>
        </div>
        <div id="menu1" class="tab-pane fade" role="tabpanel">
            <br>
            <h5>Device list</h5>
            <small class="text-muted">List of devices the server recived from domoticz. Room and Nicknames is added from configuration. <b>Click on Header to sort asc or desc</b><br><b>NOTE:</b> If you don't see any device check your connection to domoticz.</small>
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
              <form action="settings" method="post">
                <button class="btn btn-raised btn-primary" name="save" id="save"><i class="material-icons" style="vertical-align: middle;">save</i> Save</button>
                <button class="btn btn-raised btn-primary" name="backup" value="backup"><i class="material-icons" style="vertical-align: middle;">save_alt</i> Backup Config</button>
                <button class="btn btn-raised btn-primary" name="restart" value="restart"><i class="material-icons" style="vertical-align: middle;">replay</i> Restart Server</button>
                </form>
                <p class="text-muted">Restart server to activate your changes</p>
              </div>
            </div>
        </div>
        <div id="menu3" class="tab-pane fade" role="tabpanel">
            </br>
            <h5>Help</h5> 
            <p>For help or more information about configuration and to setup Action on Google:</br>
            <a href="https://github.com/DewGew/Domoticz-Google-Assistant/wiki" target="_blank" rel="noopener">Domoticz Google Assistant wiki</a> or at 
            <a href="https://discordapp.com/invite/AmJV6AC" target="_blank" rel="noopener" aria-label="Discord">Discord</a></p>

            <h6>Manual update</h6>
            <p><kbd>bash &#60;(curl -s https://raw.githubusercontent.com/DewGew/dzga-installer/master/install.sh)</kbd></p>
        </div>
        <div id="menu4" class="tab-pane fade" role="tabpanel">
            <br>
            <h5 id="logsheader">Logs</h5>
            <textarea id="logs" rows="20" style="font-size: 10pt; width: 100%;">{logs}</textarea>
            <br>
            <div class="row">
              <div class="col">
              <form action="settings" method="post">
                <button class="btn btn-raised btn-primary" name="reload" value="reload"><i class="material-icons" style="vertical-align: middle;">sync</i> Reload logs</button>
                <button class="btn btn-raised btn-primary" name="deletelogs" value="deletelogs"><i class="material-icons" style="vertical-align: middle;">delete</i> Remove logs</button>
               </form>
              </div>
            </div>
        </div>
    </div>
    </div>

    <!-- Optional JavaScript -->
    <!-- jQuery first, then Popper.js, then Bootstrap JS -->
    <script src="https://code.jquery.com/jquery-3.1.1.min.js"></script>
    <script src="https://unpkg.com/popper.js@1.12.6/dist/umd/popper.js" integrity="sha384-fA23ZRQ3G/J53mElWqVJEGJzU0sTs+SvzG8fXVWP+kJQ1lwFAOkcUOysnlKJC33U" crossorigin="anonymous"></script>
    <script src="https://unpkg.com/bootstrap-material-design@4.1.1/dist/js/bootstrap-material-design.js" integrity="sha384-CauSuKpEqAFajSpkdjv3z9t8E7RlpJ1UP0lKM/+NdtSarroVKu069AlsRPKkFBz9" crossorigin="anonymous"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/codemirror/5.48.4/codemirror.js"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/codemirror/5.48.4/mode/yaml/yaml.js"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/codemirror/5.48.4/mode/javascript/javascript.min.js"></script>
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

    var urlToGetAllOpenBugs = "https://api.github.com/repos/DewGew/Domoticz-Google-Assistant/issues?state=open";

    $(document).ready(function() {{
        var config = {conf}
        var updates = {update}
        document.getElementById("logsheader").innerHTML = 'Logs <br><small class="text-muted">Loglevel: ' + config.loglevel + '</small>';
        if (updates) {{
          document.getElementById("updates").innerHTML = "(Updates are Availible)";
          // document.getElementById("modalLabel").innerHTML = "Updates are Availible!";
          // document.getElementById("message").innerHTML = '<p>Updates are Availible. Just press update button to get latest Dzga version.</p><p><center><form action="/settings" method="post"><button class="btn btn-raised btn-primary" name="update" value="update"><i class="material-icons" style="vertical-align: middle;">update</i> Update</button></form></center></p>';
          // $('#messageModal').modal('show')
          $('#buttonUpdate').append('<br><form action="/settings" method="post"><button class="btn btn-raised btn-primary" name="update" value="update"><i class="material-icons" style="vertical-align: middle;">update</i> Update dzga</button></form>');
        }};

        $('body').bootstrapMaterialDesign();
        $(function () {{
          $('[data-toggle="tooltip"]').tooltip()
        }});

        if (config.auth_user == 'admin' || config.auth_pass == 'admin'){{
            $('#messageModal').modal('show')
        }};
        message = '{message}'
        if (message != '') {{
            document.getElementById("modalLabel").innerHTML = "Information!";
            document.getElementById("message").innerHTML = message;
            $('#messageModal').modal('show')
        }};

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

        }};
        if (typeof x !== "undefined"){{
            $('#deviceList_idx').append(x.replace('undefined',''));
        }}else{{
            document.getElementById("modalLabel").innerHTML = "Check configuration.";
            document.getElementById("message").innerHTML = "Connection to Domoticz refused! Check configuration.";
            $('#messageModal').modal('show')
        }};

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
        var logs = CodeMirror.fromTextArea(document.getElementById("logs"), {{
            lineNumbers: false,
            mode: "javascript",
            autoRefresh:true
        }});
        logs.setOption("extraKeys", {{
          Tab: function(cm) {{
            var spaces = Array(cm.getOption("indentUnit") + 1).join(" ");
            cm.replaceSelection(spaces);
          }}
        }});

        document.getElementById("save").value = document.getElementById("code").value

    }});</script>
  </body>
</html>
"""
