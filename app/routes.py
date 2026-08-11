from flask import Blueprint, render_template, request, redirect, url_for
from sqlalchemy import text
from app import db
from app.models import Task # added to import the Task class from models.py

main = Blueprint('main', __name__)

@main.route('/health')
def health():
    db.session.execute(text('SELECT 1'))
    return {'status': 'ok', 'database': 'connected'}

@main.route('/')
def index():
    tasks = Task.query.all() ## this is SQL alcehmy - talks to Postgres which runs SELECT * FROM task
        # task.query opens a search interface over the entire task table
        # .all runs SQL alchemy and pulls back every row, and converts it to a Task python object. Comes back as a list
    return render_template('index.html', tasks=tasks)
        # this hands the list of Task objects to the template
        # left tasks is variable name for Jinja to see. right tasks is the actual list of Task objects 
        # (also the python variable from the line above)

@main.route('/tasks/new', methods=['GET', 'POST'])
def create_task():
    if request.method == 'POST':
        title = request.form['title']
        status = request.form['status']
        priority = request.form['priority']
        notes = request.form['notes']

        new_task = Task(title=title, status=status, priority=priority, notes=notes)
            #creates a python object
        db.session.add(new_task)
            #stages
        db.session.commit()
            #saves to database
        return redirect(url_for('main.index'))
    
    else:
        return render_template('create_task.html')