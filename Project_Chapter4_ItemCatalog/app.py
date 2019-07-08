#!/usr/bin/python3.6.8

#https://stackoverflow.com/questions/15231359/split-python-flask-app-into-multiple-files/15231623

from flask_httpauth import HTTPBasicAuth
from flask import session as login_session
from flask import Flask, render_template, request, redirect, jsonify, url_for, abort,make_response, g
from oauth2client.client import flow_from_clientsecrets, FlowExchangeError

from main import main_api
from oauth import oauth_api
from restful import rest_api

app = Flask(__name__)
app.register_blueprint(main_api)
app.register_blueprint(oauth_api)
app.register_blueprint(rest_api)

app.secret_key = b'WL9UNUqcNlpwJWCYl-_WHxPm'

if __name__ == '__main__':
   app.debug = True
   app.run(host='localhost', port=5000)
   #app.run(host='0.0.0.0', port=8000)

