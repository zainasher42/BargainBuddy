from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)

    # Load configuration
    app.config.from_object("config.Config")

    # Initialize database
    db.init_app(app)

    # Import routes
    from app.routes import init_routes
    init_routes(app)

    # Create database tables if they don't exist
    with app.app_context():
        db.create_all()

    return app
