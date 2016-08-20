#!/usr/bin/python2

# SMS GW Frontend Class
import socket
import json

class smsgw:
    DEFAULT_PORT = 2525 # self.port must match the smsgwd port

    def __init__(self, host='localhost', port=DEFAULT_PORT):
        self.host = host
        self.PORT = port

    def send_sms(self, params):
        """Send a sms - actually submit the SMS to the queue and wait to get the status from sending the SMS

        params must be a dict that must contain the following:
        - params['priority'] (int)
        - params['gw'] (string containg one of: cheap, default, any, all, or one of the GWs in active list in smsgwd.cfg)
        - params['to'] (Recipient phone number, either national (no +) or international (starting with +))
        - params['msg'] (The message)

        Optional arguments (can always be specified)
        - params['from'] (From name, only some GW backends support that, eg. of type smsit.dk)
        - params['GetDeliveryReport'] (True/False, only used by GW of type gsmmodem)
        - params['verbose'] (0=no verbose, higher number => more verbose)
        """

        # Sanitate input
        # Priority must be 0 or a a positive integer
        if 'priority' in params:
            params['priority'] = int(params['priority'])
        else:
            params['priority'] = 10
        if params['priority'] < 0:
            params['priority'] = 0

        # Verbose must be 0 or a a positive integer
        if 'verbose' in params:
            try:
                params['verbose'] == int(params['verbose'])
            except:
                params['verbose'] == 0
        else:
            params['verbose'] = 0

        # GetDeliveryReport must be False or True if set
        if 'GetDeliveryReport' in params:
            if params['GetDeliveryReport'] == 'False':
                params['GetDeliveryReport'] == False
            elif params['GetDeliveryReport'] == 'True':
                params['GetDeliveryReport'] == True

        # create a socket object
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # connection to hostname on the PORT.
        s.connect((self.host, self.PORT))
        s.send(json.dumps(params))
        # Receive no more than 8192 bytes
        response = json.loads(s.recv(8192))
        s.close()
        return response
