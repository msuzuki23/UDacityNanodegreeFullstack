#!/usr/bin/python3.6.8

from sqlalchemy import create_engine
from sqlalchemy.orm import relationship, sessionmaker
from databaseSetup import Base, Company, Cars, User
import os

dbUser = os.environ.get('POSTGRES_USER')
dbPW = os.environ.get('POSTGRES_PW')
engine = create_engine('postgresql+psycopg2://'+dbUser+':'+dbPW+'@localhost/postgres')

Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()

def getUserID(email):
    try: 
        user = session.query(User).filter_by(user_email = email).one()
        return user.user_id
    except:
        return None

def getUserInfo(user_id):
    user = session.query(User).filter_by(user_id = user_id).one()
    return user.user_id

def createUser(login_session):
    newUser = User(user_name = login_session['username'], user_email=login_session['email'], user_picture=login_session['picture'])
    session.add(newUser)
    session.commit()
    user = session.query(User).filter_by(user_email = login_session['email']).one()
    return user.user_id