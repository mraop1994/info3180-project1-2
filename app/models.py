from . import db  
class Myprofile(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String(80), unique=False)
    lastname = db.Column(db.String(80), unique=False)
    sex = db.Column(db.String(10), unique=False)
    age = db.Column(db.String(2), unique=False)
    username = db.Column(db.String(20), unique=True)
    image = db.Column(db.String(200), unique=True)
    
    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        try:
            return unicode(self.id)  # python 2 support
        except NameError:
            return str(self.id)  # python 3 support

    def __repr__(self):
        return '<id {}>'.format(self.id)