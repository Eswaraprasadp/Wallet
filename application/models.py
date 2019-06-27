from application import db
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from application import login
from flask_login import UserMixin

@login.user_loader
def load_user(id):
	user = User.query.get(int(id))
	if(user):
		return user
	else:
		return None

@login.request_loader
def load_user_from_request(request):

    # first, try to login using the api_key url arg
    api_key = request.args.get('api_key')
    if api_key:
        user = User.query.filter_by(api_key=api_key).first()
        if user:
            return user

    # next, try to login using Basic Auth
    api_key = request.headers.get('Authorization')
    if api_key:
        api_key = api_key.replace('Basic ', '', 1)
        try:
            api_key = base64.b64decode(api_key)
        except TypeError:
            pass
        user = User.query.filter_by(api_key=api_key).first()
        if user:
            return user

    # finally, return None if both methods did not login the user
    return None

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

class SelectedUser(UserMixin, db.Model):
	id = db.Column(db.Integer, primary_key=True)
	username = db.Column(db.String(64), index=True, unique=True)

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

 

	 