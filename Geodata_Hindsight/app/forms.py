from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo, ValidationError
from app.models import User, Project, Company

class LoginForm(FlaskForm):
	username = StringField('Username', validators=[DataRequired()])
	password = PasswordField('Password', validators=[DataRequired()])
	remember_me = BooleanField('Remember Me')
	submit = SubmitField('Sign In')

class RegistrationForm(FlaskForm):
	username = StringField('Username', validators=[DataRequired()])
	email = StringField('Email', validators=[DataRequired(), Email()])
	password = PasswordField('Password', validators=[DataRequired()])
	password2 = PasswordField(
			'Repeat Password (please)', validators=[DataRequired(), EqualTo('password')])
	manager = BooleanField('Manager Access')
	submit = SubmitField('Register')

	def validate_username(self, username):
		user = User.query.filter_by(username=username.data).first()
		if user is not None:
			raise ValidationError('Please use a different username.')

	def validate_email(self, email):
		user = User.query.filter_by(email=email.data).first()
		if user is not None:
			raise ValidationError('Please use a different email address.')

class ProjectForm(FlaskForm):
	project_id = StringField('Project ID', validators=[DataRequired()])
	project_name = StringField('Project Name', validators=[DataRequired()])
	project_address = StringField('Address', validators=[DataRequired()])
	project_city = StringField('City', validators=[DataRequired()])
	project_state = StringField('State', validators=[DataRequired()])
	submit = SubmitField('Create Project')

	def validate_project_name(self, name):
		project = Project.query.filter_by(project_name=name.data).first()
		if project is not None:
			raise ValidationError('Please use a different project name. (This one might exist already!)')

	def validate_project_id(self, id):
		id = Project.query.filter_by(internal_id=id.data).first()
		if id is not None:
			raise ValidationError('Please use a different project ID. (This one might exist already!)')
			
class TaskForm(FlaskForm):
    task_body = StringField('Task', validators=[DataRequired()], default="Add Task.")
    submit = SubmitField('+')
    check_box = BooleanField('Task Completed', default=False)
