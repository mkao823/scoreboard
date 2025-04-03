from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()

class Team(Base):
    __tablename__ = 'teams'
    id = Column(Integer, primary_key=True)
    abbreviation = Column(String)
    city = Column(String)  
    #conference = Column(String)
    #division = Column(String)
    full_name = Column(String)
    name = Column(String)