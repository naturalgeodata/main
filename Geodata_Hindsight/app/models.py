from app import db, login
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from datetime import datetime
from time import time

class User(UserMixin, db.Model):
	id = db.Column(db.Integer, primary_key=True)
	username = db.Column(db.String(64), index=True, unique=True)
	email = db.Column(db.String(120), index=True, unique=True)
	password_hash = db.Column(db.String(128))
	company_id = db.Column(db.Integer, db.ForeignKey('company.id'))
	manager = db.Column(db.Boolean, default=False)
	admin = db.Column(db.Boolean, default=False)

	def __repr__(self):
		return '<User {}>'.format(self.username)

	def set_password(self, password):
		self.password_hash = generate_password_hash(password)

	def check_password(self, password):
		return check_password_hash(self.password_hash, password)

class Company(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	company_name = db.Column(db.String(64), index=True, unique=True)
	company_email = db.Column(db.String(120), index=True, unique=True)
	company_address = db.Column(db.String(200), index=True, unique=True)
	users = db.relationship('User', backref='company', lazy='dynamic')

	def __repr__(self):
		return '<Company {}>'.format(self.company_name)

class Project(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	internal_id = db.Column(db.Integer, index=True, unique=True)
	project_name = db.Column(db.String(60), index=True, unique=True)
	project_address = db.Column(db.String(120), unique=True)
	time_created = db.Column(db.DateTime, default=datetime.utcnow())

@login.user_loader
def load_user(id):
	return User.query.get(int(id))
