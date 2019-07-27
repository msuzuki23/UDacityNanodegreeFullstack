#!/usr/bin/python3.6.8
# This modules contains functionalities
# related to user
# get user info
# if user does not already exist create new user

import os
from sqlalchemy import create_engine
from sqlalchemy.orm import relationship, sessionmaker
from databaseSetup import Base, Company, Cars, User

# Create database connection
dbUser = os.environ.get('POSTGRES_USER')
dbPW = os.environ.get('POSTGRES_PW')
engine = create_engine('postgresql+psycopg2://'+dbUser+':'+dbPW+'@localhost/postgres')

# Bind database to engine
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)

# Create DB session
session = DBSession()


# Get user email
def getUserID(email):
    """Check if user/email is in DB"""

    try:
        user = session.query(User).filter_by(user_email=email).one()
        return user.user_id
    except Exception:
        return None


# Get user id
def getUserInfo(user_id):
    """Get userid"""

    user = session.query(User).filter_by(user_id=user_id).one()
    return user.user_id


# Create new user
def createUser(login_session):
    """Create new user in DB"""

    newUser = User(
                   user_name=login_session['username'],
                   user_email=login_session['email'],
                   user_picture=login_session['picture']
                   )
    session.add(newUser)
    session.commit()
    user = session.query(User).filter_by(
                                        user_email=login_session['email']
                                        ).one()
    return user.user_id
