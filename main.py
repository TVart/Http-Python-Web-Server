from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from setup_database import Base, User, Job


class Main():
    def __init__(self):
        engine = create_engine('sqlite:///userjob.db')
        Base.metadata.bind = engine
        DBSession = sessionmaker(bind=engine)
        self.session = DBSession()

        
    def get(self):
        return self.session

    def create_user(self):
        user1 = User(name='Tvart')
        self.session.add(user1)
        self.session.commit()
        self.session.query(User).all()

    def first_user(self):
        user=self.session.query(User).first()
        return user

    def all_jobs(self):
        jobs=self.session.query(Job).all()
        return jobs

    def job_filter_by_city(self,cityname):
        jobs=self.session.query(Job).filter_by(city=str(cityname))

    def user_filter(self,userid):
        user=self.session.query(User).filter_by(id=int(userid)).one()
        
    def create_job(self):
        user1=self.first_user()
        job1=Job(name='DevOps', user=user1)
        self.session.add(job1)
        self.session.commit()
        self.session.query(Job).all()
        


if __name__=='__main__':
    m=Main()
    jobs=m.all_jobs()
    for i in jobs:
        print i.name
        print i.city
        print i.user.name
    

    
        
