from application import app, db, moment
from application.models import User, Expenses

@app.shell_context_processor
def make_shell_context():
	return {'db': db, 'User': User, 'Expenses': Expenses, 'users': User.query.all(), 'expenses': Expenses.query.all(), 'moment': moment}