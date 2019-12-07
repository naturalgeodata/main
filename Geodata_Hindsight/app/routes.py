#import our base flask features
from flask import render_template, flash, redirect, url_for, request
#import from flask_login package
from flask_login import current_user, login_user, logout_user, login_required
#import from the app itself for routing
from app import app, db
#grab our homebrewed classes from the forms module inside app
from app.forms import LoginForm, RegistrationForm, ProjectForm
#import the database structure
from app.models import User, Project
#import security package
from werkzeug.urls import url_parse

#Base View
@app.route('/')
@app.route('/index')
@login_required
def index():

    return render_template('index.html',title='Home' )

#Login View
@app.route('/login', methods=['GET', 'POST'])
def login():
	if current_user.is_authenticated:
		return redirect(url_for('index'))
	form = LoginForm()

	if form.validate_on_submit():
		user = User.query.filter_by(username=form.username.data).first()
		if user is None or not user.check_password(form.password.data):
			flash('Invalid username or password')
			return redirect(url_for('login'))
		login_user(user, remember=form.remember_me.data)
		next_page = request.args.get('next')
		if not next_page or url_parse(next_page).netloc != '':
			next_page = url_for('index')
		return redirect(next_page)
	return render_template('login.html', title='Sign In', form=form)

#Logout View
@app.route('/logout', methods=['GET', 'POST'])
def logout():
	logout_user()
	return redirect(url_for('index'))

#Registration View
@app.route('/register', methods=['GET', 'POST'])

def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.company_id = current_user.company_id
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you have succesfully registered a user {}!'.format(current_user.username))
        return redirect(url_for('index'))
    return render_template('register.html', title='Register Users', form=form)

#Projects View
@app.route('/projects/<username>')
@login_required
def projects(username):
    projects = current_user.projects
    return render_template('projects.html', projects=projects)

#Create Projects view
@app.route('/projects/<username>/createproject', methods=['GET','POST'])
@login_required
def createproject(username):
    form = ProjectForm()
    if form.validate_on_submit():
        address = str(form.project_address.data + ", " + form.project_city.data + ", " + form.project_state.data)
        project = Project(internal_id=form.project_id.data, project_name=form.project_name.data, project_address=address)
        project.creator_id=current_user.id
        db.session.add(project)
        db.session.commit()
        flash('Congratulations, you have succesfully created a project: {}'.format(project.project_name))
        return redirect(url_for('projects', username=current_user.username))
    return render_template('createproject.html', form=form)
