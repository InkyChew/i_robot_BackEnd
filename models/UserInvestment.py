from database import db, ma
from sqlalchemy.orm import relationship

class UserInvestment(db.Model):
    __tablename__ = 'userInvestment'
    totalAssets = db.Column(db.Integer)
    stopLossPoint = db.Column(db.Integer)

    uid = db.Column(db.Integer, db.ForeignKey('user.uid'), nullable=False)
    # user = relationship("User", back_populates="userInvestment")

    def __init__(self, totalAssets, stopLossPoint):
        self.totalAssets = totalAssets
        self.stopLossPoint = stopLossPoint

class UserInvestmentSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = UserInvestment