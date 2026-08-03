from flask import Blueprint
from sqlalchemy import text
from app import db

main = Blueprint('main', __name__)

@main.route('/health')
def health():
    db.session.execute(text('SELECT 1'))
    return {'status': 'ok', 'database': 'connected'}