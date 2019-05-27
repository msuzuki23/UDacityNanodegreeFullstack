from flask import Flask, render_template, request, redirect, jsonify, url_for
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import psycopg2 as pg
from databaseSetup import Base, Company, Cars

engine = create_engine('postgresql+psycopg2://msuzuki:pw@localhost/postgres')

Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()

app = Flask(__name__)

@app.route('/')
@app.route('/companies/')
def show():
    companies = session.query(Company).all()
    cars = session.query(Cars).order_by(Cars.car_id.desc()).limit(5)
    return render_template('companies.html', companies=companies, cars=cars)


@app.route('/company/<int:company_id>')
def showCompany(company_id):
    company = session.query(Company).filter_by(id=company_id).one()
    cars = session.query(Cars).filter_by(company_id=company_id).all()
    return render_template('showCompany.html', company=company, cars=cars)



@app.route('/car/<int:car_id>')
def showCar(car_id):
    #company = session.query(Company).filter_by(id=company_id).one()
    car = session.query(Cars).filter_by(car_id=car_id).one()
    return render_template('showCar.html', car=car)










@app.route('/car/new', methods=['GET', 'POST'])
def addCar():
    if request.method == 'POST':
        newCar = Cars(car_name=request.form['car_name'], car_desc=request.form['car_desc'], 
        company_id=int(request.form['company_id']))
        session.add(newCar)
        session.commit()

        return redirect(url_for('showCompany', company_id=request.form['company_id']))
    else:
        companies = session.query(Company).all()
        return render_template('addCar.html', companies=companies)













@app.route('/car/<int:car_id>/edit/', methods=['GET', 'POST'])
def editCar(car_id):
    editedCar = session.query(Cars).filter_by(car_id=car_id).one()
    if request.method == 'POST':
        if request.form['car_name']:
            editedCar.car_name = request.form['car_name']
            session.commit()
            return redirect(url_for('showCompany', company_id=editedCar.company_id))
    else:
        return render_template('editCar.html', car=editedCar)





@app.route('/car/<int:car_id>/delete/', methods=['GET', 'POST'])
def deleteCar(car_id):
    carToDelete = session.query(Cars).filter_by(car_id=car_id).one()
    if request.method == 'POST':
        session.delete(carToDelete)
        session.commit()
        return redirect(
            url_for('showCompany', company_id=carToDelete.company_id))
    else:
        return render_template(
            'deleteCar.html', car=carToDelete)









if __name__ == '__main__':
   app.debug = True
   app.run(host='0.0.0.0', port=8000)
