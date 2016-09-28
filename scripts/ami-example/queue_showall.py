#!/usr/bin/python
import socket

HOST="SERVERIP"
PORT=5038

p = """Action: login
Events: off
Username: %(username)s
Secret: %(password)s

Action: Queues





Action: Logoff
"""
def queue_show_all(username, password):
    pattern = p % {
            'username': username,
            'password': password
		}

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((HOST, PORT))

    data = s.recv(1024)
    for l in pattern.split('\n'):
	#print "L:[%s]" % l
       	if l != "":
		print "Sending... ", l
       	s.send(l+'\r\n')
       	if l == "":
		data = s.recv(1024)
       		print data
    data = s.recv(1024)
    s.close()

if __name__ == '__main__':
    queue_show_all(username='USER', password='PASS')
