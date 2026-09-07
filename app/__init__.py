from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import Config
from flask_migrate import Migrate
from flask_login import LoginManager

db = SQLAlchemy()

clerk = Migrate()

login_manager = LoginManager()
login_manager.login_view = 'main.login' #send logged out users back to login view

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    clerk.init_app(app, db)

    from app.routes import main
    from app import models
    app.register_blueprint(main)

    # Initialize Flask-Login — tells Flask how to track logged-in users
    login_manager.init_app(app)

    # This function is called automatically by Flask-Login whenever it needs to fetch a user from the database
    @login_manager.user_loader
    def load_user(user_id):
        # Import User model (inside function to avoid circular imports)
        from app.models import User
        # Query database for the user with this ID, convert string to int
        return User.query.get(int(user_id))

    return app