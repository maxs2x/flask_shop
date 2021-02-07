from flask_login import UserMixin
from main import db


class Users(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=True)
    email = db.Column(db.Integer, nullable=True)
    password = db.Column(db.Integer, nullable=True)
    data = db.Column(db.Integer, nullable=False)
    paid = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return self.password