from flask import Blueprint, render_template
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
    tasks = Task.query.all()
    return render_template('index.html', tasks=tasks)
# left tasks is variable name for Jinja to see. right tasks is the actual list of Task objects 
# (also the python variable from the line above)