#!/usr/bin/python
import socket

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

if __name__ == '__main__':
    #generate_call(phone_to_dial='10031',username='USER', password='PASS',local_user='10030')
    generate_call(phone_to_dial='200',username='USER', password='PASS',local_user='201')
