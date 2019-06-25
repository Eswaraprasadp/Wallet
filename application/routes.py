from flask import render_template, flash, redirect, url_for, request
from application import app, db
from application.forms import LoginForm, RegistrationForm, ExpensesForm
from flask_login import current_user, login_user, logout_user, login_required
from application.models import User, Expenses
from werkzeug.urls import url_parse
from datetime import datetime

# def hello_world():
# 	users = [{'name' : 'Eswar', 'age' : 18}, {'name' : 'Mr. Anonymous', 'age' : 1000}]

# 	return render_template('index.html', users = users)	
@app.route('/', methods = ['POST', 'GET'])
@app.route('/index', methods = ['POST', 'GET'])
@login_required
def index():
	form = ExpensesForm()
	if(form.validate_on_submit()):
		expense = Expenses(title = form.title.data, description = form.description.data, amount = form.amount.data, user = current_user)
		current_user.set_balance(form.amount.data + current_user.balance)
		db.session.add(expense)
		db.session.commit()
		flash("Your Expense were added")
		return redirect(url_for('index'))

	return render_template('index.html', title = 'Home', form = form)

@app.route('/index/<timestamp>', methods = ['POST', 'GET'])
@login_required
def edit(timestamp):	
	form = ExpensesForm()

	if(form.validate_on_submit()):
		e = Expenses.query.filter_by(timestamp = timestamp).first_or_404()
		prevAmount = e.amount
		expense = Expenses(title = form.title.data, description = form.description.data, amount = form.amount.data, user = current_user, modified_time = datetime.utcnow(), timestamp = e.timestamp)
		db.session.delete(e)
		current_user.set_balance(form.amount.data - prevAmount + current_user.balance)
		db.session.add(expense)
		db.session.commit()
		flash("Your Expense was updated")
		return redirect(url_for('index'))

	expense = Expenses.query.filter_by(timestamp = timestamp).first_or_404()
	# form.populate_obj(expense)
	form.title.data = expense.title
	form.description.data = expense.description
	form.amount.data = expense.amount

	return render_template('edit.html', title = 'Edit', form = form)

@app.route('/index/delete/<timestamp>', methods = ['POST', 'GET'])
def delete(timestamp):
	e = Expenses.query.filter_by(timestamp = timestamp).first_or_404()
	current_user.set_balance(current_user.balance - e.amount)
	db.session.delete(e)
	db.session.commit()
	flash("Your Expense was deleted")
	return redirect(url_for('index'))

@app.route('/login', methods = ['GET', 'POST'])
def login():
	if(current_user.is_authenticated):
		return redirect(url_for('index'))
	
	form = LoginForm()
	if(form.validate_on_submit()):
		user = User.query.filter_by(username = form.username.data).first()
		if(user is None or not user.check_password(form.password.data)):
			flash('Invalid username or password')
			return redirect(url_for('login'))

		login_user(user = user, remember = form.remember_me.data)
		# flash('Login request: User: {}, Remember me: {}'.format(form.username.data, form.remember_me.data))
		next_page = request.args.get('next')
		if(not next_page or url_parse(next_page).netloc != ''):
			next_page = url_for('index')
		
		return redirect(next_page)
	
	return render_template('login.html', title = 'Sign In', form = form)

@app.route('/logout')
def logout():
	logout_user()
	return redirect(url_for('login'))

@app.route('/register', methods = ['GET', 'POST'])
def register():
	if(current_user.is_authenticated):
		return redirect(url_for('index'))

	form = RegistrationForm()
	if(form.validate_on_submit()):
		user = User(username=form.username.data, email=form.email.data)
		user.set_password(form.password.data)
		user.set_balance(0)
		db.session.add(user)
		db.session.commit()
		flash('Successfully registered!')
		return redirect(url_for('login'))

	return render_template('register.html', title='Register', form = form)

if(__name__ == '__main__'):
	app.run(debug = True)


