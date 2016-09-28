#!/usr/bin/python
from flask import Flask, render_template, request

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
    data = request.args.get('data')
    if cmd is None:
        cmd = "Argument not provided"
    print cmd
    response = cmd + data
    return response

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=88)
