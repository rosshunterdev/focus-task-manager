from flask import Blueprint, render_template, request, redirect, url_for
from sqlalchemy import text
from app import db
from app.models import Task # added to import the Task class from models.py
from datetime import date
from flask_login import current_user, login_required, logout_user
from app.models import User

main = Blueprint('main', __name__)

@main.route('/health')
def health():
    db.session.execute(text('SELECT 1'))
    return {'status': 'ok', 'database': 'connected'}

@main.route('/')
@login_required
def index():
    tasks = Task.query.filter_by(user_id=current_user.id).all() ## this is SQL alcehmy - talks to Postgres which runs SELECT * FROM task
        # task.query opens a search interface over the entire task table
        # .all runs SQL alchemy and pulls back every row, and converts it to a Task python object. Comes back as a list
    return render_template('index.html', tasks=tasks)
        # this hands the list of Task objects to the template
        # left tasks is variable name for Jinja to see. right tasks is the actual list of Task objects 
        # (also the python variable from the line above)

@main.route('/tasks/new', methods=['GET', 'POST'])
@login_required
def create_task():
    if request.method == 'POST':
        title = request.form['title']
        status = request.form['status']
        priority = request.form['priority']
        notes = request.form['notes']
        date_str = request.form.get('date', '')
        task_date = date.fromisoformat(date_str) if date_str else date.today()

        new_task = Task(title=title, status=status, priority=priority, notes=notes, date=task_date, user_id=current_user.id)
            #creates a python object
        db.session.add(new_task)
            #stages
        db.session.commit()
            #saves to database
        return redirect(url_for('main.index'))
    
    else:
        return render_template('create_task.html')


@main.route('/tasks/<int:task_id>/update', methods=['POST'])
@login_required
def update_task(task_id):
    task_to_update = Task.query.filter_by(id=task_id, user_id=current_user.id).first_or_404()
    task_to_update.title = request.form.get('title', task_to_update.title)
    task_to_update.status = request.form.get('status', task_to_update.status)
    task_to_update.priority = request.form.get('priority', task_to_update.priority)
    task_to_update.notes = request.form.get('notes', task_to_update.notes)
    new_date = request.form.get('date')
    if new_date:
        task_to_update.date = date.fromisoformat(new_date)
    db.session.commit()
    return redirect(url_for('main.index')) # this redirects to the main dashboard
    # redirecting after POST stops the browser from resubmitting the same POST if someone hits refresh

@main.route('/tasks/<int:task_id>/delete', methods=['POST'])
@login_required
def delete_task(task_id):
    task_to_delete = Task.query.filter_by(id=task_id, user_id=current_user.id).first_or_404()
    db.session.delete(task_to_delete)
    db.session.commit()
    return redirect(url_for('main.index'))


@main.route('/tasks/<int:task_id>/edit')
@login_required
def edit_task(task_id):
    task = Task.query.filter_by(id=task_id, user_id=current_user.id).first_or_404()
    return render_template('edit_task.html', task=task)


@main.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            return render_template('register.html', error="Email already registered")

        new_user = User(email=email)
        new_user.set_password(password)
        db.session.add(new_user)
        db.session.commit()

        return redirect(url_for('main.login'))
    return render_template('register.html')

@main.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        user = User.query.filter_by(email=email).first()

        if user and user.check_password(password):
            from flask_login import login_user
            login_user(user)
            return redirect(url_for('main.index'))

        return render_template('login.html', error='Invalid email or password')

    return render_template('login.html')

@main.route('/logout', methods=['POST'])
def logout():
    logout_user()
    return redirect(url_for('main.index'))