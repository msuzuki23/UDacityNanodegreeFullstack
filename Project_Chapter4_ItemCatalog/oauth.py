#!/usr/bin/python3.6.8
# This module contains all the oauth
# authentication routes for both
# Google and Facebook

import json
import random
import string
import requests
import httplib2
import psycopg2 as pg
from user import getUserID, getUserInfo, createUser
from databaseSetup import Base, Company, Cars, User
from sqlalchemy.ext.declarative import declarative_base
from oauth2client.client import FlowExchangeError
from oauth2client.client import flow_from_clientsecrets
from flask_httpauth import HTTPBasicAuth
from flask import session as login_session
from flask import Flask, render_template, request
from flask import redirect, jsonify, url_for, abort
from flask import g, make_response, flash, Blueprint

# Create oauth_api blueprint
oauth_api = Blueprint('oauth_api', __name__)

# Google client secret
CLIENT_ID = json.loads(open('client_secrets.json',
                            'r').read())['web']['client_id']


# Google Authentication
@oauth_api.route('/gconnect', methods=['POST'])
def gconnect():
    """Authenticate user using Google"""

    # Validate state token
    if request.args.get('state') != login_session['state']:
        response = make_response(json.dumps('Invalid state parameter.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    # Obtain authorization code
    code = request.data
    try:
        # Upgrade the authorization code into a credentials object
        oauth_flow = flow_from_clientsecrets('client_secrets.json', scope='')
        oauth_flow.redirect_uri = 'postmessage'
        credentials = oauth_flow.step2_exchange(code)
    except FlowExchangeError:
        response = make_response(
            json.dumps('Failed to upgrade the authorization code.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    # Check that the access token is valid.
    access_token = credentials.access_token
    url = ("https://www.googleapis.com/oauth2/"+\
            "v1/tokeninfo?access_token=%s" % access_token)
    h = httplib2.Http()
    result = json.loads(h.request(url, 'GET')[1])
    # If there was an error in the access token info, abort.
    if result.get('error') is not None:
        response = make_response(json.dumps(result.get('error')), 500)
        response.headers['Content-Type'] = 'application/json'
        return response
    # Verify that the access token is used for the intended user.
    gplus_id = credentials.id_token['sub']
    if result['user_id'] != gplus_id:
        response = make_response(json.dumps(
                                            "Token's user ID doesn't match given user ID."
                                            ), 401
                                )
        response.headers['Content-Type'] = 'application/json'
        return response
    # Verify that the access token is valid for this app.
    if result['issued_to'] != CLIENT_ID:
        response = make_response(
            json.dumps("Token's client ID does not match app's."), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    stored_access_token = login_session.get('access_token')
    stored_gplus_id = login_session.get('gplus_id')
    if stored_access_token is not None and gplus_id == stored_gplus_id:
        response = make_response(json.dumps(
                                            'Current user is already connected.'
                                            ), 200
                                )
        response.headers['Content-Type'] = 'application/json'
        return response
    # Store the access token in the session for later use.
    login_session['provider'] = 'google'
    login_session['access_token'] = credentials.access_token
    login_session['gplus_id'] = gplus_id
    # Get user info
    userinfo_url = "https://www.googleapis.com/oauth2/v1/userinfo"
    params = {'access_token': credentials.access_token, 'alt': 'json'}
    answer = requests.get(userinfo_url, params=params)
    data = answer.json()
    login_session['username'] = data['name']
    login_session['picture'] = data['picture']
    login_session['email'] = data['email']

    # see if user exists, if it doesn't make a new one
    user_id = getUserID(login_session['email'])
    if not user_id:
        user_id = createUser(login_session)
    login_session['user_id'] = user_id
    output = ''
    output += '<div class="container text-center">'+\
                '<div class="row justify-content-md-center">'+\
                    '<div class="col-md-8 border p-1 m-1"><pclass="m-1">Welcome, '
    output += login_session['username']
    output += '!</p>'
    output += '<div class="d-flex justify-content-center m-1">'+\
                '<img class="rounded mx-auto d-block" '+\
                    'width="30%" src="'
    output += login_session['picture']
    output += '"></div></div></div></div>'
    return output


# Google DISCONNECT - Revoke a current
# user's token and reset their login_session
@oauth_api.route('/gdisconnect')
def gdisconnect():
    """Disconnect user using Google"""

    access_token = login_session.get('access_token')
    if access_token is None:
        response = make_response(json.dumps(
                                            'Current user not connected.'
                                            ), 401
                                )
        response.headers['Content-Type'] = 'application/json'
        return response
    url = 'https://accounts.google.com/o/oauth2/revoke?token=%s'\
             % login_session['access_token']
    h = httplib2.Http()
    result = h.request(url, 'GET')[0]
    if result['status'] == '200':
        del login_session['access_token']
        del login_session['gplus_id']
        # del login_session['username']
        # del login_session['email']
        # del login_session['picture']
        response = make_response(json.dumps('Successfully disconnected.'), 200)
        response.headers['Content-Type'] = 'application/json'
        return response
    else:
        response = make_response(json.dumps(
                                            'Failed to revoke token for given user.', 400
                                            )
                                )
        response.headers['Content-Type'] = 'application/json'
    return response


# Facebook DISCONNECT
@oauth_api.route('/fbdisconnect')
def fbdisconnect():
    """Disconnect user using Facebook"""

    facebook_id = login_session['facebook_id']
    url = 'https://graph.facebook.com/%s/permissions' % facebook_id
    h = httplib2.Http()
    result = h.request(url, 'DELETE')[1]
    del login_session['facebook_id']
    return "you have been logged out"


# Facebook connect/authenticate
@oauth_api.route('/fbconnect', methods=['POST'])
def fbconnect():
    """Authenticate user using Facebook"""

    if request.args.get('state') != login_session['state']:
        response = make_response(json.dumps('Invalid state parameter.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    access_token = request.data
    access_token = access_token.decode("utf-8")
    # Exchange client token for long-lived server-side token with GET 
    # /oauth/access_toke?grant_type=fb_exchange_token&client_id={app-id}&
    # client_secret={app-secret}&fb_exchange_token={short-lived-token}
    app_id = json.loads(open('fb_client_secrets.json','r').read())['web']['app_id']
    app_secret = json.loads(open('fb_client_secrets.json','r').read())['web']['app_secret']
    url = "https://graph.facebook.com/oauth/access_token?grant_type="+\
            "fb_exchange_token&client_id=%s&client_secret=%s&fb_exchange_token=%s"\
            % (app_id, app_secret, access_token)
    h = httplib2.Http()
    result = h.request(url, 'GET')[1]
    result_string = result.decode("utf-8")
    # Use token to get user info from API
    userinfo_url = "https://graph.facebook.com/v3.2/me"
    # Strip expire tag from access token
    token = result_string.split(',')[0].split(':')[1].replace('"', '')
    url = "https://graph.facebook.com/v3.2/"+\
            "me?access_token=%s&fields=name,id,email" % token
    h = httplib2.Http()
    result = h.request(url, 'GET')[1]
    result_string = result.decode("utf-8")
    data = json.loads(result_string)
    login_session['provider'] = 'facebook'
    login_session['username'] = data["name"]
    login_session['email'] = data["email"]
    login_session['facebook_id'] = data["id"]
    # Get user picture
    url = "https://graph.facebook.com/v3.3/"+\
            "me?access_token=%s&fields=picture" % token
    h = httplib2.Http()
    result = h.request(url, 'GET')[1]
    data = json.loads(result)
    login_session['picture'] = data["picture"]["data"]["url"]
    # See if user exists
    user_id = getUserID(login_session['email'])
    if not user_id:
        user_id = createUser(login_session)
    login_session['user_id'] = user_id
    output = ''
    output += '<div class="container text-center">'+\
                '<div class="row justify-content-md-center">'+\
                    '<div class="col-md-8 border p-1 m-1">'+\
                        '<pclass="m-1">Welcome, '
    output += login_session['username']
    output += '!</p>'
    output += '<div class="d-flex justify-content-center m-1">'+\
                '<img class="rounded mx-auto d-block" width="30%" src="'
    output += login_session['picture']
    output += '"></div></div></div></div>'
    return output


# Authentication disconnection
# common functionalities
@oauth_api.route('/disconnect')
def disconnect():
    """Disconnect common functionalities"""

    # Check providers
    if 'provider' in login_session:
        if login_session['provider'] == 'facebook':
            fbdisconnect()
            # del login_session['facebook_id']
        elif login_session['provider'] == 'google':
            gdisconnect()
        del login_session['username']
        del login_session['email']
        del login_session['picture']
        del login_session['user_id']
        del login_session['provider']
        flash("You have succesfully logged out.")
        return redirect(url_for('main_api.show'))