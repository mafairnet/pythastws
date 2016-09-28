#!/usr/bin/python
import socket

HOST="SERVERIP"
PORT=5038

p = """Action: login
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
def add_member(username, password, queue, interface, state_interface, member_name):
    pattern = p % {
            'username': username,
            'password': password,
            'queue': queue,
            'interface':interface,
	    'state_interface':state_interface,
            'member_name':member_name
		}

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

if __name__ == '__main__':
    add_member(username='USER', password='PASS', queue='20008', interface='SIP/10031', state_interface='Local/10031@from-internal/n', member_name='Local/10031@from-internal/n')
