from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from datetime import datetime

db = SQLAlchemy()

class User(UserMixin, db.Model):
    id       = db.Column(db.Integer, primary_key=True)
    name     = db.Column(db.String(100), nullable=False)
    email    = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)
    created  = db.Column(db.DateTime, default=datetime.utcnow)

class Complaint(db.Model):
    id          = db.Column(db.Integer, primary_key=True)
    name        = db.Column(db.String(100))
    order_id    = db.Column(db.String(50))
    email       = db.Column(db.String(150))
    issue_type  = db.Column(db.String(100))
    description = db.Column(db.Text)
    status      = db.Column(db.String(30), default='Pending')
    created     = db.Column(db.DateTime, default=datetime.utcnow)

class Review(db.Model):
    id       = db.Column(db.Integer, primary_key=True)
    name     = db.Column(db.String(100))
    stars    = db.Column(db.Integer)
    category = db.Column(db.String(100))
    text     = db.Column(db.Text)
    created  = db.Column(db.DateTime, default=datetime.utcnow)