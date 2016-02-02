import sys,datetime
from sqlalchemy import Column, String, Integer, ForeignKey, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
 
Base = declarative_base()
Now = datetime.datetime.now()
 
class User(Base):
    __tablename__='user'
    name=Column(String(50),nullable=False)
    id=Column(Integer, primary_key=True)
    email=Column(String(150),default=None)
    phone=Column(String(20),default=None)
 
class Listing(Base):
     
    __tablename__='listing'
    title=Column(String(150),nullable=False)
    description=Column(String(150),nullable = False)
    property_type=Column(String(50),nullable=False)
    city=Column(String(100),nullable=False)
    zip_code=Column(String(10),nullable=False)
    price=Column(Integer,nullable=False)
    surface=Column(Integer)
    property_type=Column(String(50),nullable=False)
    date_creation=Column(String(50),default=Now.strftime("%Y-%m-%d %H:%M"))
    date_update=Column(String(50),default=Now.strftime("%Y-%m-%d %H:%M"))
    id=Column(Integer, primary_key=True)
    url=Column(String(250),nullable=False)
    user_id=Column(Integer, ForeignKey('user.id'))
    user=relationship(User)
 
engine=create_engine("sqlite:///database.db",echo=True);
Base.metadata.create_all(engine)
