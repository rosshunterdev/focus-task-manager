from datetime import date
from app import db

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    status = db.Column(db.String(20), nullable=False, default='Yet-to-do')
    priority = db.Column(db.String(10), nullable=False, default='Medium')
    date = db.Column(db.Date, nullable=False, default=date.today)
    image = db.Column(db.String(300), nullable=True)
    notes = db.Column(db.Text, nullable=True)

    def __repr__(self):
        return f'<Task {self.id}: {self.title}>' 