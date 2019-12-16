#import our base flask features
from flask import render_template, flash, redirect, url_for, request
#import from flask_login package
from flask_login import current_user, login_user, logout_user, login_required
#import from the app itself for routing
from app import app, db
#grab our homebrewed classes from the forms module inside app
from app.forms import LoginForm, RegistrationForm, ProjectForm, TaskForm
#import the database structure
from app.models import User, Project, Task
#import security package
from werkzeug.urls import url_parse

#Base View
@app.route('/')
@app.route('/index')
@login_required
def index():
    
    projects = Project.query.filter_by(creator_id=current_user.id)
    projects.order_by(Project.time_created.desc()).all()
    return render_template('index.html',title='Home', projects=projects )

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
    
    if not current_user.manager:
        flash('Your not authorized to register users.')
        return redirect(url_for('index'))
        
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.company_id = current_user.company_id
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you have succesfully registered a user: {}!'.format(user.username))
        return redirect(url_for('index'))
        
    return render_template('register.html', title='Register Users', form=form)

#Projects Overall View
@app.route('/projects/users/<username>')
@login_required
def projects(username):
    #Placeholder for the many-many database relationship that will allow managers to place users on projects
    projects = Project.query.all()
        
    return render_template('exploreprojects.html', projects=projects)

#Create Projects view
@app.route('/projects/users/<username>/createproject', methods=['GET','POST'])
@login_required
def createproject(username):
    if not current_user.manager:
        flash('Your not authorized to create projects.')
        return redirect(url_for('index'))
        
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

#Projects Individual View
@app.route('/projects/<projectid>', methods=['GET', 'POST'])
@login_required
def project(projectid):
    project = Project.query.filter_by(internal_id=projectid).first()
    if project is None:
        flash('The requested project does not exist!')
        return redirect(url_for('index'))
        
    form = TaskForm()
    tasks = Task.query.filter_by(project_id=project.id).all()
        
    current_user.current_project=project.id

    if form.validate_on_submit():
        task = Task(body=form.task_body.data, project_id=project.id)
        db.session.add(task)
        db.session.commit()
        flash('Task succesfully added.')
        return redirect(url_for('project', projectid=project.internal_id))
    return render_template('project.html', project=project, tasks=tasks, form=form)
    
#Delete Task View.  Not really a view, but more of a database action & redirect
@app.route('/projects/deletetask/<taskid>')
@login_required
def delete_task(taskid):
    task = Task.query.filter_by(id=taskid).first()
    db.session.delete(task)
    db.session.commit()
    flash('Task deleted.')
    project = Project.query.filter_by(id=task.project_id).first()
    return redirect(url_for('project', projectid=project.internal_id))
    
#Delete Project View.  Not really a view, but more of a database action & redirect
@app.route('/deleteproject/<projectid>')
@login_required
def delete_project(projectid):
    if not current_user.manager:
        flash('Your not authorized to delete projects.')
        return redirect(url_for('index'))
        
    project = Project.query.filter_by(id=projectid).first()
    db.session.delete(project)
    db.session.commit()
    flash('Project deleted.')
    return redirect(url_for('projects', username=current_user.username))