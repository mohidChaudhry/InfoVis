from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import os

db = SQLAlchemy()
migrate = Migrate()

def create_app():
    app = Flask(__name__)
    port = int(os.environ.get("PORT", 5000))
    
    # Configuration
    if os.environ.get('RENDER'):
        app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')
    else:
        app.config.from_object('config')
    
    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)
    
    # Register blueprints
    from app.views import main as main_blueprint
    app.register_blueprint(main_blueprint)
    
    return app
