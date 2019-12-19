# Domoticz-Google-Assistant

<img src="dzga_UI.png" alt="drawing" width="600"/>

Standalone implementation. It means that you can put this server wherever you want, even on another machine. You need to setup a project in Actions on Google Console. You find instructions below.

Based on Pawcio's script at [domoticz forum](https://www.domoticz.com/forum/viewtopic.php?f=69&t=27244)

Required:
- public url
- python >= 3.5
- Make local deployment available trough HTTPS with valid certificate:
  - Use ngrok for a secure SSL tunnel with valid public HTTPS URL
  - Configure reverse proxy with domain name and valid certificate using Lets Encrypt

Domoticz-Google-Assistant delivers: 
- The oauth authorization and smarthome endpoint for the google assistant.
- Two-factor authentication pin for domoticz protected devices. (works best with english language)
- Acknowledgement with Yes or No. (works best with english language)
- Arm Disarm Securitypanel. (works best with english language)
- On/Off, Brightness, Thermostat, Color Settings, speaker volume, Lock/Unlock, Scene and Open/Close.
- Stream surveillance camera to chromecast.
- Toggle Selector switches.
- Ngrok, instantly create a public HTTPS URL. Don't have to open any port on router and do not require a reverse proxy.

Please feel free to modify it, extend and improve

### [Installation and configuration](https://github.com/DewGew/Domoticz-Google-Assistant/wiki)
