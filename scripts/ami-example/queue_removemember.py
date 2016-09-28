#!/usr/bin/python
import socket

HOST="SERVERIP"
PORT=5038

p = """Action: login
Events: off
Username: %(username)s
Secret: %(password)s

Action: QueueRemove
Queue: %(queue)s
Interface: %(interface)s

Action: Logoff
"""
def remove_member(username, password, queue, interface):
    pattern = p % {
            'username': username,
            'password': password,
            'queue': queue,
            'interface':interface
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
    remove_member(username='USER', password='PASS', queue='20008', interface='SIP/10031')
