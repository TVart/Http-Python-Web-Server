__author__ = 'vartan'

from bson.objectid import ObjectId
from pymongo import MongoClient
import datetime

class Articles():
    """Articles du blog"""
    def __init__(self):
        self.client = MongoClient('localhost', 27017)
        self.db = self.client['py-data']
        self.collection = self.db['articles']
        self.pagesize=10
        #self.articles = articles = [{"id":1,"title":"titre1"},{"id":2,"title":"titre2"}]

    def getAll(self,page=1):
        #db.foo.find().sort({x:1});
        #The 1 will sort ascending (oldest to newest) and -1 will sort descending (newest to oldest.)
        #db.foo.find().sort({_id:1});
        #That will return back all your documents sorted from oldest to newest.
        #db.foo.find().sort({_id:1}).limit(50);
        """
        //Page 1
        db.users.find().limit (10)
        //Page 2
        db.users.find().skip(10).limit(10)
        //Page 3
        db.users.find().skip(20).limit(10)
        db.users.find().skip(pagesize*(n-1)).limit(pagesize)
        """
        return self.collection.find().skip(self.pagesize*(page-1)).limit(self.pagesize);

    def getOne(self,key, value):
        return []

    def create(self,data):
        pass

    def edit(self,id,data):
        pass

    def delete(self,id):
        pass

if __name__ == '__main__':
    print "This class should never been launched from itself"