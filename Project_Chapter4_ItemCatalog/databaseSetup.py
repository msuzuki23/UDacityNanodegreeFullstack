import os
import sys
from sqlalchemy import create_engine
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, ForeignKey, Integer, String

Base = declarative_base()

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

    @property
    def serialize(self):
        """Return object data in easily serializeable format"""
        return {
            'car_id': self.car_id,
            'car_name': self.car_name,
            'car_desc': self.car_desc,
            'company': self.company,
        }



engine = create_engine('postgresql+psycopg2://msuzuki:pw@localhost/postgres')
Base.metadata.create_all(engine)




