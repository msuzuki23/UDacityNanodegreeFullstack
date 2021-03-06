# !/usr/bin/python3.6.8
# This module is the entry point
# to the application

from flask_httpauth import HTTPBasicAuth
from flask import session as login_session
from flask import Flask, render_template, request, redirect
from flask import jsonify, url_for, abort, make_response, g
from oauth2client.client import flow_from_clientsecrets, FlowExchangeError
from main import main_api
from oauth import oauth_api
from restful import rest_api

# App Flask
app = Flask(__name__)

# Register blueprints
app.register_blueprint(main_api)
app.register_blueprint(oauth_api)
app.register_blueprint(rest_api)

# Application secret key
app.secret_key = b'WL9UNUqcNlpwJWCYl-_WHxPm'

# Main body
if __name__ == '__main__':
  app.debug = True
  app.run(host='localhost', port=5000)