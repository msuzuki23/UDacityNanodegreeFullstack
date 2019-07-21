# !/usr/bin/python3.6.8

import os
import sys
import random
import string
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine, Column, ForeignKey, Integer, String
from passlib.apps import custom_app_context as pwd_context
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from itsdangerous import BadSignature, SignatureExpired

Base = declarative_base()
secret_key = ''.join(random.choice(string.ascii_uppercase + string.digits)
                     for x in range(32))

dbUser = os.environ.get('POSTGRES_USER')
dbPW = os.environ.get('POSTGRES_PW')


class User(Base):
    __tablename__ = 'users'
    user_id = Column(Integer, primary_key=True)
    user_name = Column(String(50), nullable=False)
    user_email = Column(String(100), index=True)  # nullable=False)
    user_picture = Column(String(50))
    password_hash = Column(String(64))

    def hash_password(self, password):
        self.password_hash = pwd_context.encrypt(password)

    def verify_password(self, password):
        return pwd_context.verify(password, self.password_hash)

    def generate_auth_token(self, expiration=600):
        s=Serializer(secret_key, expires_in=expiration)
        return s.dumps({'id': self.user_id})

    @staticmethod
    def verify_auth_token(token):
        s = Serializer(secret_key)
        try:
            data = s.loads(token)
        except SignatureExpired:
            # Valid Token, but expired
            return None
        except BadSignature:
            # Invalid Token
            return None
        user_id = data['id']
        return user_id


class Company(Base):
    __tablename__ = 'companies'
    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
    
    @property
    def serialize(self):
        """Return object data in easily serializeable format"""
        return {
            'id': self.id,
            'name': self.name,
        }


class Cars(Base):
    __tablename__ = 'cars'
    car_id = Column(Integer, primary_key=True)
    car_name = Column(String(50), nullable=False)
    car_desc = Column(String(500), nullable=False)
    company_id = Column(Integer, ForeignKey('companies.id'))
    company = relationship(Company)
    user_id = Column(Integer, ForeignKey('users.user_id'))
    user = relationship(User)
    
    @property
    def serialize(self):
        """Return object data in easily serializeable format"""
        return {
            'car_id': self.car_id,
            'car_name': self.car_name,
            'car_desc': self.car_desc,
            'company_id': self.company.id,
            'company_name': self.company.name,
        }


engine = create_engine('postgresql+psycopg2://'+dbUser+':'+dbPW+'@localhost/postgres')
Base.metadata.create_all(engine)