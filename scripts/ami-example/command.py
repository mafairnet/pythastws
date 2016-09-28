#!/usr/bin/python
import socket

HOST="SERVERIP"
PORT=5038

p = """Action: login
Events: off
Username: %(username)s
Secret: %(password)s

Action: Command
Command: %(command)s

Action: Logoff
"""
def command(username, password, command):
    pattern = p % {
            'username': username,
            'password': password,
            'command': command
		}

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((HOST, PORT))

    data = s.recv(4096)
    for l in pattern.split('\n'):
	#print "L:[%s]" % l
       	if l != "":
		print "Sending... ", l
       	s.send(l+'\r\n')
       	if l == "":
		data = s.recv(4096)
       		print data
    data = s.recv(4096)
    s.close()

if __name__ == '__main__':
    command(username='USER', password='PASS', command='core show hints')
