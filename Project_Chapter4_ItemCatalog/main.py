#!/usr/bin/python3.6.8

import random, string, json, os
from flask import Flask, render_template, request, redirect, jsonify, url_for, abort, g, Blueprint
from flask import session as login_session
from sqlalchemy import create_engine
from sqlalchemy.orm import relationship, sessionmaker
from user import getUserID, getUserInfo, createUser
from databaseSetup import Base, Company, Cars, User

main_api = Blueprint('main_api', __name__)

dbUser = os.environ.get('POSTGRES_USER')
dbPW = os.environ.get('POSTGRES_PW')
engine = create_engine('postgresql+psycopg2://'+dbUser+':'+dbPW+'@localhost/postgres')

Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()

@main_api.route('/')
@main_api.route('/companies')
def show():
    companies = session.query(Company).order_by(Company.name)
    cars = session.query(Cars).order_by(Cars.car_id.desc()).limit(10)
    return render_template('companies.html', companies=companies, cars=cars)

@main_api.route('/login')
def showLogin():
    state = ''.join(random.choice(string.ascii_uppercase + string.digits)
    for x in range(32))
    login_session['state'] = state
    return render_template('login.html', STATE=state)

@main_api.route('/company/<int:company_id>')
def showCompany(company_id):    
    company = session.query(Company).filter_by(id=company_id).one()
    cars = session.query(Cars).filter_by(company_id=company_id).all()
    if 'user_id' in login_session:
        conUserId = login_session['user_id']
        return render_template('showCompany.html', company=company, cars=cars, conUserId = conUserId)
    return render_template('showCompany.html', company=company, cars=cars, conUserId = 'null')

@main_api.route('/car/<int:car_id>')
def showCar(car_id):
    car = session.query(Cars).filter_by(car_id=car_id).one()
    if 'username' not in login_session:
        return render_template('showCar.html', car=car, conUserId = 'null')
    conUserId = login_session['user_id']
    return render_template('showCar.html', car=car, conUserId = conUserId)

@main_api.route('/car/new', methods=['GET', 'POST'])
def addCar():
    if 'username' not in login_session:
        return redirect('/login')
    if request.method == 'POST':
        newCar = Cars(car_name=request.form['car_name'], car_desc=request.form['car_desc'], 
        company_id=int(request.form['company_id']), user_id=getUserID(login_session['email']))
        session.add(newCar)
        session.commit()
        return redirect(url_for('main_api.showCompany', company_id=request.form['company_id']))
    else:
        companies = session.query(Company).all()
        return render_template('addCar.html', companies=companies)

@main_api.route('/car/<int:car_id>/edit/', methods=['GET', 'POST'])
def editCar(car_id):
    if 'username' not in login_session:
        return redirect('/login')
    editedCar = session.query(Cars).filter_by(car_id=car_id).one()
    if request.method == 'POST':
        editedCar.car_name = request.form['car_name']
        editedCar.car_desc = request.form['car_desc']
        session.commit()
        return redirect(url_for('main_api.showCompany', company_id=editedCar.company_id))
    else:
        return render_template('editCar.html', car=editedCar)
        
@main_api.route('/car/<int:car_id>/delete/', methods=['GET', 'POST'])
def deleteCar(car_id):
    if 'username' not in login_session:
        return redirect('/login')
    carToDelete = session.query(Cars).filter_by(car_id=car_id).one()
    if request.method == 'POST':
        session.delete(carToDelete)
        session.commit()
        return redirect(
            url_for('main_api.showCompany', company_id=carToDelete.company_id))
    else:
        return render_template('deleteCar.html', car=carToDelete)
        