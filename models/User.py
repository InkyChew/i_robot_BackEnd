from database import db, ma
from sqlalchemy.orm import relationship
class User(db.Model):
    __tablename__ = 'user'
    uid = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), nullable=True, unique=True)
    password = db.Column(db.String(128))
    name = db.Column(db.String(50), nullable=False)
    picture = db.Column(db.String(128))
    lineId = db.Column(db.String(128), nullable=False, unique=True)

    # userInvestment = relationship("UserInvestment", uselist=False, back_populates="user")

    def __init__(self, email, password, name, picture, lineId):
        self.email = email
        self.password = password
        self.name = name
        self.picture = picture
        self.lineId = lineId

class UserSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = User