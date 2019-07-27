#!/usr/bin/python3.6.8
# This module contains the routes
# for the rest api

import os
import json
from sqlalchemy import create_engine
from sqlalchemy.orm import relationship, sessionmaker
from flask import Blueprint, jsonify
from databaseSetup import Base, Company, Cars, User

# Database connection
dbUser = os.environ.get('POSTGRES_USER')
dbPW = os.environ.get('POSTGRES_PW')
engine = create_engine('postgresql+psycopg2://'+dbUser+':'+dbPW+'@localhost/postgres')

# Bind database to engine
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)

# Create DB session
session = DBSession()

# Create rest_api blueprint
rest_api = Blueprint('rest_api', __name__)


# API ROUTES
# ALL Companies Route: GET ALL COMPANIES
@rest_api.route('/companies/JSON')
def companiesJSON():
    """Get all companies route"""

    companies = session.query(Company).all()
    return jsonify(companies=[c.serialize for c in companies])


# SINGLE Company Route: GET SINGLE COMPANY WITH ALL CARS
@rest_api.route('/company/<int:company_id>/JSON')
def companyJSON(company_id):
    """Get a single company route"""

    cars = session.query(Cars).filter_by(company_id=company_id).all()
    return jsonify(Cars=[car.serialize for car in cars])


# SINGLE Car Route:
@rest_api.route('/car/<int:car_id>/JSON')
def carJSON(car_id):
    """Get a single car route"""

    car = session.query(Cars).filter_by(car_id=car_id).one()
    return jsonify(Car=car.serialize)