from database import db

class User(db.Model):
    __tablename__ = 'user'
    uid = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), nullable=False, unique=True)
    password = db.Column(db.String(128))
    name = db.Column(db.String(50), nullable=False)

    def __init__(self, email, password, name):
        self.email = email
        self.password = password
        self.name = name