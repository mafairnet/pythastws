PythAst WS 
=============

This tool is a webservice to make requests through AMI to Asterisk. This service handles all requests and queue all the into a Redis Database. This helps the asterisk perfomance and voice quality is not degradated. 

Prerequisites
-----------
-Linux 2.6 
-Redis
-Python 2.7
-Flask

Installation
-----------
Just copy all the files from the bin folder to /opt/pythastws/ to run your local copy of PythAstWS and set the file permissions.

```
wget https://github.com/mafairnet/pythastws/archive/master.zip
unzip master.zip
cd pythastws-master
mkdir /opt/pythastws/
cp -R bin/ /opt/pythastws
chmod +x pythast_worker.py
chmod +x pythast_engine.py
chmod +x pythast_webserver.py
```

**For USER/DEVICE mode in FreePBX add the content of the extensions_custom.conf file to your extensions_custom.conf.**

Usage
-----
Start Redis

```
redis-server --deamonize yes
```

Start your workers

```
/opt/pythastws/pythast_worker.py
```

Start your webservice

```
/opt/pythastws/pythast_webserver.py
```

Make a request on your browser

```
http://SERVERIP:88/command?cmd=exec&command=sip show peers
```

Start integrating you apps with the PythastWS =D