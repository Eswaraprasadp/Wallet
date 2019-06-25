from application import db
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from application import login
from flask_login import UserMixin

@login.user_loader
def load_user(id):
	return User.query.get(int(id))

class User(UserMixin, db.Model):
	id = db.Column(db.Integer, primary_key=True)
	username = db.Column(db.String(64), index=True, unique=True)
	email = db.Column(db.String(120), index=True, unique=True)
	password_hash = db.Column(db.String(128))
	balance = db.Column(db.Integer)
	expenses = db.relationship('Expenses', backref = 'user', lazy = 'dynamic')

	def set_password(self, password):
		self.password_hash = generate_password_hash(password)

	def check_password(self, password):
		return check_password_hash(self.password_hash, password)

	def set_balance(self, balance):
		self.balance = balance

	def get_balance(self):
		return self.balance

	def __repr__(self):
		return '<User {}>'.format(self.username)  

class Expenses(db.Model):
 	id = db.Column(db.Integer, primary_key = True)
 	title = db.Column(db.String(140))
 	description = db.Column(db.String(140))
 	amount = db.Column(db.Integer)
 	timestamp = db.Column(db.DateTime, index = True, default = datetime.utcnow)
 	modified_time = db.Column(db.DateTime, index = True, default = datetime.utcnow)
 	user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

 	def __repr__(self):
 		return '<Expense {}: {}>'.format(self.title, self.description)

 	def isModified(self):
 		return str(self.modified_time) != str(self.timestamp) 

 

	 