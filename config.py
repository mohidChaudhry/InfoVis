import os
from datetime import timedelta

basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    # Basic Flask Configuration
    SECRET_KEY = os.environ.get('SECRET_KEY', 'secretsecretsecret')
    WTF_CSRF_ENABLED = True
    UPLOAD_FOLDER = 'static/posts'
    
    # Database Configuration
    if os.environ.get('RENDER'): # When deploying on Render
        SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')
        # Fix Render's postgres:// URL to postgresql://
        if SQLALCHEMY_DATABASE_URI and SQLALCHEMY_DATABASE_URI.startswith("postgres://"):
            SQLALCHEMY_DATABASE_URI = SQLALCHEMY_DATABASE_URI.replace("postgres://", "postgresql://", 1)
    else: # Local development
        SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app.db')
    
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    
    # Session configuration
    PERMANENT_SESSION_LIFETIME = timedelta(minutes=30)