from flask import Flask, render_template, request, redirect, jsonify, url_for
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import psycopg2 as pg
from databaseSetup import Base, Company, Cars

engine = create_engine('postgresql+psycopg2://msuzuki:pw@localhost/postgres')

Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()

#companies = session.query(Company).all()
#cars = session.query(Cars).all()
#for car in cars:
#    print(car.car_name, car.company.name)
#Testing Calling outside function
#hi = hello()
#print(hi)


app = Flask(__name__)




@app.route('/')
@app.route('/companies/')
def show():
    companies = session.query(Company).all()
    cars = session.query(Cars).all()
    return render_template('companies.html', companies=companies, cars=cars)




if __name__ == '__main__':
   app.debug = True
   app.run(host='0.0.0.0', port=8000)
