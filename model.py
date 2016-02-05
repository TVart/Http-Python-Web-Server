from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from setup_database import Base, User, Listing
 
class Model():
    """ Super class pour manager les models """
    def __init__(self):
        engine=create_engine('sqlite:///database.db',echo=True)
        Base.metadata.bind=engine
        DBSession = sessionmaker(bind=engine)
        self.session = DBSession()
 
    def get_users(self):
        users = self.session.query(User).all()
        return users

    def find_user(self,userid):
        user = self.session.query(User).filter_by(id=userid).one()
        return user
    
    def update_user(self,u):       
        user=self.session.query(User).filter_by(id=u['id']).one()
        if user:
            try:
                user.email = u['email']
                user.name = u['name']
                user.phone = u['phone']
                self.session.add(user)
                self.session.commit()
            except KeyError:
                print "Fail to update user %s" % u['name']
        else:
            print u

    def delete_user(self,userid):
        res = self.session.query(User).filter_by(id=userid).one()
        if res:
            self.session.delete(res)
            self.session.commit()
                         
    def create_user(self,form):
        print form
        u = User(name=form.getvalue('name'),email=form.getvalue('email'),phone=form.getvalue('phone'))
        print u
        self.session.add(u)
        self.session.commit()
 
if __name__=="__main__":
    model = Model()
    print model.__doc__
