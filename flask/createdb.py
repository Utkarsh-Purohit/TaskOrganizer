# create_db.py

from app import app, db

# Use the app's context manager to create tables
with app.app_context():
    db.create_all()