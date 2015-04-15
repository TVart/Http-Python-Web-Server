class User: 
    def __init__(self): 
        self.nom = "Invite"

	# setters
    def set_nom(self, _nom='Invite'): 
        self.nom = "Invite"

    def set_age(self, _age): 
        self.age = _age

    def set_ville(self): 
        self.ville = _ville

	#getter
    def get_nom(self): 
        return self.nom

    def get_age(self): 
        return self.age

    def get_ville(self): 
        return self.ville

    def help(self):
	print "u = User()\nAvailable methods :\n-set_nom\n-set_age\n-set_ville\n-get_ville\n-get_nom\n-get_age";


if __name__ == '__main__': User.help(User())

