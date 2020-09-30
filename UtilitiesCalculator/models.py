from datetime import datetime
from sqlalchemy.orm import relationship
from flask_login import UserMixin
from sqlalchemy import Column, Integer, String, ForeignKey
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from UtilitiesCalculator.__init__ import app, db


class User(db.Model, UserMixin):
    __tablename__ = "USER"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column("Name", db.String(20), unique=True, nullable=False)
    email = db.Column("Email", db.String(120), unique=True,
                          nullable=False)
    password = db.Column("Password", db.String(60), unique=True,
                            nullable=False)

    def get_reset_token(self, expires_sec=1800):
        s = Serializer(app.config['SECRET_KEY'], expires_sec)
        return s.dumps({'user_id': self.id}).decode('utf-8')

    @staticmethod
    def verify_reset_token(token):
        s = Serializer(app.config['SECRET_KEY'])
        try:
            user_id = s.loads(token)['user_id']
        except:
            return None
        return User.query.get(user_id)