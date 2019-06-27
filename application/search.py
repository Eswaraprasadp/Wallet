from application import db
from application.models import User

def search(name):
	results = []
	for user in User.query.all():
		if(name.lower() in user.username.lower()):
			results.append(user.username)

	return results