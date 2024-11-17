# init_db.py
from app import create_app, db
from app.models import SurveyResponse

def init_database():
    app = create_app()
    with app.app_context():
        try:
            # Drop existing tables
            db.drop_all()
            print("Dropped existing tables")
            
            # Create tables
            db.create_all()
            print("Created new tables")
            
            # Create alembic version table if it doesn't exist
            db.session.execute('CREATE TABLE IF NOT EXISTS alembic_version (version_num VARCHAR(32) PRIMARY KEY)')
            db.session.commit()
            print("Database initialization complete!")
            
        except Exception as e:
            print(f"Error initializing database: {e}")
            import traceback
            print(traceback.format_exc())

if __name__ == "__main__":
    init_database()
