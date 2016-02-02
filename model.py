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
    
    def update_users(self):
        users=[
            {'name':'User A', 'email':'hello@mailbox.com','phone': '06543210'},
            {'name':'User B', 'email':'user@test.com'},
            {'name':'User C', 'email':'admin@coucou.fr','phone': '02543210'},
            {'name':'User D', 'phone': '06566898'},
            {'name':'User E'},
        ]
        for u in users:
            user=self.session.query(User).filter_by(name=u['name']).one()
            if user:
                try:
                    user.email = u['email']
                    self.session.add(user)
                    self.session.commit()
                except KeyError:
                    print "User %s has no email" % u['name']
 
    def delete_user(self):
        res = self.session.query(User).filter_by(email=None,phone=None).one()
        if res:
            self.session.delete(res)
            self.session.commit()
                         
    def populate_users(self):
        users=[
            {'name':'User A', 'email':'hello@mailbox.com','phone': '06543210'},
            {'name':'User B', 'email':'user@test.com'},
            {'name':'User C', 'email':'admin@coucou.fr','phone': '02543210'},
            {'name':'User D', 'phone': '06566898'},
            {'name':'User E'},
        ]
        for user in users:
            u = User(name=user['name'])
            self.session.add(u)
            self.session.commit()
 
if __name__=="__main__":
    model = Model()
    print model.__doc__    
    model.delete_user()
    """for u in model.get_users():
        print "%s %s %s" % (u.name, u.email, u.phone)"""
