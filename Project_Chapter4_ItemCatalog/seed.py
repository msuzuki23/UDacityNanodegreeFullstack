#!/usr/bin/python3.6.8

import os
import psycopg2 as pg

dbUser = os.environ.get('POSTGRES_USER')
dbPW = os.environ.get('POSTGRES_PW')

# Open Connection
connection = pg.connect(user=dbUser, password=dbPW, host="localhost", port="5432", database="postgres")
cursor = connection.cursor()

# Insert Car Companies
cursor.execute("INSERT INTO companies (name) VALUES ('BMW'),('Audi'),('Toyota'),('Honda'),('Chevrolet'),('Ford')")
connection.commit()

companies = {
    "BMW":[
        {"325":"This is BWM Entry Level Sedan."},
        {"525":"This is BMW Mid-Size Sedan."},
        {"735":"This is BMW Ultimate Luxury Sedan."}
        ],
    "Audi":[
        {"A4":"This is Audi Entry Level Sedan"},
        {"A6":"This is Audi Mid Level Sedan"},
        {"Q7":"This is Audi Ultimate SUV"}
    ],
    "Toyota":[
        {"Corolla":"Reliable Car"},
        {"Camry":"Mid Size Sedan"},
        {"RAV4":"Starter SUV"}
        ],
    "Honda":[
        {"Civic":"Honda Entry Level Sedan"},
        {"Accord":"Mid-Large Size Sedan"}
        ],
    "Chevrolet":[
        {"Volt":"Electric Car"},
        {"Silverado":"Mid Large Size Truck"},
        {"Suburban":"Luxury Large Size SUV"}
        ],
    "Ford":[
        {"Focus":"Small Size Hatchback"},
        {"F150":"Mid Large Size Truck"},
        {"Excursion":"Large Size SUV"}
        ]   
    }

for company in companies:
    cursor.execute("SELECT id FROM companies WHERE name='"+company+"'")
    companyID = cursor.fetchone()
    for car in companies[company]:
        print(list(car.keys())[0], list(car.values())[0], str(list(companyID)[0]))
        carQuery = "INSERT INTO cars (car_name, car_desc, company_id) VALUES ('"+list(car.keys())[0]+"', '"+list(car.values())[0]+"', '"+str(list(companyID)[0])+"')"
        cursor.execute(carQuery)
        connection.commit()

# Close Cursor and Connection
cursor.close()
connection.close()


    