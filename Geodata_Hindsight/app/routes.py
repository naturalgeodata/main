from flask import render_template
from app import app

@app.route('/')
@app.route('/index')
@app.route('/homebase')
def index():
    user = {'username': 'Joshie Poshie'}
    return render_template('index.html',title='Home' , user=user )
