import os
import sys
from pathlib import Path
from pyngrok import ngrok
import socketserver
from server import *
from auth import *
from smarthome import *
from const import configuration, VERSION, PUBLIC_URL

tunnel = PUBLIC_URL
class ThreadingSimpleServer(socketserver.ThreadingMixIn, http.server.HTTPServer):
    pass
    
def requestDevicesSync():
    SmartHomeReqHandler.forceDevicesSync()
    
def startServer():
    global tunnel
    try:
        #Create a web server and define the handler to manage the
        #incoming request
        server = ThreadingSimpleServer(('', configuration['port_number']), AogServer)
        print ()
        print ('Started DZGA v' + VERSION + ' server at port ' + str(configuration['port_number']))
        print ()
        print ('   Visit http://localhost:' + str(configuration['port_number']) + '/settings to access the user inteface')
        print ()
        if 'ngrok_tunnel' in configuration and configuration['ngrok_tunnel']:
            try:
                public_url = ngrok.connect(configuration['port_number'])
                tunnel = public_url.replace("http", "https")
            except Exception as e:
                print ('Ngrok was unable to start')
                print (e)
                
        print ('=====')
        print ('Visit the Actions on Google console at http://console.actions.google.com')
        print ('Under Develop section, replace the fulfillment URL in Actions with:')
        print ('   ' + tunnel + '/smarthome')
        print ()
        print ('In Account linking, set the Authorization URL to:')
        print ('  ' + tunnel + '/oauth')
        print ()
        print ('Then set the Token URL to:')
        print ('  ' + tunnel + '/token')
        print ()
        print ('Finally press \'SAVE\' and then \'TEST\' button')
        if 'ngrok_tunnel' in configuration and configuration['ngrok_tunnel']:
            print ('** NOTE: Ngrok assigns random urls. When server restart the server gets a new url')
        print ()
        #Wait forever for incoming http requests
        server.serve_forever()

    except (KeyboardInterrupt, SystemExit):
        print()
        print ('^C received, shutting down the web server')
        server.socket.close()

if __name__ == "__main__":
    # execute only if run as a script

    for path,value in {**oauthGetMappings, **smarthomeGetMappings}.items():
        addGetMappings(path, value)
    
    for path,value in {**oauthPostMappings, **smarthomePostMappings}.items():
        addPostMappings(path, value)
        
    startServer()
