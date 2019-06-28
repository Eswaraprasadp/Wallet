from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, IntegerField, FieldList, FormField
from wtforms.ext.sqlalchemy.fields import QuerySelectMultipleField, QuerySelectField
from wtforms import widgets
from wtforms.validators import DataRequired, ValidationError, Email, EqualTo, NumberRange, Length
from application.models import User, Expenses, SelectedUser
from wtforms.fields.core import Label
from application import db

class LoginForm(FlaskForm):
	username = StringField('Username', validators=[DataRequired()])
	password = PasswordField('Password', validators=[DataRequired()])
	remember_me = BooleanField('Remember Me')
	submit = SubmitField('Sign In')

class RegistrationForm(FlaskForm):
	username = StringField('Username', validators=[DataRequired()])
	email = StringField('Email', validators=[DataRequired(), Email()])
	password = PasswordField('Password', validators=[DataRequired()])
	confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
	submit = SubmitField('Register')

	def validate_username(self, username):
		user = User.query.filter_by(username = username.data).first()
		if(user is not None):
			raise ValidationError("This Username is already taken by other user")

	def validate_email(self, email):
		email = User.query.filter_by(email = email.data).first()
		if(email is not None):
			raise ValidationError("This Email is already taken by other user")

class ExpensesForm(FlaskForm):
	title = StringField('Title',validators=[DataRequired(), Length(min = 1, max = 50)])
	description  = StringField('Description', validators=[Length(min = 0, max = 140)])
	amount = IntegerField('Amount', validators=[DataRequired(), NumberRange(min = 0, max = 10000000)])	
	submit = SubmitField('Add to Wallet')		

class SearchForm(FlaskForm):
	search = StringField('Search User', validators = [DataRequired(), Length(min = 1, max = 50)])
	submit = SubmitField('Search')

def select_users_form_factory(keyword):

	class SelectUsersForm(FlaskForm):
		
		users = QuerySelectMultipleField('User', query_factory = lambda: User.query.filter(User.username.ilike('%{0}%'.format(keyword))).all() , get_label =  lambda user:user.username, widget=widgets.ListWidget(prefix_label = False),
	        option_widget=widgets.CheckboxInput())
		submit = SubmitField('Select')
	
	return SelectUsersForm

# def amount_form_factory(username):
# 	class AmountForm(FlaskForm):
# 		amount =  IntegerField(label = username, NumberRange(min = 0, max = 1000000), validators = [DataRequired()])

# 	return AmountForm

class PaymentForm(FlaskForm):
	submit = SubmitField('Pay')
