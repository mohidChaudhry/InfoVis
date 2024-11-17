from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import os

db = SQLAlchemy()
migrate = Migrate()

def create_app():
    app = Flask(__name__, 
                static_url_path='/static',
                static_folder='static')
    
    # Load the Config class from config.py
    app.config.from_object('config.Config')
    
    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)
    
    # Force create tables
    with app.app_context():
        try:
            # Import models here to ensure they're known to SQLAlchemy
            from app.models import SurveyResponse
            
            # Create tables
            db.create_all()
            print("Database tables created successfully!")
        except Exception as e:
            print(f"Error creating database tables: {e}")
            # Try to print more detailed error info
            import traceback
            print(traceback.format_exc())
    
    # Register blueprints
    from app.views import main as main_blueprint
    app.register_blueprint(main_blueprint)
    
    return app