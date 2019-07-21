#!/usr/bin/python3.6.8

# CURL COMMAND:
# curl -u lily:lily -i -X GET http://localhost:5000/protected_resource

# To get an Authentication Token:
# curl -u lily:lily -i -X GET http://localhost:5000/token

import os
import json
import requests
import httplib2
from flask_httpauth import HTTPBasicAuth
from sqlalchemy import create_engine
from sqlalchemy.orm import relationship, sessionmaker
from flask import Flask, render_template, request, redirect
from flask import jsonify, url_for, abort, g, Blueprint, make_response
from oauth2client.client import FlowExchangeError, flow_from_clientsecrets
from databaseSetup import Base, Company, Cars, User

dbUser = os.environ.get('POSTGRES_USER')
dbPW = os.environ.get('POSTGRES_PW')
engine = create_engine('postgresql+psycopg2://'+dbUser+':'+dbPW+'@localhost/postgres')

Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()

auth = HTTPBasicAuth()
CLIENT_ID = json.loads(open('client_secrets.json',
                            'r').read())['web']['client_id']

rest_api = Blueprint('rest_api', __name__)


############################################################
# OAuth Authentication and OAuth Token Generation
# App Token Generation
@auth.verify_password
def verify_password(username_or_token, password):
    # Try to see if it's a token first
    user_id = User.verify_auth_token(username_or_token)
    if user_id:
        user = session.query(User).filter_by(user_id=user_id).one()
    else:
        user = session.query(User).filter_by(
                                            user_name=username_or_token
                                            ).first()
        if not user or not user.verify_password(password):
            return False
    g.user = user
    return True


@rest_api.route('/token')
@auth.login_required
def get_auth_token():
    token = g.user.generate_auth_token()
    return jsonify({'token': token.decode('ascii')})


@rest_api.route('/users', methods=['GET', 'POST'])
def new_user():
    if request.method == 'POST':
        username = request.args.get('username')
        user_email = request.args.get('email')
        password = request.args.get('password')
        if username is None or password is None:
            abort(400)  # missing arguments(
        user = User(user_name=username)
        user.user_email = user_email
        user.hash_password(password)
        session.add(user)
        session.commit()
        return jsonify({'username': user.user_name}), 201


@rest_api.route('/clientOAuth')
def start():
    return render_template('clientOAuth.html')

# @rest_api.route('/protected_resource')
# @auth.login_required
# def get_resource():
#     return jsonify({ 'data': 'Hello, %s!' % g.user.user_name})


@rest_api.route('/oauth/<provider>', methods=['POST'])
def login(provider):
    # Parse the auth code
    auth_code = request.args.get('auth_code')
    # print("Received auth code %s" % auth_code)
    if provider == 'google':
        # Exchange for a token
        try:
            # Upgrade the authorization code into a credentials object
            oauth_flow = flow_from_clientsecrets(
                                                'client_secrets.json', scope=''
                                                )
            oauth_flow.redirect_uri = 'postmessage'
            credentials = oauth_flow.step2_exchange(auth_code)
        except FlowExchangeError:
            response = make_response(json.dumps(
                                                'Failed to ugrade the authorization code.'
                                                ), 401)
            response.headers['Content-Type'] = 'application/json'
            return response
        # Check that the access token is valid.
        access_token = credentials.access_token
        url = ('https://www.googleapis.com/oauth2/v1/tokeninfo?access_token=%s'\
               % access_token)
        h = httplib2.Http()
        result = json.loads(h.request(url, 'GET')[1])
        # If there was an error in the access token info, abort.
        if result.get('error') is not None:
            response = make_response(json.dumps(result.get('error')), 500)
            response.headers['Content-Type'] = 'application/json'
        print("Step 2 Complete! Access Token: %s " % credentials.access_token)
        # Get user info
        h = httplib2.Http()
        userinfo_url = "https://www.googleapis.com/oauth2/v1/userinfo"
        params = {'access_token': credentials.access_token, 'alt': 'json'}
        answer = requests.get(userinfo_url, params=params)
        data = answer.json()
        name = data['name']
        picture = data['picture']
        email = data['email']
    # FACEBOOK REST API
    elif provider == 'facebook':
        # Exchange client token for long-lived server-side token with 
        # GET /oauth/access_toke?grant_type=fb_exchange_token&client_id={app-id}&
        # client_secret={app-secret}&fb_exchange_token={short-lived-token}
        app_id = json.loads(open('fb_client_secrets.json', 
                            'r').read())['web']['app_id']
        app_secret = json.loads(open('fb_client_secrets.json',
                                'r').read())['web']['app_secret']
        # print("access token type: %s" % type(auth_code))
        url = """https://graph.facebook.com/oauth/access_token?grant_type=
                fb_exchange_token&client_id=%s&client_secret=%s&fb_exchange_token=%s"""\
                 % (app_id, app_secret, auth_code)   # access_token
        h = httplib2.Http()
        result = h.request(url, 'GET')[1]
        # print("r %s" % type(result))
        result_string = result.decode("utf-8")
        # Use token to get user info from API
        userinfo_url = "https://graph.facebook.com/v3.2/me"
        # Strip expire tag from access token
        token = result_string.split(',')[0].split(':')[1].replace('"', '')
        # print("result: "+result_string)
        # print("token"+token)
        url = """https://graph.facebook.com/v3.2/me?access_token=
                %s&fields=name,id,email""" % token
        h = httplib2.Http()
        result = h.request(url, 'GET')[1]
        # print "url sent fro API access:%s" %url
        # print "API JSON result: %s" %result
        result_string = result.decode("utf-8")
        data = json.loads(result_string)
        # print(data)
        # login_session['provider'] = 'facebook'
        name = data["name"]
        email = data["email"]
        facebook_id = data["id"]
        # Get user picture
        url = """https://graph.facebook.com/v3.3/
                me?access_token=%s&fields=picture""" % token
        h = httplib2.Http()
        result = h.request(url, 'GET')[1]
        data = json.loads(result)
        picture = data["picture"]["data"]["url"]
    else:
        return 'Unrecognized Provider'
    # See if User exists, if it doesn't make a new one
    user = session.query(User).filter_by(user_email=email).first()
    if not user:
        user = User(
                    user_name=name,
                    user_picture=picture,
                    user_email=email
                    )
        session.add(user)
        session.commit()
    # Make token
    token = user.generate_auth_token(600)
    # Send back token to the client'
    return jsonify({'token': token.decode('ascii')})
    # return jsonify({'token': token.decode('ascii'), 'duration': 600})


############################################################
# API ROUTES
# ALL Companies Route: GET ALL COMPANIES
@rest_api.route('/companies/JSON')
# @auth.login_required
def companiesJSON():
    companies = session.query(Company).all()
    return jsonify(companies=[c.serialize for c in companies])


# SINGLE Company Route: GET SINGLE COMPANY WITH ALL CARS
@rest_api.route('/company/<int:company_id>/JSON')
# @auth.login_required
def companyJSON(company_id):
    cars = session.query(Cars).filter_by(company_id=company_id).all()
    return jsonify(Cars=[car.serialize for car in cars])


# SINGLE Car Route:
@rest_api.route('/car/<int:car_id>/JSON')
#@auth.login_required
def carJSON(car_id):
    car = session.query(Cars).filter_by(car_id=car_id).one()
    return jsonify(Car=car.serialize)