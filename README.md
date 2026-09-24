# FOCUS Task Manager

Built for SD204B Cloud Application Development at Yoobee Colleges, scenario 3.

A web app for students to register, log in and manage their daily tasks, with a status, priority, date and notes on each task.

Live site: https://focus-task-manager-axbkb2dvcmepcghc.australiasoutheast-01.azurewebsites.net

## Tech stack

- Python 3.14, Flask, Jinja templates
- Flask-Login for accounts, Werkzeug for password hashing
- PostgreSQL with Flask-SQLAlchemy and Flask-Migrate
- Hosted on Azure App Service (gunicorn) with Azure Database for PostgreSQL
- Deployed by GitHub Actions on every push to `main`

## Running it locally

1. Create and activate a virtual environment:
   ```
   python -m venv venv
   source venv/Scripts/activate    # Windows (Git Bash)
   source venv/bin/activate        # macOS / Linux
   ```
2. Install the dependencies:
   ```
   pip install -r requirements.txt
   ```
3. Copy `.env.example` to `.env` and fill in both values. `SECRET_KEY` can be any random string. `DATABASE_URL` is a PostgreSQL URL, or `sqlite:///local-test.db` for a quick local database. Both are required: an empty value stops the app working.
4. Create the database tables:
   ```
   flask db upgrade
   ```
5. Start the app and open http://127.0.0.1:5000:
   ```
   flask run
   ```
