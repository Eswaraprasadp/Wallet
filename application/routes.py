from flask import render_template, flash, redirect, url_for, request
from application import app, db
from application.forms import LoginForm, RegistrationForm, ExpensesForm, SearchForm, select_users_form_factory,  PaymentForm
from flask_login import current_user, login_user, logout_user, login_required
from application.models import User, Expenses, SelectedUser
from werkzeug.urls import url_parse
from datetime import datetime
from wtforms import IntegerField
from wtforms.validators import DataRequired

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

	deleted = db.session.query(SelectedUser).delete()
	db.session.commit()
	current_user.set_balance(current_user.balance)

	return render_template('index.html', title = 'Home', form = form)

@app.route('/split_bill/search', methods = ['GET', 'POST'])
def search_users():
	search_form = SearchForm()
	if(search_form.validate_on_submit()):
		return redirect(url_for('select_users', query = search_form.search.data))		

	print("SelectedUsers: ", SelectedUser.query.all())
	return render_template('search.html', title = 'Search', search_form = search_form, selected = SelectedUser.query.all())

@app.route('/split_bill/select/<query>', methods = ['GET', 'POST'])
def select_users(query):
	
	SelectUsersForm = select_users_form_factory(query)
	select_users_form = SelectUsersForm()

	if(select_users_form.validate_on_submit()):
		selected_users = select_users_form.users.data
		# print("Selected Users: ", selected_users)
		print("Current User: ", current_user)
		if(current_user in selected_users):
			flash("You Cannot choose your yourself!", 'error')
			return render_template('search_results.html', title = 'Search', select_form = select_users_form, search_form = SearchForm(search = query), selected = SelectedUser.query.all())
		
		for user in selected_users:
			u = SelectedUser(username = user.username)
			db.session.add(u)
			db.session.commit()

		return redirect(url_for('search_users'))

	return render_template('search_results.html', title = 'Search', select_form = select_users_form, search_form = SearchForm(search = query), selected = SelectedUser.query.all())

@app.route('/split_bill/check/<selected>', methods = ['GET', 'POST'])
@login_required
def check_selected(selected):
	selected_users = SelectedUser.query.all()
	if(len(selected_users) >= 0):
		return redirect(url_for('split_bill', selected = selected_users))

	flash("Select atleast one user!", "error")
	return redirect(url_for('search_users'))

@app.route('/split_bill/<selected>', methods = ['GET', 'POST'])
@login_required
def split_bill(selected):
	usernames = [user.username for user in SelectedUser.query.all()]
	for username in usernames:
		setattr(PaymentForm, username, IntegerField(1000, validators = [DataRequired()]))

	payment_form = PaymentForm()
	if(payment_form.validate_on_submit()):	
		amounts = [getattr(payment_form, username).data for username in usernames]
		if(sum(amounts) >= current_user.balance):
			flash("You do not have enough balance to pay!")
			return render_template('split_bill.html', form = payment_form, usernames = usernames)

		else:
			description = "Payments: \n"
			for amount, username in zip(list(amounts), list(usernames)):
				reciever = User.query.filter_by(username = username).first()
				reciever.balance += amount
				current_user.balance -= amount
				description += username + ": Rs. %s" % amount
				recieved = Expenses(user = reciever, amount = amount, title = "Payment recieved from " + current_user.username)

			names = ', '.join(usernames)
			if(len(usernames) > 1):
				names = ', '.join(usernames[:-1])
				names += " and " + usernames[-1]	
			

			deleted = db.session.query(SelectedUser).delete()
			payment = Expenses(user = current_user, amount = sum(amounts), title = "Payment done for " + names, description = description)
			db.session.commit()

			flash("Payment done", "success")
			return redirect(url_for('index'))

	return render_template('split_bill.html', form = payment_form, usernames = usernames)

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
	flash("This will just delete the history. Cannot be refunded. Click OK to proceed", "alert")
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
			flash('Invalid username or password', "error")
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


