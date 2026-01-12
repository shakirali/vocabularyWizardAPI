"""
Database initialization script.
Run this to create all database tables.
"""
from app.database import Base, engine
from app.models import user, vocabulary, progress, quiz

if __name__ == "__main__":
    print("Creating database tables...")
    Base.metadata.create_all(bind=engine)
    print("Database tables created successfully!")

