#!/usr/bin/python
from flask import Flask, render_template, request
import socket
import time

from rq import Connection, Queue, get_current_job
from rq.job import Job
from redis import Redis

from pythast_engine  import generate_call,asterisk_command,queue_show_all,add_member,pause_member,unpause_member,remove_member

######### This part of the code defines the isntructions to initialize redis connection
redis_conn = Redis()
q = Queue(connection=redis_conn)

#increase this timeout if you have a lot of petitions
JOB_RESULT_TIMEOUT = 1

########## This part of the code handles petitions using a webserver 

app = Flask(__name__)

@app.route('/')
def index():
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
        response_received = False
        caller = request.args.get('caller')
        called = request.args.get('called')
        jobqueue = q.enqueue(generate_call,called,caller)
        while(response_received is False):
            time.sleep(JOB_RESULT_TIMEOUT)
            if jobqueue.result is not None:
                response_received = True
        return str(jobqueue.result)

    if cmd == "queueaddmember":
        response_received = False
        queue = request.args.get('queue')
        extension = request.args.get('extension')
        interface = "SIP/"+extension
        state_interface = "Local/"+extension+"@from-internal/n"
        member_name = "Local/"+extension+"@from-internal/n"
        jobqueue = q.enqueue(add_member,queue,interface,state_interface,member_name)
        while(response_received is False):
            time.sleep(JOB_RESULT_TIMEOUT)
            if jobqueue.result is not None:
                response_received = True
        return str(jobqueue.result)

    if cmd == "queueremovemember":
        response_received = False
        queue = request.args.get('queue')
        extension = request.args.get('extension')
        interface = "SIP/"+extension
        jobqueue = q.enqueue(remove_member,queue,interface)
        while(response_received is False):
            time.sleep(JOB_RESULT_TIMEOUT)
            if jobqueue.result is not None:
                response_received = True
        return str(jobqueue.result)

    if cmd == "queuepausemember":
        response_received = False
        queue = request.args.get('queue')
        extension = request.args.get('extension')
        interface = "SIP/"+extension
        jobqueue = q.enqueue(pause_member,queue,interface)
        while(response_received is False):
            time.sleep(JOB_RESULT_TIMEOUT)
            if jobqueue.result is not None:
                response_received = True
        return str(jobqueue.result)

    if cmd == "queueunpausemember":
        response_received = False
        queue = request.args.get('queue')
        extension = request.args.get('extension')
        interface = "SIP/"+extension
        jobqueue = q.enqueue(unpause_member,queue,interface)
        while(response_received is False):
            time.sleep(JOB_RESULT_TIMEOUT)
            if jobqueue.result is not None:
                response_received = True
        return str(jobqueue.result)

    if cmd == "queueshowall":
        response_received = False
        jobqueue = q.enqueue(queue_show_all)
        while(response_received is False):
            time.sleep(JOB_RESULT_TIMEOUT)
            if jobqueue.result is not None:
                response_received = True
        return str(jobqueue.result)

    if cmd == "exec":
        response_received = False
        command = request.args.get('command')
        jobqueue = q.enqueue(asterisk_command,command)
        while(response_received is False):
            time.sleep(JOB_RESULT_TIMEOUT)
            if jobqueue.result is not None:
                response_received = True
        return str(jobqueue.result)

    return render_template('response.html',response=response)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=88)