import os
from pathlib import Path
import socketserver
from server import *
from auth import *
from smarthome import *
from const import configuration

class ThreadingSimpleServer(socketserver.ThreadingMixIn, http.server.HTTPServer):
    pass
    
def requestDevicesSync():
    SmartHomeReqHandler.forceDevicesSync()
    
def startServer():
    try:
        #Create a web server and define the handler to manage the
        #incoming request
        server = ThreadingSimpleServer(('', configuration['port_number']), AogServer)
        print ('Started httpserver on port ' , configuration['port_number'])

        #Wait forever for incoming htto requests
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
