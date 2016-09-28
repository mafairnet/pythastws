#!/usr/bin/python
from flask import Flask, render_template, request
import socket
import time

#########This part of the code defines the commands to control Asterisk

HOST="SERVERIP"
PORT=5038

p_generate_call = """Action: login
Events: off
Username: %(username)s
Secret: %(password)s

Action: originate
Channel: SIP/%(local_user)s
WaitTime: 60
CallerId: %(local_user)s
Exten: %(phone_to_dial)s
Context: default
Priority: 1

Action: Logoff
"""

p_queue_add_member = """Action: login
Events: off
Username: %(username)s
Secret: %(password)s

Action: QueueAdd
Queue: %(queue)s
Interface: %(interface)s
Penalty: 0
MemberName: %(member_name)s
StateInterface: %(state_interface)s
Paused: false

Action: Logoff
"""

p_queue_remove_member = """Action: login
Events: off
Username: %(username)s
Secret: %(password)s

Action: QueueRemove
Queue: %(queue)s
Interface: %(interface)s

Action: Logoff
"""

p_queue_pause_member = """Action: login
Events: off
Username: %(username)s
Secret: %(password)s

Action: QueuePause
Queue: %(queue)s
Interface: %(interface)s
Paused: true

Action: Logoff
"""

p_queue_unpause_member = """Action: login
Events: off
Username: %(username)s
Secret: %(password)s

Action: QueuePause
Queue: %(queue)s
Interface: %(interface)s
Paused: false

Action: Logoff
"""

p_queue_showall = """Action: login
Events: off
Username: %(username)s
Secret: %(password)s

Action: Queues





Action: Logoff
"""

p_command = """Action: login
Events: off
Username: %(username)s
Secret: %(password)s

Action: Command
Command: %(command)s

Action: Logoff
"""

def recv_timeout(the_socket,timeout=0.1):
    #make socket non blocking
    the_socket.setblocking(0)

    #total data partwise in an array
    total_data=[];
    data='';

    #beginning time
    begin=time.time()
    while 1:
        #if you got some data, then break after timeout
        if total_data and time.time()-begin > timeout:
            break

        #if you got no data at all, wait a little longer, twice the timeout
        elif time.time()-begin > timeout*2:
            break

        #recv something
        try:
            data = the_socket.recv(8192)
            if data:
                total_data.append(data)
                #change the beginning time for measurement
                begin=time.time()
            else:
                #sleep for sometime to indicate a gap
                time.sleep(0.1)
        except:
            pass

    #join all parts to make final string
    return ''.join(total_data)


def generate_call(phone_to_dial, username, password, local_user):
    pattern = p_generate_call % {
            'phone_to_dial': phone_to_dial,
            'username': username,
            'password': password,
            'local_user': local_user}

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((HOST, PORT))
    dataReceived = ""
    data = s.recv(1024)
    dataReceived = dataReceived + data
    for l in pattern.split('\n'):
        print "Sending&gt;", l
        s.send(l+'\r\n')
        if l == "":
            data = s.recv(1024)
	    dataReceived = dataReceived + data
            print data
    data = s.recv(1024)
    dataReceived = dataReceived + data
    s.close()
    return dataReceived

def add_member(username, password, queue, interface, state_interface, member_name):
    pattern = p_queue_add_member % {
            'username': username,
            'password': password,
            'queue': queue,
            'interface':interface,
            'state_interface':state_interface,
            'member_name':member_name
                }

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((HOST, PORT))

    dataReceived = ""
    data = s.recv(1024)
    dataReceived = dataReceived + data
    for l in pattern.split('\n'):
        print "Sending&gt;", l
        s.send(l+'\r\n')
        if l == "":
            data = s.recv(1024)
            dataReceived = dataReceived + data
            print data
    data = s.recv(1024)
    dataReceived = dataReceived + data
    s.close()
    return dataReceived

def remove_member(username, password, queue, interface):
    pattern = p_queue_remove_member % {
            'username': username,
            'password': password,
            'queue': queue,
            'interface':interface
                }

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((HOST, PORT))

    dataReceived = ""
    data = s.recv(1024)
    dataReceived = dataReceived + data
    for l in pattern.split('\n'):
        print "Sending&gt;", l
        s.send(l+'\r\n')
        if l == "":
            data = s.recv(1024)
            print data
	    dataReceived = dataReceived + data
    data = s.recv(1024)
    dataReceived = dataReceived + data
    s.close()
    return dataReceived

def pause_member(username, password, queue, interface):
    pattern = p_queue_pause_member % {
            'username': username,
            'password': password,
            'queue': queue,
            'interface':interface
                }

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((HOST, PORT))

    dataReceived = ""
    data = s.recv(1024)
    dataReceived = dataReceived + data
    for l in pattern.split('\n'):
        print "Sending&gt;", l
        s.send(l+'\r\n')
        if l == "":
            data = s.recv(1024)
	    dataReceived = dataReceived + data
            print data
    data = s.recv(1024)
    dataReceived = dataReceived + data
    s.close()
    return dataReceived

def unpause_member(username, password, queue, interface):
    pattern = p_queue_unpause_member % {
            'username': username,
            'password': password,
            'queue': queue,
            'interface':interface
                }

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((HOST, PORT))
    
    dataReceived = ""
    data = s.recv(1024)
    dataReceived = dataReceived + data
    for l in pattern.split('\n'):
        print "Sending&gt;", l
        s.send(l+'\r\n')
        if l == "":
            data = s.recv(1024)
	    dataReceived = dataReceived + data
            print data
    data = s.recv(1024)
    dataReceived = dataReceived + data
    s.close()
    return dataReceived

def queue_show_all(username, password):
    pattern = p_queue_showall % {
            'username': username,
            'password': password
                }

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((HOST, PORT))

    dataReceived = ""
    data = s.recv(1024)
    dataReceived = dataReceived + data
    for l in pattern.split('\n'):
        #print "L:[%s]" % l
        if l != "":
                print "Sending... ", l
        s.send(l+'\r\n')
        if l == "":
                data = s.recv(1024)
		dataReceived = dataReceived + data
                print data
    data = s.recv(1024)
    dataReceived = dataReceived + data
    s.close()
    return dataReceived

def asterisk_command(username, password, command):
    pattern = p_command % {
            'username': username,
            'password': password,
            'command': command
                }

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((HOST, PORT))
    dataReceived = ""
    for l in pattern.split('\n'):
        #print "L:[%s]" % l
        if l != "":
                print "Sending... ", l
        s.send(l+'\r\n')
        if l == "":
                data = recv_timeout(s)
		dataReceived = dataReceived + data
                print data
    s.close()
    return dataReceived


########## This part of the code handles petitions useing a webserver 

app = Flask(__name__)

@app.route('/')
def index():
    #command = request.args.get('command')
    #if command is None:
	#command = "Argument not provided"
    #print command
    #response = command
    #return render_template('index.html',response=response)
    return render_template('index.html')

@app.route('/monitor')
def monitor():
    return 'Asterisk Queues Monitor'

@app.route('/command')
def command():

    cmd = request.args.get('cmd')

    if cmd is None:
        cmd = "Argument not provided"
    print cmd

    response = ""

    if cmd == "originate":
	caller = request.args.get('caller')
	called = request.args.get('called')
	response = generate_call(phone_to_dial=called,username='USER', password='PASS',local_user=caller)

    if cmd == "queueaddmember":
	queue = request.args.get('queue')
	extension = request.args.get('extension')
	interface = "SIP/"+extension
	state_interface = "Local/"+extension+"@from-internal/n"
	member_name = "Local/"+extension+"@from-internal/n"
	response = add_member(username='USER', password='PASS', queue=queue, interface=interface, state_interface=state_interface, member_name=member_name)

    if cmd == "queueremovemember":
        queue = request.args.get('queue')
        extension = request.args.get('extension')
	interface = "SIP/"+extension
	response = remove_member(username='USER', password='PASS', queue=queue, interface=interface)

    if cmd == "queuepausemember":
        queue = request.args.get('queue')
        extension = request.args.get('extension')
        interface = "SIP/"+extension
        response = pause_member(username='USER', password='PASS', queue=queue, interface=interface)

    if cmd == "queueunpausemember":
        queue = request.args.get('queue')
        extension = request.args.get('extension')
        interface = "SIP/"+extension
        response = unpause_member(username='USER', password='PASS', queue=queue, interface=interface)

    if cmd == "queueshowall":
        response = queue_show_all(username='USER', password='PASS')

    if cmd == "exec":
	command = request.args.get('command')
        response = asterisk_command(username='USER', password='PASS',command=command)

    return render_template('response.html',response=response)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=88)
