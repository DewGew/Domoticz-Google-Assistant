import os
import sys
from pathlib import Path
from pyngrok import ngrok
import socketserver
from server import *
from auth import *
from smarthome import *
from const import configuration

tunnel = ''
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
        print ('Started DZGA server at port ' + str(configuration['port_number']))
        print ()
        print ('   Visit http://localhost:' + str(configuration['port_number']) + '/settings to access the user inteface')
        print ()
        if 'ngrok_tunnel' in configuration and configuration['ngrok_tunnel']:
            try:
                public_url = ngrok.connect(configuration['port_number'])
                tunnel = public_url.replace("http", "https")
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
                print ('** NOTE: Ngrok assigns random urls. When server restart the server gets a new url')
                print ()
            except Exception as e:
                print ('Ngrok was unable to start')
                print (e)
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
