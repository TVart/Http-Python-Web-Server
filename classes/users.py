class User: 
    def __init__(self): 
        self.users={
            1:{"nom":"demo","prenom":"mode","age":12},
            2:{"nom":"test","prenom":"tost","age":7},
            3:{"nom":"toto","prenom":"momo","age":21}
        }

    def all(self):
        r=""
        for u in self.users:
            r += "<a href='/user/%s'>%s</a> %s %s<br/>"  % \
                 (str(u), self.users[u]['nom'],self.users[u]['prenom'],self.users[u]['age'])
        return r
    def get(self, id):
        try:
            return self.users[id]
        except KeyError:
            return {"error":{"message": "index %d not found" % id}}

    def add(self,user):
        self.users.update(user)

    def help(self):
	    print "Do not be stupid";


if __name__ == '__main__':
    User.help(User())

