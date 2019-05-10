from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from flask_login import current_user
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField
from wtforms.validators import DataRequired,Length,Email, EqualTo,ValidationError
from flaskblog2.models import User

class RegistrationForm(FlaskForm):
	username = StringField('Username', validators=[DataRequired(), Length(min=5, max=20)])
	email = StringField('Email', validators=[DataRequired(), Email()])
	password = PasswordField('Password' ,validators=[DataRequired()])
	confirm = PasswordField('Confirm Password', validators=[DataRequired(),EqualTo('password')])
	submit = SubmitField('Signup')

	def validate_username(self, username):
		user = User.query.filter_by(username=username.data).first()
		if user:
			raise ValidationError("A user with '{}' username already exist. Use a different username".format(username.data))


	def validate_email(self, email):
		user = User.query.filter_by(email=email.data).first()
		if user:
			raise ValidationError("A user with '{}' email already exist. Use a different email instead".format(email.data))



class LoginForm(FlaskForm):
	email = StringField('Email', validators=[DataRequired(), Email()])
	password = PasswordField('Password', validators=[DataRequired()])
	remember = BooleanField('Remember me')
	submit = SubmitField('Login')

class UpdateAccountForm(FlaskForm):
	username = StringField('Username', validators=[DataRequired(), Length(min=5, max=20)])
	email = StringField('Email', validators=[DataRequired(), Email()])
	picture = FileField('Update Profile Picture', validators=[FileAllowed(['jpg','png'])])
	submit = SubmitField('Update')

	def validate_username(self, username):
		if current_user.username != username.data:
			user = User.query.filter_by(username=username.data).first()
			if user:
				raise ValidationError("A user with '{}' username already exist. Use a different username".format(username.data))


	def validate_email(self, email):
		if current_user.email != email.data:
			user = User.query.filter_by(email=email.data).first()
			if user:
				raise ValidationError("A user with '{}' email already exist. Use a different email instead".format(email.data))

class PostForm(FlaskForm):
	title = StringField('Title', validators=[DataRequired()])
	content = TextAreaField('Content', validators=[DataRequired()])
	post_image = FileField('Add picture',validators=[FileAllowed(['jpg','png'])])
	submit = SubmitField('Submit')




