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




#app = Flask(__name__)

# http://localhost:8000/
#@app.route("/")
#def hello():
#    return "Hello World!"


# @app.route('/')
# @app.route('/restaurant/')
# def showRestaurants():
#     restaurants = session.query(Restaurant).all()
#     # return "This page will show all my restaurants"
# return render_template('restaurants.html', restaurants=restaurants)




# http://localhost:8000/catalog/Snowboarding/items


# http://localhost:8000/catalog/Snowboarding/Snowboard


# http://localhost:8000/catalog/Snowboard/edit (logged in)


# http://localhost:8000/catalog/Snowboard/delete (logged in)


# http://localhost:8000/catalog.json

#if __name__ == '__main__':
#    app.debug = True
#    app.run(host='0.0.0.0', port=8000)
