from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from datetime import datetime

db = SQLAlchemy()

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    role = db.Column(db.String(50), default='user')

class Analysis(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    predicted_price = db.Column(db.Float)
    roi = db.Column(db.Float)
    irr = db.Column(db.Float)
    risk_level = db.Column(db.String(50))
    recommendation = db.Column(db.String(50))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))