import socketserver

from pid import PidFile
from const import PUBLIC_URL
from server import *
from smarthome import *

use_ssl = ('use_ssl' in configuration and configuration['use_ssl'] == True)

if use_ssl:
    import ssl

if 'ngrok_tunnel' in configuration and configuration['ngrok_tunnel'] == True:
    from pyngrok import ngrok

tunnel = PUBLIC_URL

def secure(server):
    key  = configuration['ssl_key']  if 'ssl_key'  in configuration else None
    cert = configuration['ssl_cert'] if 'ssl_cert' in configuration else None

    if key is None or cert is None:
        logger.info('ssl_key and ssl_cert options are mandatory if use_ssl is True')
        return

    logger.info('Using SSL connection')
    server.socket = ssl.wrap_socket (server.socket, keyfile=key, certfile=cert, server_side=True, ssl_version=ssl.PROTOCOL_TLSv1_2)

class ThreadingSimpleServer(socketserver.ThreadingMixIn, http.server.HTTPServer):
    pass


def startServer():
    with PidFile('dzga') as p:
        print(p.piddir)
        global tunnel
        # Create tunnel if ngrok_tunnel set to true
        if 'ngrok_tunnel' in configuration and configuration['ngrok_tunnel'] is True:
            try:
                if 'ngrok_auth_token' in configuration and configuration['ngrok_auth_token'] != 'auth_token':
                    ngrok.set_auth_token(configuration['ngrok_auth_token'])
                else:
                    logger.info(
                        'If you use the ngrok tunnel option without account the tunnel will be terminated after 5 or 6 hours')
                public_url = ngrok.connect(configuration['port_number'])
                tunnel = public_url.replace("http", "https")
            except Exception as err:
                logger.error('Ngrok was unable to start. Error: %s is not valid' % err)
        try:
            # Create a web server and define the handler to manage the
            # incoming request
            server = ThreadingSimpleServer(('', configuration['port_number']), AogServer)
            if(use_ssl):
                secure(server)

            logger.info('========')
            logger.info('Started DZGA v%s server at port %s', VERSION, configuration['port_number'])
            logger.info(' ')
            if 'userinterface' in configuration and configuration['userinterface'] is True:
                protocol = 'https' if use_ssl else 'http'
                logger.info('   Visit %s://localhost:%d/settings to access the user interface', protocol, configuration['port_number'])
            else:
                logger.info('   Configure your settings in config.yaml in Domoticz-Google-Assistant folder')
            logger.info(' ')
            logger.info('=========')
            logger.info('Visit the Actions on Google console at http://console.actions.google.com')
            logger.info('Under Develop section, replace the fulfillment URL in Actions with:')
            logger.info('   %s/smarthome', tunnel)
            logger.info(' ')
            logger.info('In Account linking, set the Authorization URL to:')
            logger.info('   %s/oauth', tunnel)
            logger.info(' ')
            logger.info('Then set the Token URL to:')
            logger.info('   %s/token', tunnel)
            logger.info(' ')
            logger.info('Finally press \'SAVE\' and then \'TEST\' button')
            if 'ngrok_tunnel' in configuration and configuration['ngrok_tunnel'] is True:
                logger.info('** NOTE: Ngrok assigns random urls. When server restart the server gets a new url')
            logger.info('=======')
            print("(Press CTRL+C to stop server)")
            # Sync with domoticz at startup
            try:
                getDevices()
                getSettings()
            except (ValueError, Exception):
                logger.error('Error in  getting devices and settings')
                pass
            # Exit if running on travis
            istravis = os.environ.get('TRAVIS') == 'true'
            if istravis:
                logger.info('Travis test is finished')
                exit()
            # Wait forever for incoming http requests
            server.serve_forever()

        except (KeyboardInterrupt, SystemExit):
            print()
            logger.info('^C received, shutting down the web server')
            server.socket.close()


if __name__ == "__main__":
    # Execute only if run as a script

    for path, value in {**oauthGetMappings, **smarthomeGetMappings}.items():
        addGetMappings(path, value)

    for path, value in {**oauthPostMappings, **smarthomePostMappings}.items():
        addPostMappings(path, value)

    startServer()
