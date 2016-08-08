smsgw - A SMS GW controller for multiple backends and frontends
===============================================================

The smsgw can send SMS'es via multiple backends:
* gsmmodem: python-gsmmodem (https://github.com/faucamp/python-gsmmodem or https://github.com/bennyslbs/python-gsmmodem)
* smsit.dk: A Danish SMS GW
* eu.apksoft.android.smsgateway: An Android App for sending and receiving SMS'es

There can be multiple GW backends of each type.

It requires python-gsmmodem (even if such a GW backend isn't used), sorry.

It works on linux (tested on Raspberry Pi).

Security
--------

The smsgw client(s) and the smsgwd communicates non-encrypted over a socket interface, and there are no password protection of any kind!

If needed to use over a unsecure network, pleace encapsulate the traffic in a tunnel.

Usage
-----
* Fetch and install python-gsmmodem
* Fetch smsgw
* Create a config file for the server, example below
* Start the server, `smsgwd` (-h for help)
* Send SMS via client, `smsgw` (either command line interface or a python class)

Examples on sending a SMS
-------------------------

Send a SMS:
* `-p 0`: Highest priority (0)
* `-f 'Me'`: From Me - some network SMS Gateways allows to use a string as the sender, check with your GW provider (only smsit.dk supports that)
* `-t +451234`: To phone number, national (starting with +) or international number
* `-m Hello`: Message: Hello
* `-g cheap`: Which gateway to use, either:
.* cheap:   The one marked as cheap in server config file
.* default: The one marked as default in server config file
.* any:     Use any GW in active list in server config file, continue until ok(exit code 0)
.* all:     Use all GW in active list in server config file
.* One of the gatways in the active list in server config file
* `-r`      Request delivery report (only some GW backends support that (gsmmodem have propably the best support)
. or `-R`   Don't request delivery report

Example command:

    smsgw -p 0 -f 'Me' -t +451234 -m 'Hello' -g cheap -r

Note: chaining port must be done in both server (config file) and
client (argument), the client can be executed on another host than the
server depending on host entry in config file.

Incomming SMS'es
----------------
* gsmmodem can receive SMS'es, at the moment they are printed on STDOUT of smsgwd, this could be changed to forward to mail
.* Not concatenated mails are not concatenated
* Using smsit.dk does not support incomming SMS'es (in their cheapest plan) - Nothing to do for the smsgwd
* Using eu.apksoft.android.smsgateway can forward SMSes to a mail account - Nothing to do for the smsgwd (also possible to access url)

Config example
--------------

Default location: `/etc/smsgwd.cfg`

    [socketCfg]
    # Empty string => Any host
    # Field is socket host format, e.g accepting localhost, server name, IP
    # Special: If gethostname() then it is replaced by output from python socket.gethostname()
    host = 
    port = 2525
    
    [GWs]
    # List of active SMS GWs, NoSmsGw is a special GW actually not sending any SMS's
    active = ["NoSmsGw", "MySim", "smsit.dk"]
    
    # The cheapest active GW (except NoSmsGw)
    cheap = MySim
    
    # Defualt active GW to use
    default = %(cheap)s
    
    # Supported types for SMS GWs:
    # - NoSmsGw (No SMS's are sent)
    #   - Needed parameters: None
    # - gsmmodem (Sending via gsmmodem from https://github.com/faucamp/python-gsmmodem/)
    #   - Needed parameters:
    #     - tty, e.g. tty=/dev/ttyUSB0
    #     - baud, baudrate, e.g. 115200
    #     - pin, either 4 digit pin or None
    #     - GetDeliveryReport=True or False
    # - smsit.dk
    #   - Needed parameters:
    #     - key=abcdef1234
    #     - default_from = SmsGW (Only used if no from is speicified by smsgw client)
    # - eu.apksoft.android.smsgateway
    #   See https://play.google.com/store/apps/details?id=eu.apksoft.android.smsgateway
    #   - Needed parameters:
    #     - key=<password> (not tested without)
    
    [smsgw-NoSmsGw]
    type = NoSmsGw
    
    [smsgw-MySim]
    type = gsmmodem
    tty  = /dev/ttyUSB0
    baud = 115200
    # Set pin to number or None if no pincode
    pin  = None
    pin  = 1234
    # Can be overrided by client via flag GetDeliveryReport
    GetDeliveryReport = True
    
    [smsgw-smsit.dk]
    type = smsit.dk
    key  = y0urKeyFromSmsit
    url  = dummy
    # default_from is the sender of the message, used if client don't specify From
    default_from = SmsGW
    
    [smsgw-app]
    type = eu.apksoft.android.smsgateway
    url	 = http://192.168.0.2:9090/sendsms
    key  = AppPassword

Add to systemd service system
-----------------------------

Do the following steps:
* Create system user for the gw daemon (with limited access)
* Add the user to group dialout
* Copy service script from init.d/smsgw
* Create logfile and let the smsgw user be the owner
* Mention that service script smsgw have been updated
* Start the script

The following code does that stuff:

    cp -p <smsgw>/init.d/smsgw /etc/init.d/smsgw
    # I needed the user to use bash to flush output to logfile line by line
    sudo useradd -s /bin/bash -r -M smsgw
    sudo usermod -a -G dialout smsgw
    sudo chown root:root /etc/init.d/smsgw
    sudo touch /var/log/smsgw.log
    sudo chown smsgw /var/log/smsgw.log
    sudo update-rc.d smsgw defaults
    sudo service smsgw start
