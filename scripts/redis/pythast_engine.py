#!/usr/bin/python
import socket
import time

HOST="SERVERIP"
PORT=5038

p = """Action: login
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

def command(username, password, command):
    pattern = p_command % {
            'username': username,
            'password': password,
            'command': command
                }

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((HOST, PORT))

    for l in pattern.split('\n'):
        #print "L:[%s]" % l
        if l != "":
                print "Sending... ", l
        s.send(l+'\r\n')
        if l == "":
                data = recv_timeout(s)
                print data
    s.close()


def generate_call(phone_to_dial, username, password, local_user):
    pattern = p % {
            'phone_to_dial': phone_to_dial,
            'username': username,
            'password': password,
            'local_user': local_user}

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((HOST, PORT))

    data = s.recv(1024)
    for l in pattern.split('\n'):
        print "Sending&gt;", l
        s.send(l+'\r\n')
        if l == "":
            data = s.recv(1024)
            print data
    data = s.recv(1024)
    s.close()
