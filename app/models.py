from datetime import date
from app import db
from werkzeug.security import generate_password_hash, check_password_hash

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    status = db.Column(db.String(20), nullable=False, default='Yet-to-do')
    priority = db.Column(db.String(10), nullable=False, default='Medium')
    date = db.Column(db.Date, nullable=False, default=date.today)
    image = db.Column(db.String(300), nullable=True)
    notes = db.Column(db.Text, nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f'<Task {self.id}: {self.title}>' 


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String, nullable=False, unique=True)
    password_hash = db.Column(db.String, nullable=False)

    def set_password(self, plaintext):
        # Use generate_password_hash() to hash plaintext
        hashed = generate_password_hash(plaintext)
        # Store result in self.password_hash
        self.password_hash = hashed
        pass
    
    def check_password(self, plaintext):
        return check_password_hash(self.password_hash, plaintext)
        # Use check_password_hash() to verify plaintext against self.password_hash
        # Return True or False
        pass
    
    def __repr__(self):
        return f'<User {self.id}: {self.email}>'

   