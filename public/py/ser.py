#!flask/bin/python

import sys

from flask import Flask, render_template, request, redirect, Response
import random, json

app = Flask(__name__)

@app.route('/')
def output():
	# serve index template
	#return render_template('index.html', name='Joe')
	return "<h1>hello</h1>"

@app.route('/receiver', methods = ['GET'])
def worker():
	# read json + reply
	ret_data = {"value": request.args.get('val')}
	print ret_data
	return "hello"

if __name__ == '__main__':
	# run!
	app.run(host='127.0.0.1', port=80)