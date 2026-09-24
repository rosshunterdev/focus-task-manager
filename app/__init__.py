from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import Config
from flask_migrate import Migrate
from flask_login import LoginManager

db = SQLAlchemy()

clerk = Migrate()

login_manager = LoginManager()
login_manager.login_view = 'main.login' # send logged-out users to the login page

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    clerk.init_app(app, db)

    from app.routes import main
    from app import models
    app.register_blueprint(main)

    login_manager.init_app(app)

    # Flask-Login uses this to load the logged-in user from the session
    @login_manager.user_loader
    def load_user(user_id):
        # imported here to avoid a circular import
        from app.models import User
        return User.query.get(int(user_id))

    return app