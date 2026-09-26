from flask import Blueprint, render_template, request, redirect, url_for
from sqlalchemy import text
from app import db
from app.models import Task
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
    tasks = Task.query.filter_by(user_id=current_user.id).all()
    return render_template('index.html', tasks=tasks)

@main.route('/dashboard')
@login_required
def dashboard():
    # only today's tasks for the logged-in user
    tasks = Task.query.filter_by(user_id=current_user.id, date=date.today()).all()

    return render_template('dashboard.html', tasks=tasks)

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
        db.session.add(new_task)
        db.session.commit()
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
    # go back to the page the request came from, so a refresh doesn't resubmit the form
    next_url = request.form.get('next')
    return redirect(next_url) if next_url else redirect(url_for('main.index'))

@main.route('/tasks/<int:task_id>/delete', methods=['POST'])
@login_required
def delete_task(task_id):
    task_to_delete = Task.query.filter_by(id=task_id, user_id=current_user.id).first_or_404()
    db.session.delete(task_to_delete)
    db.session.commit()
    next_url = request.form.get('next')
    return redirect(next_url) if next_url else redirect(url_for('main.index'))


@main.route('/tasks/<int:task_id>/edit')
@login_required
def edit_task(task_id):
    task = Task.query.filter_by(id=task_id, user_id=current_user.id).first_or_404()
    next_url = request.args.get('next')
    return render_template('edit_task.html', task=task, next_url=next_url)


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